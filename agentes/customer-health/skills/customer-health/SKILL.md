---
name: customer-health
description: El usuario pregunta por clientes en riesgo de churn o salud de la cartera.
---

# customer-health

Skill de **Customer Success Health** (Clientes). Skill principal del agente.

## When to use
El usuario pregunta por clientes en riesgo de churn o salud de la cartera.

## Instructions
1. Leer uso con get_account_usage.
2. Leer historial de soporte con get_support_history.
3. Calcular score con compute_health (fórmula versionada).
4. Explicar señales y nivel de confianza por cuenta.
5. Proponer plan de retención con draft_retention_plan.

## Tools que utiliza
`get_account_usage`, `get_support_history`, `compute_health`, `draft_retention_plan`

## Output
Ranking - score - señales - confianza - plan de acción con responsable y fecha

## Guardrails
- Acceso solo a cartera asignada y datos pertinentes.
- Riesgo debe basarse en evidencia y sin diagnóstico infundado.
- Ante falta de datos o permisos, decláralo; no inventes.
- Solo lectura: no modificar sistemas.

## Ejemplo
> ¿Qué clientes están en riesgo de churn y qué acciones recomendarías?

Resultado esperado: Ranking de cuentas con señales, plan y nivel de confianza.
