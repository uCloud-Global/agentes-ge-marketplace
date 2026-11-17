---
name: kpi-variance-explainer
description: El usuario pregunta por qué cambió un indicador o pide explicar una desviación contra meta.
---

# kpi-variance-explainer

Skill de **Executive Intelligence** (Dirección).

## When to use
El usuario pregunta por qué cambió un indicador o pide explicar una desviación contra meta.

## Instructions
1. Identificar KPI, periodo y comparación (meta, periodo anterior, año anterior).
2. Obtener la serie con get_kpis y calcular variación absoluta y %.
3. Buscar evidencia cualitativa en actas o correos que explique la variación.
4. Separar causas documentadas de hipótesis y declarar nivel de confianza.

## Tools que utiliza
`get_kpis`

## Output
Variación cuantificada - Causas documentadas - Hipótesis (etiquetadas) - Datos faltantes

## Guardrails
- No revelar indicadores fuera del rol del solicitante.
- Cuando no haya datos actualizados debe indicarlo; validar que ninguna cifra se invente.
- Ante falta de datos o permisos, decláralo; no inventes.
- Solo lectura: no modificar sistemas.
