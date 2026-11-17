# Visualização de vendas e oportunidades de veículos

`vehicle-sales-opportunity` · Português

## Objetivo e âmbito

Visualizar quantidades existentes de automóveis, motos, UTV, ATV e barcos, comparar períodos iguais e desenhar investigação fundamentada.

## Fundamento e dependências

Dados autorizados com mercado/período civil/métrica/unidade; Python 3.10+ padrão e navegador para inspeção visual. Núcleo offline sem conta/API; validação exige produto, utilizadores, compatibilidade e custos.

## Entradas

Obrigatórios dataset JSON mensal, janelas de referência iguais e novo diretório. Opcionais limiares/brief/provas. Manter ausentes/assetType/metricKind; não repartir anos/trimestres igualmente por meses.

## Saídas

dashboard.html, analysis.json, opportunities.json, report.md, qa.json e research-review.md escrito à parte. Candidatos e PASS aritmético não provam procura, compatibilidade ou ROI.

## Procedimento

1. Fixar pergunta/mercados/unidades/direitos
2. ID estáveis, separar CY/MY, vendas/parque, tipos e retalho/grosso/entregas/novos registos
3. validar/gerar
4. conferir subidas/descidas/base zero/ausentes nas mesmas coortes completas
5. rever hipóteses com prova/teste mínimo/paragem
6. verificar filtros/detalhes/exportação em computador/telemóvel.

## Limites e condições de interrupção

Sem compra de dados nem publicação automática. Caso UTV:124 entradas,105 fontes, coortes históricas calculáveis US63/CA15/MX1; VIO total desconhecido. Cenários não são vendas observadas, intervalos de confiança ou limites inferiores. Canais ATV estudados mas ATV excluídos do dataset UTV; refinamento de anos/imagens pendente.

## Exemplo de pedido

Use `$vehicle-sales-opportunity` — Comparar janeiro–junho EUA/Canadá/México com os mesmos meses anteriores; +30% de vendas não prova +30% de procura por acessórios; responda em português e preserve as provas, os dados desconhecidos e os limites de autorização.

## Especificação completa

[Entrada do Skill e referências detalhadas](../../SKILL.md).

Use o idioma explicitamente solicitado; caso contrário, siga o idioma do pedido. Preserve comandos, identificadores, chaves JSON, valores enumerados, unidades e citações originais. Distinga traduções e originais. Não deduza país, moeda ou jurisdição pelo idioma. Leia as referências detalhadas relevantes e mantenha todas as verificações e autorizações existentes.

Antes da entrega, confira entradas, provas, valores em falta, ficheiros e critérios de conclusão originais. Assinale como não verificados os passos não executados; o sucesso de um script não valida conclusões comerciais.

## Cobertura linguística e validação

Este guia localizado cobre objetivo, requisitos, entradas, saídas, passos, exemplos e limites; não traduz todas as referências linha por linha. Referências técnicas detalhadas, casos históricos, erros de scripts, interfaces de exemplo e imagens mantêm o idioma original e podem ser explicados a pedido. Verificam-se estrutura, ligações e restrições essenciais; não se afirma revisão por falantes nativos de cada idioma.

