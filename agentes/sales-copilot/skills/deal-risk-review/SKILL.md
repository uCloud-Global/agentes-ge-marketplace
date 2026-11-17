---
name: deal-risk-review
description: El usuario pregunta qué oportunidades están en riesgo o pide revisar su pipeline.
---

# deal-risk-review

Skill de **Sales CRM Copilot** (Ventas).

## When to use
El usuario pregunta qué oportunidades están en riesgo o pide revisar su pipeline.

## Instructions
1. Buscar deals abiertos del propietario.
2. Aplicar señales de riesgo del playbook: sin actividad >14 días, fecha de cierre vencida, sin decisor, descuento fuera de política.
3. Ordenar por monto x probabilidad x riesgo.
4. Explicar las señales usadas por deal.

## Output
Ranking de deals en riesgo con señales y evidencia

## Guardrails
- Actualizar CRM solo con aprobación y permisos del propietario.
- No modificar deal ni enviar correo sin confirmación y registro.
- Ante falta de datos o permisos, decláralo; no inventes.
- Escrituras solo tras vista previa y aprobación explícita.
