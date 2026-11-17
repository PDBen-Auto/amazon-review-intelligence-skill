# Recolha e análise de avaliações escritas Amazon

`amazon-review-scraper` · Português

## Objetivo e âmbito

Recolher ou analisar avaliações de ASIN exatos, deduplicar com prudência e entregar tabelas/relatórios offline rastreáveis.

## Fundamento e dependências

Python 3.10+, openpyxl para XLSX, Pillow opcional para imagens. Woot opcional apenas EUA com correspondência ASIN/oferta exata; outros mercados exigem conector ou navegador autorizado disponível.

## Entradas

Recolha: ASIN/URL e mercado, filtros opcionais de data/estrelas/quantidade. Análise: JSON/CSV/XLSX/HTML fornecido. Definir entregáveis e privacidade; não repetir ficheiros completos.

## Saídas

Fontes/estado por ASIN, JSON canónico, XLSX/CSV/URL multimédia pedidos, HTML autónomo e passagem VOC opcional. Original completo, tradução e resumo separados.

## Procedimento

1. Identificar produto/mercado
2. verificar Woot ou alternativa permitida
3. zero na interface/paginação falhada não prova conjunto vazio completo
4. fundir por ID ou texto integral comprovado
5. um problema/benefício principal por avaliação, etiquetas secundárias não exclusivas
6. abrir e conferir contagens.

## Limites e condições de interrupção

Parar em CAPTCHA, autenticação ou restrições. Não ler cookies, encomendas ou contas. Proteger HTML/fórmulas. Avaliações escritas ≠ classificações; amostra ≠ taxa de defeito da população. Campos fixos translation_zh/summary_zh permanecem em chinês.

## Exemplo de pedido

Use `$amazon-review-scraper` — Analisar avaliações fornecidas de suportes, manter originais e explicar em português temas recorrentes e limites da amostra; responda em português e preserve as provas, os dados desconhecidos e os limites de autorização.

## Especificação completa

[Entrada do Skill e referências detalhadas](../../SKILL.md).

Use o idioma explicitamente solicitado; caso contrário, siga o idioma do pedido. Preserve comandos, identificadores, chaves JSON, valores enumerados, unidades e citações originais. Distinga traduções e originais. Não deduza país, moeda ou jurisdição pelo idioma. Leia as referências detalhadas relevantes e mantenha todas as verificações e autorizações existentes.

Antes da entrega, confira entradas, provas, valores em falta, ficheiros e critérios de conclusão originais. Assinale como não verificados os passos não executados; o sucesso de um script não valida conclusões comerciais.

## Cobertura linguística e validação

Este guia localizado cobre objetivo, requisitos, entradas, saídas, passos, exemplos e limites; não traduz todas as referências linha por linha. Referências técnicas detalhadas, casos históricos, erros de scripts, interfaces de exemplo e imagens mantêm o idioma original e podem ser explicados a pedido. Verificam-se estrutura, ligações e restrições essenciais; não se afirma revisão por falantes nativos de cada idioma.

