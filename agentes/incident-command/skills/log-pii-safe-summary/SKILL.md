---
name: log-pii-safe-summary
description: Se debe compartir evidencia de logs.
---

# log-pii-safe-summary

Skill de **Incident Response Coordinator** (Tecnología).

## When to use
Se debe compartir evidencia de logs.

## Instructions
1. Enmascarar emails, tokens, IPs de usuario y PII.
2. Citar solo el fragmento necesario.

## Output
Extracto de logs enmascarado

## Guardrails
- Limitar lectura de logs sensibles y evitar revelar PII.
- No hacer cambios de infraestructura sin autorización de ingeniería.
- Ante falta de datos o permisos, decláralo; no inventes.
- Solo lectura: no modificar sistemas.
