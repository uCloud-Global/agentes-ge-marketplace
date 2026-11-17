---
name: obligation-extractor
description: Se piden obligaciones, fechas o renovaciones de un contrato.
---

# obligation-extractor

Skill de **Contract Review Assistant** (Legal).

## When to use
Se piden obligaciones, fechas o renovaciones de un contrato.

## Instructions
1. Extraer obligaciones por parte.
2. Extraer fechas y preavisos.
3. Listar renovaciones automáticas.

## Output
Tabla obligación - responsable - fecha

## Guardrails
- No firmar ni compartir contratos sin validación legal.
- No sustituir revisión de abogado y evitar conclusiones jurídicas definitivas.
- Ante falta de datos o permisos, decláralo; no inventes.
- Solo lectura: no modificar sistemas.
