# Onde guardar os dados com segurança

Hoje o app tem dois modos: a **demonstração** (dados fictícios no navegador) e a versão em **Google Planilhas** (pasta `apps-script/`). Se a equipe não quer Google Planilhas, a recomendação abaixo é um banco de dados de verdade com login.

## Comparação

| Opção | Vantagens | Pontos de atenção |
| --- | --- | --- |
| **Supabase (PostgreSQL)** | Banco de verdade, login com e-mail e senha, autenticação em dois fatores, regras de acesso por linha (RLS), cifragem de campos, painel simples | Serviço de terceiro: é preciso contrato/termos de operador de dados. Plano gratuito pausa após 1 semana sem uso e não faz backup automático. Plano Pro a partir de US$ 25/mês, com backup diário por 7 dias ([preços oficiais](https://supabase.com/pricing.md)). Confirmar na criação do projeto se a região de São Paulo está disponível |
| Firebase (Google) | Fácil de ligar ao app, login pronto | Também é Google, o que não resolve o incômodo com o Google. Banco de documentos, mais difícil para relatórios |
| Airtable | Parece uma planilha, fácil para a lojista | Dados de clientes em serviço de terceiros fora do Brasil; limites de registros; menos controle de acesso fino |
| Servidor próprio (VPS + PostgreSQL) | Controle total e custo baixo | Exige manter servidor, atualizações, backup e segurança. Só vale com alguém para cuidar disso |
| Google Planilhas (atual) | Zero custo, a loja já usa Google | Não é feito para dados pessoais; fácil de compartilhar sem querer; sem trilha de auditoria |

## Recomendação

**Supabase**, com o app publicado numa página protegida por login. O arquivo `supabase/schema.sql` já tem o modelo de dados com:

- login obrigatório e acesso só aos dados do próprio usuário (RLS);
- CPF cifrado, com a chave guardada no Vault do Supabase e fora do código;
- exclusão de cliente que apaga os dados pessoais e mantém as vendas sem vínculo;
- registro de auditoria de exclusões e leituras de CPF.

**Estado:** o SQL é uma proposta e ainda não foi executado. O app também ainda não está ligado ao Supabase. O app já separa a gravação em um único ponto (`B`, no `index.html`), então trocar Google Planilhas por Supabase é escrever um adaptador no lugar dele.

## Plano de implantação

1. Criar a conta e um projeto no Supabase na conta da Lemaréz (ou da empresa que vai manter o app) e escolher a região mais próxima do Brasil.
2. Criar o segredo `cpf_key` no Vault e rodar `supabase/schema.sql`.
3. Criar o usuário da lojista, ativar verificação em duas etapas e desligar o cadastro público de novos usuários.
4. Escrever o adaptador do app para o Supabase e importar o catálogo e, se a lojista quiser, as vendas reais da planilha financeira.
5. Publicar o app em hospedagem com HTTPS (GitHub Pages, Netlify ou Vercel) e ligar o login.
6. Plano Pro (ou backup manual semanal) antes de cadastrar clientes reais.

## Checklist de LGPD para a empreendedora

- Definir quem responde pelos dados (a lojista, como controladora) e um e-mail para pedidos dos clientes.
- Revisar o texto de privacidade com um profissional jurídico e ter um aviso para o cliente no balcão ou no WhatsApp.
- Contratar o serviço de banco de dados sabendo que ele é um operador de dados e conferir os termos dele.
- Coletar só o necessário (o CPF é opcional), responder pedidos de acesso, correção e exclusão e revisar cadastros parados uma vez por ano.
- Ter um plano para incidentes: quem avisar e como trocar senhas rapidamente.

Este documento é um guia técnico e não substitui orientação jurídica.
