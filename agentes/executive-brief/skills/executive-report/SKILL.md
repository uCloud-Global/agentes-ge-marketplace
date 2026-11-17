---
name: executive-report
description: El usuario pide un resumen ejecutivo, briefing semanal/mensual o preparación de comité con KPIs, riesgos y decisiones.
---

# executive-report

Skill de **Executive Intelligence** (Dirección). Skill principal del agente.

## When to use
El usuario pide un resumen ejecutivo, briefing semanal/mensual o preparación de comité con KPIs, riesgos y decisiones.

## Instructions
1. Confirmar periodo, unidad de negocio y audiencia del briefing.
2. Consultar KPIs con get_kpis y registrar fecha de corte de cada métrica.
3. Buscar actas y reportes del periodo con search_drive; extraer decisiones y compromisos.
4. Cruzar variaciones de KPIs con decisiones y riesgos documentados.
5. Redactar el briefing con draft_executive_brief citando fuente por cada cifra.
6. Revisar que ninguna cifra quede sin fuente; marcar las faltantes como "sin dato".

## Tools que utiliza
`get_kpis`, `search_drive`, `draft_executive_brief`

## Output
Resumen (5 bullets) - Tabla KPI (valor, meta, variación, corte, fuente) - Riesgos - Decisiones pendientes - Fuentes

## Guardrails
- No revelar indicadores fuera del rol del solicitante.
- Cuando no haya datos actualizados debe indicarlo; validar que ninguna cifra se invente.
- Ante falta de datos o permisos, decláralo; no inventes.
- Solo lectura: no modificar sistemas.

## Ejemplo
> Resume resultados de esta semana, riesgos y decisiones pendientes para comité.

Resultado esperado: Resumen ejecutivo con KPIs, tendencias, riesgos, decisiones y links a fuentes.
