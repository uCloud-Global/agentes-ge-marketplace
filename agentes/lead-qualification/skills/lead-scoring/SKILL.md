---
name: lead-scoring
description: El usuario pide clasificar, priorizar o calificar leads entrantes.
---

# lead-scoring

Skill de **Lead Qualification Agent** (Ventas). Skill principal del agente.

## When to use
El usuario pide clasificar, priorizar o calificar leads entrantes.

## Instructions
1. Recuperar leads del periodo y deduplicar con find_contact.
2. Obtener señales con get_lead_signals.
3. Calcular score con score_lead (reglas versionadas, no a criterio del modelo).
4. Explicar score: señales presentes, ausentes y peso.
5. Proponer tareas para leads SQL y pedir aprobación antes de create_sales_task.

## Tools que utiliza
`find_contact`, `get_lead_signals`, `score_lead`, `create_sales_task`

## Output
Ranking - score - categoría MQL/SQL - señales usadas - datos faltantes - tarea propuesta

## Guardrails
- No inferir atributos sensibles ni crear tareas sin aprobación.
- Score debe explicar señales usadas y datos ausentes; evitar discriminación.
- Ante falta de datos o permisos, decláralo; no inventes.
- Escrituras solo tras vista previa y aprobación explícita.

## Ejemplo
> Clasifica los leads entrantes y dime cuáles necesita contactar ventas hoy.

Resultado esperado: Ranking de leads, score explicable y tareas pendientes de aprobación.
