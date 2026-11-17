---
name: quality-report
description: El usuario pide el estado de calidad o SLA de datasets.
---

# quality-report

Skill de **Data Quality Sentinel** (Datos). Skill principal del agente.

## When to use
El usuario pide el estado de calidad o SLA de datasets.

## Instructions
1. Seleccionar datasets críticos según contratos de datos.
2. Verificar frescura con get_freshness.
3. Ejecutar reglas con run_quality_checks.
4. Correlacionar con logs de pipeline.
5. Priorizar anomalías por impacto.
6. Preparar incidente con draft_issue.

## Tools que utiliza
`get_freshness`, `run_quality_checks`, `draft_issue`

## Output
Scorecard tabla - regla - resultado - SLA - impacto - incidente propuesto

## Guardrails
- Consulta solo lectura; remediación mediante pipeline aprobado.
- No borrar ni reparar automáticamente datos sin reglas de autorización.
- Ante falta de datos o permisos, decláralo; no inventes.
- Solo lectura: no modificar sistemas.

## Ejemplo
> ¿Qué datasets críticos incumplieron sus SLA de calidad esta semana?

Resultado esperado: Scorecard de calidad, tablas afectadas y tickets propuestos.
