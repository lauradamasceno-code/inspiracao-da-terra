-- Lemaréz Gestão: modelo de dados para Supabase (PostgreSQL)
-- STATUS: proposta. Não foi executado em nenhum projeto Supabase ainda. Teste num projeto vazio antes de usar.
--
-- Ideias de segurança:
--  1. Login obrigatório (Supabase Auth). Cada linha pertence a um usuário (owner_id).
--  2. Row Level Security: ninguém lê ou grava linha de outro usuário, nem com a chave pública do app.
--  3. CPF guardado cifrado (cpf_cifrado). A chave fica no Supabase Vault, nunca no código do app.
--  4. Excluir cliente apaga os dados pessoais e deixa as vendas sem cliente (on delete set null).
--  5. Trilha de auditoria para exclusões de clientes.

create extension if not exists pgcrypto with schema extensions;

-- ---------- tabelas ----------
create table public.clientes (
  id              uuid primary key default gen_random_uuid(),
  owner_id        uuid not null default auth.uid() references auth.users(id) on delete cascade,
  nome            text not null check (char_length(nome) between 1 and 200),
  cpf_cifrado     bytea,                                   -- use salvar_cpf() / ler_cpf()
  cpf_final       text check (cpf_final ~ '^[0-9]{2}$'),   -- 2 últimos dígitos, para exibir mascarado
  endereco        text check (char_length(endereco) <= 300),
  email           text check (char_length(email) <= 200),
  telefone        text not null check (telefone ~ '^[0-9]{10,13}$'),
  nascimento      date,
  consentimento_em date not null,                          -- data em que o cliente autorizou
  criado_em       timestamptz not null default now()
);

create table public.produtos (
  id        uuid primary key default gen_random_uuid(),
  owner_id  uuid not null default auth.uid() references auth.users(id) on delete cascade,
  nome      text not null,
  categoria text not null check (categoria in ('Perfume','Perfume extras','Vela','Água de lençol','Outro')),
  preco     numeric(12,2) check (preco >= 0),
  custo     numeric(12,2) check (custo >= 0)
);

create table public.catalogo (
  owner_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  codigo   text not null check (codigo ~ '^I[FM][0-9]{2}$'),
  nome     text not null,
  marca    text,
  genero   text generated always as (case when codigo like 'IF%' then 'Feminino' else 'Masculino' end) stored,
  primary key (owner_id, codigo)
);

create table public.vendas (
  id         uuid primary key default gen_random_uuid(),
  owner_id   uuid not null default auth.uid() references auth.users(id) on delete cascade,
  data       date not null,
  descricao  text not null,
  cliente_id uuid references public.clientes(id) on delete set null,
  tipo       text not null default 'Receita' check (tipo = 'Receita'),
  categoria  text not null check (categoria in ('Receita Operacional Bruta','Deduções da Receita Bruta')),
  produto    text not null,
  frag       text check (frag ~ '^(I[FM][0-9]{2}|EXTRA)$'),   -- código do catálogo ou EXTRA
  extra      text,                                            -- nome do perfume extra
  qtd        numeric(10,2) not null check (qtd > 0),
  pagamento  text not null check (pagamento in ('PIX','Crédito','Débito','Dinheiro','Pagamento online','PIX (Maquininha)')),
  valor      numeric(12,2) not null check (valor >= 0)
);

create table public.custos (
  id        uuid primary key default gen_random_uuid(),
  owner_id  uuid not null default auth.uid() references auth.users(id) on delete cascade,
  data      date not null,
  descricao text not null,
  tipo      text not null check (tipo in ('Custo Variável','Despesas Adm','Impostos')),
  categoria text not null check (categoria in ('Insumos e Matérias-primas','Logística','Fixas e Operacionais','Impostos Extras')),
  pagamento text not null check (pagamento in ('PIX','Crédito','Débito','Dinheiro','Pagamento online','PIX (Maquininha)')),
  valor     numeric(12,2) not null check (valor >= 0)
);

create table public.auditoria (
  id        bigint generated always as identity primary key,
  owner_id  uuid,
  quando    timestamptz not null default now(),
  acao      text not null,
  tabela    text not null,
  registro  uuid
);

create index on public.vendas (owner_id, data desc);
create index on public.vendas (cliente_id);
create index on public.custos (owner_id, data desc);
create index on public.clientes (owner_id, nome);

-- ---------- Row Level Security ----------
do $$
declare t text;
begin
  foreach t in array array['clientes','produtos','catalogo','vendas','custos'] loop
    execute format('alter table public.%I enable row level security', t);
    execute format('create policy "dono_total" on public.%I for all to authenticated using (owner_id = auth.uid()) with check (owner_id = auth.uid())', t);
  end loop;
end $$;

alter table public.auditoria enable row level security;
create policy "dono_le_auditoria" on public.auditoria for select to authenticated using (owner_id = auth.uid());

-- ---------- CPF cifrado ----------
-- Antes: crie o segredo no Vault (Dashboard > Vault) com o nome cpf_key e um valor longo e aleatório.
create or replace function public.salvar_cpf(p_cliente uuid, p_cpf text) returns void
language plpgsql security definer set search_path = public, extensions, vault as $$
declare k text; d text := regexp_replace(p_cpf, '\D', '', 'g');
begin
  if length(d) <> 11 then raise exception 'CPF inválido'; end if;
  select decrypted_secret into k from vault.decrypted_secrets where name = 'cpf_key';
  if k is null then raise exception 'Segredo cpf_key não configurado'; end if;
  update public.clientes
     set cpf_cifrado = pgp_sym_encrypt(d, k), cpf_final = right(d, 2)
   where id = p_cliente and owner_id = auth.uid();
end $$;

create or replace function public.ler_cpf(p_cliente uuid) returns text
language plpgsql security definer set search_path = public, extensions, vault as $$
declare k text; r bytea;
begin
  select decrypted_secret into k from vault.decrypted_secrets where name = 'cpf_key';
  select cpf_cifrado into r from public.clientes where id = p_cliente and owner_id = auth.uid();
  if r is null then return null; end if;
  insert into public.auditoria(owner_id, acao, tabela, registro) values (auth.uid(), 'ler_cpf', 'clientes', p_cliente);
  return pgp_sym_decrypt(r, k);
end $$;

revoke all on function public.salvar_cpf(uuid, text) from public, anon;
revoke all on function public.ler_cpf(uuid) from public, anon;
grant execute on function public.salvar_cpf(uuid, text) to authenticated;
grant execute on function public.ler_cpf(uuid) to authenticated;

-- ---------- auditoria de exclusão de cliente ----------
create or replace function public.audita_exclusao_cliente() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  insert into public.auditoria(owner_id, acao, tabela, registro) values (old.owner_id, 'excluir', 'clientes', old.id);
  return old;
end $$;
create trigger trg_audita_cliente after delete on public.clientes
  for each row execute function public.audita_exclusao_cliente();
