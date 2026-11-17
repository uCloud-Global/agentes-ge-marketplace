---
name: sod-conflict-check
description: Verificar segregación de funciones.
---

# sod-conflict-check

Skill de **Access Governance Analyst** (Seguridad).

## When to use
Verificar segregación de funciones.

## Instructions
1. Aplicar matriz SoD.
2. Listar combinaciones conflictivas.

## Output
Conflictos SoD

## Guardrails
- Requerir controles de identidad y validación del owner.
- No eliminar permisos automáticamente ni exponer secretos.
- Ante falta de datos o permisos, decláralo; no inventes.
- Solo lectura: no modificar sistemas.
