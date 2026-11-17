---
name: project-report
description: El usuario pide status semanal, riesgos o estado de proyectos.
---

# project-report

Skill de **Project PMO Copilot** (Operaciones). Skill principal del agente.

## When to use
El usuario pide status semanal, riesgos o estado de proyectos.

## Instructions
1. Reunir estado con read_project_docs y get_milestones.
2. Detectar hitos vencidos o en riesgo.
3. Extraer bloqueos de actas.
4. Semaforizar RAG con criterio explícito.
5. Redactar reporte y borradores de seguimiento.

## Tools que utiliza
`read_project_docs`, `get_milestones`

## Output
Status report: RAG por proyecto - hitos - riesgos - bloqueos - próximos compromisos

## Guardrails
- No enviar reportes o modificar cronogramas sin aprobación.
- No asignar compromisos a personas sin confirmar responsables.
- Ante falta de datos o permisos, decláralo; no inventes.
- Solo lectura: no modificar sistemas.

## Ejemplo
> Prepara el informe semanal de los proyectos y sus principales riesgos.

Resultado esperado: Status report, RAG semaforizado y seguimiento propuesto.
