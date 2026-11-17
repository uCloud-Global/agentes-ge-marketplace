---
name: forecast-model
description: El usuario pide proyectar flujo de caja o liquidez.
---

# forecast-model

Skill de **Cashflow Forecast Analyst** (Finanzas). Skill principal del agente.

## When to use
El usuario pide proyectar flujo de caja o liquidez.

## Instructions
1. Leer históricos con read_cashflow y conciliar saldos iniciales.
2. Leer AR/AP con get_ar_ap y aplicar patrones de cobro/pago.
3. Calcular escenarios con calculate_scenarios.
4. Explicar supuestos y rango de incertidumbre.
5. Redactar pronóstico con draft_forecast.

## Tools que utiliza
`read_cashflow`, `get_ar_ap`, `calculate_scenarios`, `draft_forecast`

## Output
Tabla semanal (12 semanas) por escenario - supuestos - riesgos - semanas críticas

## Guardrails
- Aislar información financiera y permisos por entidad.
- No presentar predicciones como garantías; conciliar cifras origen.
- Ante falta de datos o permisos, decláralo; no inventes.
- Solo lectura: no modificar sistemas.

## Ejemplo
> Proyecta el flujo de caja de las próximas 12 semanas con escenarios.

Resultado esperado: Pronóstico por semana, rango de incertidumbre y principales riesgos.
