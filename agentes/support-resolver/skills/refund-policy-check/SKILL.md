---
name: refund-policy-check
description: El caso involucra cobros, reembolsos o créditos.
---

# refund-policy-check

Skill de **Customer Support Resolver** (Clientes).

## When to use
El caso involucra cobros, reembolsos o créditos.

## Instructions
1. Leer política de devolución vigente.
2. Verificar elegibilidad con datos del ticket.
3. Indicar monto máximo autorizado sin aprobación.
4. Escalar si excede.

## Output
Elegibilidad sí/no + base normativa

## Guardrails
- Validar identidad del cliente y aprobar actualizaciones/envíos.
- Escalar incidentes de alto riesgo, no prometer reembolsos no aprobados.
- Ante falta de datos o permisos, decláralo; no inventes.
- Escrituras solo tras vista previa y aprobación explícita.
