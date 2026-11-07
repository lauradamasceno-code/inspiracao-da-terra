# Lemaréz Gestão

Painel de gestão para a Lemaréz Perfumaria: clientes (com LGPD), vendas, custos, produtos e o catálogo de fragrâncias IF/IM, com painel de resultados e exportação em CSV.

> **Esta versão é uma apresentação.** Todos os dados que aparecem (clientes, vendas, custos e histórico mensal) são **fictícios**. Veja a tabela abaixo.

## Ver a demonstração
- **Localmente:** abra `index.html` no navegador. Não precisa instalar nada.
- **Na web:** em *Settings > Pages* do repositório, escolha a branch `main` e a pasta `/ (root)`. O link aparece na mesma tela.
- O botão **Restaurar dados fictícios** (no topo) volta ao estado original. O que for cadastrado na demonstração fica só no navegador de quem está usando.

## O que é real e o que é simulado

| Parte | Estado |
| --- | --- |
| Interface, formulários, filtros, ranking top 10, perfume extra, CSV | **Real.** Funciona como será usado |
| Catálogo de 54 femininos e 52 masculinos | **Real.** Transcrito do catálogo da Lemaréz, com os nomes como estão nele |
| Regras de privacidade (autorização, CPF validado e oculto, exclusão do cliente) | **Real** no app |
| Clientes, vendas, custos, histórico mensal | **Fictícios.** Gerados por `scripts/gerar_mock.py` (`data/mock-db.js`) |
| Onde os dados ficam | **Simulado.** Na demonstração, só no navegador (localStorage) e sem login |
| Banco de dados definitivo com login | **Ainda não existe.** Proposta em `supabase/schema.sql` e `docs/ARMAZENAMENTO-SEGURO.md` |
| Versão em Google Planilhas (`apps-script/`) | **Funciona em teste simulado.** Não foi instalada numa conta Google real |
| Texto de privacidade | Texto de apoio. Precisa de revisão jurídica antes do uso com clientes |

## Estrutura

```
index.html                 app de demonstração (usa data/mock-db.js)
data/mock-db.js|json       banco de dados FICTÍCIO
scripts/gerar_mock.py      gera o banco fictício
apps-script/               versão que salva numa planilha Google (Code.gs + Index.html)
supabase/schema.sql        proposta de banco seguro (PostgreSQL com RLS e CPF cifrado)
docs/                      resumo para a empreendedora e guia de armazenamento seguro
```

## Regras de dados
- **Nunca** suba dados reais de clientes para este repositório. O `.gitignore` bloqueia `.csv`, `.xlsx` e `.env`.
- O histórico financeiro real da loja não está aqui.

## Documentos
- [Resumo para a empreendedora](docs/RESUMO-EMPREENDEDORA.md)
- [Armazenamento seguro dos dados](docs/ARMAZENAMENTO-SEGURO.md)

## Equipe
| Nome | E-mail |
| --- | --- |
| (preencher) | (preencher) |
