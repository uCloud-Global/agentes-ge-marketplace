---
name: campaign-attribution
description: El usuario pregunta qué campañas generan resultados u oportunidades.
---

# campaign-attribution

Skill de **Marketing Performance Analyst** (Marketing). Skill principal del agente.

## When to use
El usuario pregunta qué campañas generan resultados u oportunidades.

## Instructions
1. Leer campañas del periodo.
2. Unir métricas por UTM con run_readonly_query.
3. Calcular conversiones y costo por resultado si existe.
4. Explicar con fuentes y límites del modelo de atribución.

## Tools que utiliza
`run_readonly_query`

## Output
Tabla comparativa + modelo de atribución usado + limitaciones

## Guardrails
- Solo consultar datasets y cuentas autorizadas.
- No atribuir causalidad sin diseño analítico; vigilar sesgo de datos.
- Ante falta de datos o permisos, decláralo; no inventes.
- Solo lectura: no modificar sistemas.

## Ejemplo
> ¿Qué campañas generaron más oportunidades calificadas el último mes?

Resultado esperado: Tabla comparativa con conversiones, costos si están disponibles y fuentes.
