# Recopilación y análisis de reseñas escritas Amazon

[简体中文](README.zh-CN.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Español](README.es.md) | [Português](README.pt.md)

Usa el idioma solicitado expresamente; si no se indica, sigue el de la petición. Conserva comandos, identificadores, claves JSON, valores enumerados, unidades y citas originales. Separa traducciones y originales. No deduzcas país, moneda ni jurisdicción por el idioma. Lee las referencias detalladas pertinentes y conserva todos los controles y permisos existentes.

## Instalación y uso

Descarga o clona el repositorio y copia el directorio del Skill indicado, con sus references, scripts, assets y demás dependencias existentes, al directorio de Skills del entorno. Conserva el nombre y SKILL.md. Cambiar el idioma de la documentación no requiere otra instalación. Los comandos son opciones, no pruebas de instalación ni activación.

```sh
git clone https://github.com/PDBen-Auto/amazon-review-intelligence-skill.git
```

## Recopilación y análisis de reseñas escritas Amazon

`amazon-review-scraper`

Recopilar o analizar reseñas de ASIN exactos, deduplicar de forma conservadora y entregar tablas e informes sin conexión trazables.

Directorio del Skill: `.`

**Fundamento y dependencias**

Python 3.10+, openpyxl para XLSX, Pillow opcional para imágenes. Woot opcional solo EE.UU. con ASIN/oferta exactos; otros mercados requieren conector o navegador autorizado disponible.

**Entradas**

Recopilación: ASIN/URL y mercado, filtros opcionales de fecha/estrellas/cantidad. Análisis: JSON/CSV/XLSX/HTML aportado. Definir entregables y privacidad; no repetir captura de archivos completos.

**Salidas**

Fuentes/estado por ASIN, JSON canónico, XLSX/CSV/URL multimedia pedidos, HTML autónomo y transferencia VOC opcional. Texto íntegro, traducción y resumen separados.

[Procedimiento · Límites y condiciones de parada · Ejemplo de solicitud](references/i18n/es.md)

> Usa `$amazon-review-scraper` — Analizar reseñas aportadas de soportes, conservar originales y explicar en español problemas repetidos con límites de muestra; responde en español y conserva pruebas, datos desconocidos y límites de autorización.

## Cobertura lingüística y validación

Esta guía localizada cubre objetivo, requisitos, entradas, salidas, pasos, ejemplos y límites; no traduce línea por línea todas las referencias. La documentación técnica detallada, los casos históricos, errores de scripts, interfaces de ejemplo e imágenes mantienen su idioma original y pueden explicarse a petición. Se comprueban estructura, enlaces y restricciones esenciales; no se afirma una revisión por hablantes nativos de cada idioma.

Antes de entregar, concilia entradas, pruebas, valores ausentes, archivos y criterios de finalización originales. Marca como no verificados los pasos no ejecutados; el éxito de un script no valida conclusiones comerciales.
