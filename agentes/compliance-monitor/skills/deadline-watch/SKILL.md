---
name: deadline-watch
description: Se pregunta por vencimientos próximos.
---

# deadline-watch

Skill de **Compliance Control Monitor** (Legal).

## When to use
Se pregunta por vencimientos próximos.

## Instructions
1. Consultar obligaciones de los próximos 30/60/90 días.
2. Cruzar con evidencia existente.

## Output
Calendario de vencimientos con estado

## Guardrails
- Sin cerrar controles ni enviar alertas masivas automáticamente.
- Registrar evidencias y no declarar cumplimiento sin validación humana.
- Ante falta de datos o permisos, decláralo; no inventes.
- Escrituras solo tras vista previa y aprobación explícita.
