---
name: process-improvement
description: El usuario pide analizar un proceso, cuellos de botella u oportunidades de automatización.
---

# process-improvement

Skill de **Process Improvement Scout** (Operaciones). Skill principal del agente.

## When to use
El usuario pide analizar un proceso, cuellos de botella u oportunidades de automatización.

## Instructions
1. Seleccionar proceso y alcance.
2. Leer SOP con search_sop.
3. Medir tiempos por etapa con query_cycle_time.
4. Identificar cuellos de botella y retrabajos.
5. Diseñar TO-BE y backlog priorizado.
6. Estimar impacto con supuestos.

## Tools que utiliza
`search_sop`, `query_cycle_time`

## Output
Mapa AS-IS/TO-BE (mermaid) - cuellos de botella con evidencia - backlog priorizado - impacto estimado

## Guardrails
- Cualquier cambio operativo debe ser aprobado por el dueño del proceso.
- Distinguir oportunidades supuestas de evidencia observada.
- Ante falta de datos o permisos, decláralo; no inventes.
- Solo lectura: no modificar sistemas.

## Ejemplo
> Analiza el proceso de aprobación de compras y dónde se pierde tiempo.

Resultado esperado: Mapa AS-IS / TO-BE, cuellos de botella y backlog de automatización.
