# Criar o banco de dados (passo a passo)

Este guia cria o banco de dados da Lemaréz no **Supabase** (PostgreSQL com login). Leva cerca de 30 minutos.

> **Estado do projeto:** o banco criado por este guia ainda **não está ligado ao app**. A demonstração continua guardando dados fictícios no navegador. O próximo passo de desenvolvimento é escrever o adaptador que faz o app ler e gravar neste banco. O SQL deste guia é uma proposta que ainda não foi executada num projeto real, então teste num projeto vazio primeiro.

Os nomes de menus do Supabase podem mudar com o tempo. Se não achar um item, use a busca do painel ou a [documentação oficial](https://supabase.com/docs).

## O que você precisa
- Um e-mail da Lemaréz (ou da empresa que vai manter o app) para a conta Supabase.
- Um gerenciador de senhas para guardar as senhas e chaves (por exemplo Bitwarden ou 1Password).
- Os arquivos `supabase/schema.sql` e `supabase/seed_catalogo.sql` deste repositório.

## 1. Criar a conta e o projeto
1. Entre em supabase.com e crie a conta. Ative a **verificação em duas etapas** na conta.
2. Clique em **New project** e preencha:
   - **Name:** `lemarez-gestao`
   - **Database password:** use o gerador de senha e **guarde no gerenciador de senhas**.
   - **Region:** escolha a opção mais próxima do Brasil. Se houver **South America (São Paulo)**, escolha essa.
   - **Plan:** o plano gratuito serve para testar, mas pausa o projeto após 1 semana sem uso e não faz backup automático. Antes de cadastrar clientes reais, passe para o **Pro** (a partir de US$ 25/mês e com backup diário por 7 dias, [conforme a página de preços](https://supabase.com/pricing.md)).
3. Espere o projeto ficar pronto (alguns minutos).

## 2. Criar o segredo que cifra o CPF
1. No menu, abra **Database > Vault** (ou procure por "Vault").
2. Crie um segredo com o nome exato `cpf_key` e um valor longo e aleatório (use o gerador do gerenciador de senhas).
3. Guarde esse valor também no gerenciador de senhas. **Se ele for perdido, os CPFs cifrados não podem ser recuperados.**

## 3. Criar as tabelas
1. Abra **SQL Editor > New query**.
2. Cole todo o conteúdo de `supabase/schema.sql` e clique em **Run**.
3. Confira em **Table Editor** se existem as tabelas `clientes`, `vendas`, `custos`, `produtos`, `catalogo` e `auditoria`, todas com a marca de segurança **RLS enabled**.

## 4. Criar o usuário da lojista e fechar o cadastro
1. Abra **Authentication > Users > Add user > Create new user**. Informe o e-mail da lojista e uma senha forte, e marque a confirmação do e-mail.
2. Abra as configurações de login (**Authentication > Sign In / Providers**) e **desative a criação de novos usuários** (Allow new users to sign up). Assim, só quem você cadastrar consegue entrar.
3. Ative o segundo fator (**Authentication > Multi-Factor**, opção TOTP). A lojista vai cadastrar o app autenticador no primeiro acesso.
4. Copie o **User UID** da lojista (aparece na lista de usuários). Você vai usar no próximo passo.

## 5. Carregar o catálogo de perfumes
1. Abra `supabase/seed_catalogo.sql` e troque o valor de `v_dono` pelo **User UID** da lojista.
2. Cole no **SQL Editor** e clique em **Run**.
3. Em **Table Editor > catalogo**, confira as 106 linhas (54 IF e 52 IM).

## 6. Testar a segurança antes de usar
1. Em **Project Settings > API**, copie o **Project URL** e a chave pública (`anon` ou `publishable`). Essa chave pode ir no app, porque o acesso é limitado pelas regras RLS.
2. **Nunca** use a chave `service_role` no app nem a envie para o GitHub. Ela ignora todas as regras de segurança.
3. Sem login, tente ler `clientes` pela API usando só a chave pública. O resultado deve ser uma lista vazia.
4. Crie um segundo usuário de teste, cadastre um cliente de teste com um deles e confirme que o outro não vê. Depois apague o usuário e o cliente de teste.

## 7. Backup e rotina
- Com o plano Pro, o backup diário fica em **Database > Backups**. Anote a data do último backup uma vez por mês.
- Se ficar no plano gratuito, exporte as tabelas em CSV toda semana (Table Editor > Export) e guarde em local protegido. O CSV de clientes tem dados pessoais e deve ser apagado depois de usado.
- Uma vez por ano, exclua cadastros de quem não compra mais.

## 8. Guardar as chaves
- Guarde no gerenciador de senhas: senha do banco, valor de `cpf_key`, Project URL e chave pública.
- No código do app, as chaves vão num arquivo `config.js` que **não é enviado ao GitHub** (inclua `config.js` no `.gitignore`).

## 9. Próximos passos (desenvolvimento)
1. Adaptador do app para o Supabase (login, leitura e gravação nas tabelas acima, CPF pelas funções `salvar_cpf` e `ler_cpf`).
2. Importar as vendas reais da planilha financeira.
3. Publicar o app com HTTPS (GitHub Pages, Netlify ou Vercel) e testar na loja por uma semana.
4. Revisar com um profissional jurídico o texto de privacidade e os termos do serviço de banco de dados.

## Se der erro
- **"permission denied" ou lista vazia depois do login:** confira se `owner_id` das linhas é o UID da lojista.
- **Erro ao salvar CPF:** confira se o segredo `cpf_key` existe no Vault, com esse nome exato.
- **Projeto pausado:** no plano gratuito, abra o painel e clique em restaurar. No plano Pro isso não acontece.
