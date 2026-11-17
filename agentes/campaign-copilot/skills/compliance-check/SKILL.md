---
name: compliance-check
description: Antes de programar o cuando se pide revisar una pieza.
---

# compliance-check

Skill de **Campaign Launch Copilot** (Marketing).

## When to use
Antes de programar o cuando se pide revisar una pieza.

## Instructions
1. Verificar opt-in del segmento.
2. Verificar enlace de baja y remitente.
3. Detectar claims sin respaldo.
4. Bloquear si falla un control.

## Output
Checklist pass/fail por control

## Guardrails
- No publicar ni enviar campañas automáticamente.
- Cumplimiento de consentimiento y opt-out, evitar segmentos sin autorización.
- Ante falta de datos o permisos, decláralo; no inventes.
- Escrituras solo tras vista previa y aprobación explícita.
