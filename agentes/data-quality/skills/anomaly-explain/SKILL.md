---
name: anomaly-explain
description: Se detecta un salto o caída inusual en un dataset.
---

# anomaly-explain

Skill de **Data Quality Sentinel** (Datos).

## When to use
Se detecta un salto o caída inusual en un dataset.

## Instructions
1. Comparar volumen vs. histórico.
2. Revisar cambios de esquema.
3. Revisar logs del pipeline.

## Output
Explicación con evidencia

## Guardrails
- Consulta solo lectura; remediación mediante pipeline aprobado.
- No borrar ni reparar automáticamente datos sin reglas de autorización.
- Ante falta de datos o permisos, decláralo; no inventes.
- Solo lectura: no modificar sistemas.
