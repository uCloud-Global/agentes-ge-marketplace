---
name: strategic-radar
description: El usuario pide identificar, priorizar o actualizar oportunidades estratégicas o señales de mercado.
---

# strategic-radar

Skill de **Strategic Opportunity Radar** (Dirección). Skill principal del agente.

## When to use
El usuario pide identificar, priorizar o actualizar oportunidades estratégicas o señales de mercado.

## Instructions
1. Leer prioridades y objetivos vigentes con search_knowledge.
2. Consultar métricas internas con get_strategy_metrics.
3. Buscar señales externas con web search y validar cada una con al menos una fuente fechada.
4. Contrastar señales vs. prioridades: encaje, impacto, esfuerzo y dependencias.
5. Priorizar con matriz impacto/esfuerzo y declarar supuestos.
6. Presentar hallazgos separando hechos, hipótesis y estimaciones.

## Tools que utiliza
`search_knowledge`, `get_strategy_metrics`

## Output
Matriz oportunidad - impacto - esfuerzo - evidencia - supuestos - dependencias

## Guardrails
- Fuentes externas deben validarse; no prometer resultados.
- Debe separar hechos, hipótesis y estimaciones; comprobar trazabilidad.
- Ante falta de datos o permisos, decláralo; no inventes.
- Solo lectura: no modificar sistemas.

## Ejemplo
> ¿Qué oportunidades estratégicas emergieron este trimestre y cuáles priorizamos?

Resultado esperado: Matriz oportunidad-impacto-evidencia, dependencias y supuestos.
