---
name: data-contract-check
description: Validar un dataset contra su contrato de datos.
---

# data-contract-check

Skill de **Data Quality Sentinel** (Datos).

## When to use
Validar un dataset contra su contrato de datos.

## Instructions
1. Leer contrato.
2. Verificar esquema, tipos y reglas.

## Output
Cumple / no cumple por cláusula

## Guardrails
- Consulta solo lectura; remediación mediante pipeline aprobado.
- No borrar ni reparar automáticamente datos sin reglas de autorización.
- Ante falta de datos o permisos, decláralo; no inventes.
- Solo lectura: no modificar sistemas.
