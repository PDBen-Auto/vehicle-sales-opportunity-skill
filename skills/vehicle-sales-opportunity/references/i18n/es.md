# Visualización de ventas y oportunidades de vehículos

`vehicle-sales-opportunity` · Español

## Objetivo y alcance

Visualizar cantidades existentes de coches, motos, UTV, ATV y barcos, comparar periodos equivalentes y diseñar investigación con pruebas.

## Fundamento y dependencias

Datos autorizados con mercado/periodo civil/métrica/unidad; Python 3.10+ estándar y navegador para revisión visual. Núcleo sin cuenta/API; validar negocio exige producto, usuarios, compatibilidad y costes.

## Entradas

Obligatorios dataset JSON mensual, ventanas base equivalentes y nuevo directorio. Opcionales umbrales/brief/pruebas. Mantener ausentes/assetType/metricKind; no repartir años/trimestres en meses iguales.

## Salidas

dashboard.html, analysis.json, opportunities.json, report.md, qa.json y research-review.md escrito aparte. Candidatos y PASS aritmético no prueban demanda, compatibilidad ni ROI.

## Procedimiento

1. Fijar pregunta/mercados/unidades/permisos
2. ID estables y separación CY/MY, ventas/parque, tipos y minorista/mayorista/entregas/altas nuevas
3. validar/generar
4. conciliar subidas/bajadas/base cero/ausentes en cohortes completas iguales
5. revisar hipótesis con prueba/ensayo mínimo/parada
6. comprobar filtros/detalles/exportación en escritorio/móvil.

## Límites y condiciones de parada

Sin compra de datos ni publicación automática. Caso UTV:124 entradas,105 fuentes, cohortes históricas calculables US63/CA15/MX1; VIO total desconocido. Escenarios no son ventas observadas, intervalos de confianza ni límites inferiores. Canales ATV estudiados pero ATV fuera del dataset UTV; refinamiento de años/imágenes pendiente.

## Ejemplo de solicitud

Usa `$vehicle-sales-opportunity` — Comparar enero–junio de EE.UU./Canadá/México con los mismos meses anteriores; +30% de ventas no demuestra +30% de demanda de accesorios; responde en español y conserva pruebas, datos desconocidos y límites de autorización.

## Especificación completa

[Entrada del Skill y referencias detalladas](../../SKILL.md).

Usa el idioma solicitado expresamente; si no se indica, sigue el de la petición. Conserva comandos, identificadores, claves JSON, valores enumerados, unidades y citas originales. Separa traducciones y originales. No deduzcas país, moneda ni jurisdicción por el idioma. Lee las referencias detalladas pertinentes y conserva todos los controles y permisos existentes.

Antes de entregar, concilia entradas, pruebas, valores ausentes, archivos y criterios de finalización originales. Marca como no verificados los pasos no ejecutados; el éxito de un script no valida conclusiones comerciales.

## Cobertura lingüística y validación

Esta guía localizada cubre objetivo, requisitos, entradas, salidas, pasos, ejemplos y límites; no traduce línea por línea todas las referencias. La documentación técnica detallada, los casos históricos, errores de scripts, interfaces de ejemplo e imágenes mantienen su idioma original y pueden explicarse a petición. Se comprueban estructura, enlaces y restricciones esenciales; no se afirma una revisión por hablantes nativos de cada idioma.

