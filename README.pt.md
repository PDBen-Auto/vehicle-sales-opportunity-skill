# Visualização de vendas e oportunidades de veículos

[简体中文](README.zh-CN.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Español](README.es.md) | [Português](README.pt.md)

Use o idioma explicitamente solicitado; caso contrário, siga o idioma do pedido. Preserve comandos, identificadores, chaves JSON, valores enumerados, unidades e citações originais. Distinga traduções e originais. Não deduza país, moeda ou jurisdição pelo idioma. Leia as referências detalhadas relevantes e mantenha todas as verificações e autorizações existentes.

## Instalação e utilização

Transfira ou clone o repositório e copie o diretório do Skill indicado, com as suas references, scripts, assets e demais dependências existentes, para o diretório de Skills do ambiente. Preserve o nome e SKILL.md. Mudar o idioma da documentação não exige outra instalação. Os comandos são opções, não provas de instalação ou ativação.

```sh
git clone https://github.com/PDBen-Auto/vehicle-sales-opportunity-skill.git
```

## Visualização de vendas e oportunidades de veículos

`vehicle-sales-opportunity`

Visualizar quantidades existentes de automóveis, motos, UTV, ATV e barcos, comparar períodos iguais e desenhar investigação fundamentada.

Diretório do Skill: `skills/vehicle-sales-opportunity`

**Fundamento e dependências**

Dados autorizados com mercado/período civil/métrica/unidade; Python 3.10+ padrão e navegador para inspeção visual. Núcleo offline sem conta/API; validação exige produto, utilizadores, compatibilidade e custos.

**Entradas**

Obrigatórios dataset JSON mensal, janelas de referência iguais e novo diretório. Opcionais limiares/brief/provas. Manter ausentes/assetType/metricKind; não repartir anos/trimestres igualmente por meses.

**Saídas**

dashboard.html, analysis.json, opportunities.json, report.md, qa.json e research-review.md escrito à parte. Candidatos e PASS aritmético não provam procura, compatibilidade ou ROI.

[Procedimento · Limites e condições de interrupção · Exemplo de pedido](skills/vehicle-sales-opportunity/references/i18n/pt.md)

> Use `$vehicle-sales-opportunity` — Comparar janeiro–junho EUA/Canadá/México com os mesmos meses anteriores; +30% de vendas não prova +30% de procura por acessórios; responda em português e preserve as provas, os dados desconhecidos e os limites de autorização.

[Online examples](https://pdben-auto.github.io/vehicle-sales-opportunity-skill/) · [UTV case](https://pdben-auto.github.io/vehicle-sales-opportunity-skill/cases/utv-atv/) · [Original vehicle dashboard](https://north-america-vehicle-dashboard.pages.dev/)

## Cobertura linguística e validação

Este guia localizado cobre objetivo, requisitos, entradas, saídas, passos, exemplos e limites; não traduz todas as referências linha por linha. Referências técnicas detalhadas, casos históricos, erros de scripts, interfaces de exemplo e imagens mantêm o idioma original e podem ser explicados a pedido. Verificam-se estrutura, ligações e restrições essenciais; não se afirma revisão por falantes nativos de cada idioma.

Antes da entrega, confira entradas, provas, valores em falta, ficheiros e critérios de conclusão originais. Assinale como não verificados os passos não executados; o sucesso de um script não valida conclusões comerciais.
