---
name: approval-matrix-check
description: Hay que determinar quién aprueba.
---

# approval-matrix-check

Skill de **Purchase Request Assistant** (Compras).

## When to use
Hay que determinar quién aprueba.

## Instructions
1. Leer matriz por monto y categoría.
2. Verificar segregación de funciones (solicitante ≠ aprobador).

## Output
Cadena de aprobación

## Guardrails
- Verificar límites de gasto y segregación de funciones.
- Nunca comprar o comprometer fondos sin aprobación.
- Ante falta de datos o permisos, decláralo; no inventes.
- Escrituras solo tras vista previa y aprobación explícita.
