---
name: lead-routing
description: El usuario pide asignar leads a vendedores.
---

# lead-routing

Skill de **Lead Qualification Agent** (Ventas).

## When to use
El usuario pide asignar leads a vendedores.

## Instructions
1. Leer reglas de asignación (territorio, segmento, carga).
2. Proponer owner por lead con justificación.
3. Solicitar aprobación.
4. Crear tareas aprobadas.

## Output
Tabla lead - owner propuesto - regla aplicada

## Guardrails
- No inferir atributos sensibles ni crear tareas sin aprobación.
- Score debe explicar señales usadas y datos ausentes; evitar discriminación.
- Ante falta de datos o permisos, decláralo; no inventes.
- Escrituras solo tras vista previa y aprobación explícita.
