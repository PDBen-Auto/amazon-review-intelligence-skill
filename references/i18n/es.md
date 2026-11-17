# Recopilación y análisis de reseñas escritas Amazon

`amazon-review-scraper` · Español

## Objetivo y alcance

Recopilar o analizar reseñas de ASIN exactos, deduplicar de forma conservadora y entregar tablas e informes sin conexión trazables.

## Fundamento y dependencias

Python 3.10+, openpyxl para XLSX, Pillow opcional para imágenes. Woot opcional solo EE.UU. con ASIN/oferta exactos; otros mercados requieren conector o navegador autorizado disponible.

## Entradas

Recopilación: ASIN/URL y mercado, filtros opcionales de fecha/estrellas/cantidad. Análisis: JSON/CSV/XLSX/HTML aportado. Definir entregables y privacidad; no repetir captura de archivos completos.

## Salidas

Fuentes/estado por ASIN, JSON canónico, XLSX/CSV/URL multimedia pedidos, HTML autónomo y transferencia VOC opcional. Texto íntegro, traducción y resumen separados.

## Procedimiento

1. Confirmar producto/mercado
2. verificar Woot o alternativa autorizada
3. cero de interfaz/páginas fallidas no significan vacío completo
4. fusionar por ID o texto completo demostrado
5. un problema/beneficio principal por reseña, etiquetas secundarias no exclusivas
6. abrir entregables y conciliar recuentos.

## Límites y condiciones de parada

Detener en CAPTCHA, acceso o inicio de sesión. No leer cookies, pedidos ni cuentas. Escapar HTML/fórmulas. Reseñas ≠ valoraciones, muestra ≠ tasa poblacional de fallos. Campos fijos translation_zh/summary_zh siguen en chino.

## Ejemplo de solicitud

Usa `$amazon-review-scraper` — Analizar reseñas aportadas de soportes, conservar originales y explicar en español problemas repetidos con límites de muestra; responde en español y conserva pruebas, datos desconocidos y límites de autorización.

## Especificación completa

[Entrada del Skill y referencias detalladas](../../SKILL.md).

Usa el idioma solicitado expresamente; si no se indica, sigue el de la petición. Conserva comandos, identificadores, claves JSON, valores enumerados, unidades y citas originales. Separa traducciones y originales. No deduzcas país, moneda ni jurisdicción por el idioma. Lee las referencias detalladas pertinentes y conserva todos los controles y permisos existentes.

Antes de entregar, concilia entradas, pruebas, valores ausentes, archivos y criterios de finalización originales. Marca como no verificados los pasos no ejecutados; el éxito de un script no valida conclusiones comerciales.

## Cobertura lingüística y validación

Esta guía localizada cubre objetivo, requisitos, entradas, salidas, pasos, ejemplos y límites; no traduce línea por línea todas las referencias. La documentación técnica detallada, los casos históricos, errores de scripts, interfaces de ejemplo e imágenes mantienen su idioma original y pueden explicarse a petición. Se comprueban estructura, enlaces y restricciones esenciales; no se afirma una revisión por hablantes nativos de cada idioma.

