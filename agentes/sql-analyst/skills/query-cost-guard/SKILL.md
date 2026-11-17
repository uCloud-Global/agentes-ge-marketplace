---
name: query-cost-guard
description: La consulta procesa muchos datos.
---

# query-cost-guard

Skill de **Enterprise Data Analyst** (Datos).

## When to use
La consulta procesa muchos datos.

## Instructions
1. Revisar bytes del dry-run vs. tope.
2. Proponer particiones/filtros.
3. No ejecutar si excede.

## Output
Consulta optimizada o rechazo

## Guardrails
- Cuenta de solo lectura y datasets permitidos.
- Validar esquema, límites de filas, costos y semántica; no usar DML.
- Ante falta de datos o permisos, decláralo; no inventes.
- Solo lectura: no modificar sistemas.
