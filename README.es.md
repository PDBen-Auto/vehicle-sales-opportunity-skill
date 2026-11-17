# Visualización de ventas y oportunidades de vehículos

[简体中文](README.zh-CN.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Español](README.es.md) | [Português](README.pt.md)

Usa el idioma solicitado expresamente; si no se indica, sigue el de la petición. Conserva comandos, identificadores, claves JSON, valores enumerados, unidades y citas originales. Separa traducciones y originales. No deduzcas país, moneda ni jurisdicción por el idioma. Lee las referencias detalladas pertinentes y conserva todos los controles y permisos existentes.

## Instalación y uso

Descarga o clona el repositorio y copia el directorio del Skill indicado, con sus references, scripts, assets y demás dependencias existentes, al directorio de Skills del entorno. Conserva el nombre y SKILL.md. Cambiar el idioma de la documentación no requiere otra instalación. Los comandos son opciones, no pruebas de instalación ni activación.

```sh
git clone https://github.com/PDBen-Auto/vehicle-sales-opportunity-skill.git
```

## Visualización de ventas y oportunidades de vehículos

`vehicle-sales-opportunity`

Visualizar cantidades existentes de coches, motos, UTV, ATV y barcos, comparar periodos equivalentes y diseñar investigación con pruebas.

Directorio del Skill: `skills/vehicle-sales-opportunity`

**Fundamento y dependencias**

Datos autorizados con mercado/periodo civil/métrica/unidad; Python 3.10+ estándar y navegador para revisión visual. Núcleo sin cuenta/API; validar negocio exige producto, usuarios, compatibilidad y costes.

**Entradas**

Obligatorios dataset JSON mensual, ventanas base equivalentes y nuevo directorio. Opcionales umbrales/brief/pruebas. Mantener ausentes/assetType/metricKind; no repartir años/trimestres en meses iguales.

**Salidas**

dashboard.html, analysis.json, opportunities.json, report.md, qa.json y research-review.md escrito aparte. Candidatos y PASS aritmético no prueban demanda, compatibilidad ni ROI.

[Procedimiento · Límites y condiciones de parada · Ejemplo de solicitud](skills/vehicle-sales-opportunity/references/i18n/es.md)

> Usa `$vehicle-sales-opportunity` — Comparar enero–junio de EE.UU./Canadá/México con los mismos meses anteriores; +30% de ventas no demuestra +30% de demanda de accesorios; responde en español y conserva pruebas, datos desconocidos y límites de autorización.

[Online examples](https://pdben-auto.github.io/vehicle-sales-opportunity-skill/) · [UTV case](https://pdben-auto.github.io/vehicle-sales-opportunity-skill/cases/utv-atv/) · [Original vehicle dashboard](https://north-america-vehicle-dashboard.pages.dev/)

## Cobertura lingüística y validación

Esta guía localizada cubre objetivo, requisitos, entradas, salidas, pasos, ejemplos y límites; no traduce línea por línea todas las referencias. La documentación técnica detallada, los casos históricos, errores de scripts, interfaces de ejemplo e imágenes mantienen su idioma original y pueden explicarse a petición. Se comprueban estructura, enlaces y restricciones esenciales; no se afirma una revisión por hablantes nativos de cada idioma.

Antes de entregar, concilia entradas, pruebas, valores ausentes, archivos y criterios de finalización originales. Marca como no verificados los pasos no ejecutados; el éxito de un script no valida conclusiones comerciales.
