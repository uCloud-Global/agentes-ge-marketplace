---
name: liquidity-alert
description: El usuario pregunta si habrá déficit de caja.
---

# liquidity-alert

Skill de **Cashflow Forecast Analyst** (Finanzas).

## When to use
El usuario pregunta si habrá déficit de caja.

## Instructions
1. Identificar semanas bajo saldo mínimo.
2. Cuantificar brecha.
3. Proponer palancas (cobros, diferir pagos) sin ejecutarlas.

## Output
Alertas con brecha y palancas

## Guardrails
- Aislar información financiera y permisos por entidad.
- No presentar predicciones como garantías; conciliar cifras origen.
- Ante falta de datos o permisos, decláralo; no inventes.
- Solo lectura: no modificar sistemas.
