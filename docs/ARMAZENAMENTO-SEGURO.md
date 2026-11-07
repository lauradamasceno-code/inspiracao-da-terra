# Onde guardar os dados com segurança

A decisão da equipe é **não usar Google Planilhas**. Hoje o app é uma demonstração com dados fictícios guardados no navegador. Para uso real, a recomendação é um banco de dados de verdade com login. O passo a passo para criá-lo está em [CRIAR-BANCO-DE-DADOS.md](CRIAR-BANCO-DE-DADOS.md).

## Comparação

| Opção | Vantagens | Pontos de atenção |
| --- | --- | --- |
| **Supabase (PostgreSQL)** | Banco de verdade, login com e-mail e senha, autenticação em dois fatores, regras de acesso por linha (RLS), cifragem de campos, painel simples | Serviço de terceiro: é preciso conferir os termos de operador de dados. Plano gratuito pausa após 1 semana sem uso e não faz backup automático. Plano Pro a partir de US$ 25/mês, com backup diário por 7 dias ([preços oficiais](https://supabase.com/pricing.md)). Confirmar na criação do projeto se a região de São Paulo está disponível |
| Firebase | Fácil de ligar ao app, login pronto | Banco de documentos, mais difícil para relatórios como o DRE |
| Airtable | Parece uma planilha, fácil para a lojista | Dados de clientes em serviço de terceiros fora do Brasil; limites de registros; menos controle de acesso fino |
| Servidor próprio (VPS + PostgreSQL) | Controle total e custo baixo | Exige manter servidor, atualizações, backup e segurança. Só vale com alguém para cuidar disso |

## Recomendação

**Supabase**, com o app publicado numa página protegida por login. O arquivo `supabase/schema.sql` já tem o modelo de dados com:

- login obrigatório e acesso só aos dados do próprio usuário (RLS);
- CPF cifrado, com a chave guardada no Vault do Supabase e fora do código;
- exclusão de cliente que apaga os dados pessoais e mantém as vendas sem vínculo;
- registro de auditoria de exclusões e leituras de CPF.

**Estado:** o SQL é uma proposta e ainda não foi executado. O app também ainda não está ligado ao banco. O app já concentra a gravação em um único ponto (`B`, no `index.html`), então ligar o banco é escrever um adaptador no lugar dele.

## Plano de implantação
1. Criar o projeto e o usuário da lojista, seguindo [CRIAR-BANCO-DE-DADOS.md](CRIAR-BANCO-DE-DADOS.md).
2. Escrever o adaptador do app para o banco, com tela de login.
3. Importar o catálogo (`supabase/seed_catalogo.sql`) e, se a lojista quiser, as vendas reais da planilha financeira.
4. Publicar o app em hospedagem com HTTPS (GitHub Pages, Netlify ou Vercel).
5. Passar para o plano Pro (ou fazer backup manual semanal) antes de cadastrar clientes reais.

## Checklist de LGPD para a empreendedora
- Definir quem responde pelos dados (a lojista, como controladora) e um e-mail para pedidos dos clientes.
- Revisar o texto de privacidade com um profissional jurídico e ter um aviso para o cliente no balcão ou no WhatsApp.
- Conferir os termos do serviço de banco de dados, que atua como operador dos dados.
- Coletar só o necessário (o CPF é opcional), responder pedidos de acesso, correção e exclusão e revisar cadastros parados uma vez por ano.
- Ter um plano para incidentes: quem avisar e como trocar senhas rapidamente.

Este documento é um guia técnico e não substitui orientação jurídica.
