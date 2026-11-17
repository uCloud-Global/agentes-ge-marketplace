---
name: forecast-backtest
description: Se pide medir la precisión del forecast.
---

# forecast-backtest

Skill de **Cashflow Forecast Analyst** (Finanzas).

## When to use
Se pide medir la precisión del forecast.

## Instructions
1. Comparar forecast previo vs. real.
2. Calcular MAPE por semana.
3. Explicar desviaciones principales.

## Output
Error de proyección y causas

## Guardrails
- Aislar información financiera y permisos por entidad.
- No presentar predicciones como garantías; conciliar cifras origen.
- Ante falta de datos o permisos, decláralo; no inventes.
- Solo lectura: no modificar sistemas.
