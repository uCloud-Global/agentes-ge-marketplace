---
name: metric-definition-check
description: Ambigüedad en la definición de una métrica.
---

# metric-definition-check

Skill de **Enterprise Data Analyst** (Datos).

## When to use
Ambigüedad en la definición de una métrica.

## Instructions
1. Buscar definición oficial.
2. Si hay varias, preguntar cuál usar.

## Output
Definición citada

## Guardrails
- Cuenta de solo lectura y datasets permitidos.
- Validar esquema, límites de filas, costos y semántica; no usar DML.
- Ante falta de datos o permisos, decláralo; no inventes.
- Solo lectura: no modificar sistemas.
