---
name: orphan-account-check
description: Buscar cuentas huérfanas o inactivas.
---

# orphan-account-check

Skill de **Access Governance Analyst** (Seguridad).

## When to use
Buscar cuentas huérfanas o inactivas.

## Instructions
1. Cruzar cuentas vs. directorio activo.
2. Detectar inactividad > 90 días.

## Output
Lista de cuentas candidatas a revisión

## Guardrails
- Requerir controles de identidad y validación del owner.
- No eliminar permisos automáticamente ni exponer secretos.
- Ante falta de datos o permisos, decláralo; no inventes.
- Solo lectura: no modificar sistemas.
