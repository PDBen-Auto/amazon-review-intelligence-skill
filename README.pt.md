# Recolha e análise de avaliações escritas Amazon

[简体中文](README.zh-CN.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Español](README.es.md) | [Português](README.pt.md)

Use o idioma explicitamente solicitado; caso contrário, siga o idioma do pedido. Preserve comandos, identificadores, chaves JSON, valores enumerados, unidades e citações originais. Distinga traduções e originais. Não deduza país, moeda ou jurisdição pelo idioma. Leia as referências detalhadas relevantes e mantenha todas as verificações e autorizações existentes.

## Instalação e utilização

Transfira ou clone o repositório e copie o diretório do Skill indicado, com as suas references, scripts, assets e demais dependências existentes, para o diretório de Skills do ambiente. Preserve o nome e SKILL.md. Mudar o idioma da documentação não exige outra instalação. Os comandos são opções, não provas de instalação ou ativação.

```sh
git clone https://github.com/PDBen-Auto/amazon-review-intelligence-skill.git
```

## Recolha e análise de avaliações escritas Amazon

`amazon-review-scraper`

Recolher ou analisar avaliações de ASIN exatos, deduplicar com prudência e entregar tabelas/relatórios offline rastreáveis.

Diretório do Skill: `.`

**Fundamento e dependências**

Python 3.10+, openpyxl para XLSX, Pillow opcional para imagens. Woot opcional apenas EUA com correspondência ASIN/oferta exata; outros mercados exigem conector ou navegador autorizado disponível.

**Entradas**

Recolha: ASIN/URL e mercado, filtros opcionais de data/estrelas/quantidade. Análise: JSON/CSV/XLSX/HTML fornecido. Definir entregáveis e privacidade; não repetir ficheiros completos.

**Saídas**

Fontes/estado por ASIN, JSON canónico, XLSX/CSV/URL multimédia pedidos, HTML autónomo e passagem VOC opcional. Original completo, tradução e resumo separados.

[Procedimento · Limites e condições de interrupção · Exemplo de pedido](references/i18n/pt.md)

> Use `$amazon-review-scraper` — Analisar avaliações fornecidas de suportes, manter originais e explicar em português temas recorrentes e limites da amostra; responda em português e preserve as provas, os dados desconhecidos e os limites de autorização.

## Cobertura linguística e validação

Este guia localizado cobre objetivo, requisitos, entradas, saídas, passos, exemplos e limites; não traduz todas as referências linha por linha. Referências técnicas detalhadas, casos históricos, erros de scripts, interfaces de exemplo e imagens mantêm o idioma original e podem ser explicados a pedido. Verificam-se estrutura, ligações e restrições essenciais; não se afirma revisão por falantes nativos de cada idioma.

Antes da entrega, confira entradas, provas, valores em falta, ficheiros e critérios de conclusão originais. Assinale como não verificados os passos não executados; o sucesso de um script não valida conclusões comerciais.
