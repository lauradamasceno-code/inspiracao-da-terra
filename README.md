# Lemaréz Gestão

Painel de gestão para a Lemaréz Perfumaria: clientes (com LGPD), vendas, custos, produtos, catálogo de fragrâncias IF/IM, painel de resultados, **DRE mensal** e exportação em CSV.

> **Esta versão é uma apresentação.** Todos os dados que aparecem (clientes, vendas, custos e histórico mensal, inclusive o do DRE) são **fictícios**. Veja a tabela abaixo.

## Ver a demonstração
- **Localmente:** abra `index.html` no navegador. Não precisa instalar nada.
- **Na web:** em *Settings > Pages* do repositório, escolha a branch `main` e a pasta `/ (root)`. O link aparece na mesma tela.
- O botão **Restaurar dados fictícios** (no topo) volta ao estado original. O que for cadastrado na demonstração fica só no navegador de quem está usando.

## Abas
Painel, **DRE**, Vendas, Custos, Clientes, Produtos e Catálogo. A quantidade nas vendas é sempre um número inteiro. Valores em reais são digitados com vírgula nos centavos (120,50); o botão **Como preencher**, no topo do app, explica o formato de cada campo. O CSV sai separado por ponto e vírgula e com vírgula decimal, para abrir direto no Excel em português.

Na aba Catálogo, o botão **Gerar catálogo em PDF** monta um catálogo com o kit de marca (capa, linha feminina IF e linha masculina IM) a partir das fragrâncias cadastradas. Ele usa a impressão do navegador: na janela que abre, escolha *Salvar como PDF*. Se ela adicionar ou editar uma fragrância, o próximo PDF já sai atualizado.

## O que é real e o que é simulado

| Parte | Estado |
| --- | --- |
| Interface, formulários, filtros, ranking top 10, DRE, catálogo em PDF, perfume extra, CSV | **Real.** Funciona como será usado |
| Catálogo de 54 femininos e 52 masculinos | **Real.** Transcrito do catálogo da Lemaréz, com os nomes como estão nele |
| Regras de privacidade (autorização, CPF validado e oculto, exclusão do cliente) | **Real** no app |
| Clientes, vendas, custos, histórico mensal e histórico do DRE | **Fictícios.** Gerados por `scripts/gerar_mock.py` (`data/mock-db.js`) |
| Onde os dados ficam | **Simulado.** Na demonstração, só no navegador (localStorage) e sem login |
| Banco de dados definitivo com login | **Ainda não está ligado ao app.** Guia em `docs/CRIAR-BANCO-DE-DADOS.md` e modelo em `supabase/schema.sql` (ainda não executado em projeto real) |
| Texto de privacidade | Texto de apoio. Precisa de revisão jurídica antes do uso com clientes |

## Estrutura

```
index.html                 app de demonstração (usa data/mock-db.js)
data/mock-db.js|json       banco de dados FICTÍCIO
scripts/gerar_mock.py      gera o banco fictício
supabase/schema.sql        modelo do banco seguro (PostgreSQL com RLS e CPF cifrado)
supabase/seed_catalogo.sql carga inicial do catálogo no banco
docs/                      resumo para a empreendedora e guias de banco de dados
```

## Banco de dados
O projeto não usa Google Planilhas. O banco recomendado é o Supabase (PostgreSQL com login). O passo a passo para criá-lo está em [docs/CRIAR-BANCO-DE-DADOS.md](docs/CRIAR-BANCO-DE-DADOS.md), e a comparação com outras opções em [docs/ARMAZENAMENTO-SEGURO.md](docs/ARMAZENAMENTO-SEGURO.md).

## Regras de dados
- **Nunca** suba dados reais de clientes para este repositório. O `.gitignore` bloqueia `.csv`, `.xlsx`, `.env` e `config.js`.
- O histórico financeiro real da loja não está aqui.

## Documentos
- [Resumo para a empreendedora](docs/RESUMO-EMPREENDEDORA.md)
- [Criar o banco de dados](docs/CRIAR-BANCO-DE-DADOS.md)
- [Armazenamento seguro dos dados](docs/ARMAZENAMENTO-SEGURO.md)

