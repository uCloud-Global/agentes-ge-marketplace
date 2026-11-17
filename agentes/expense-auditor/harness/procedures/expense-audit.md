---
name: expense-audit
description: El usuario pide auditar gastos de un viaje o periodo.
---

# expense-audit

Skill de **Expense Policy Auditor** (Finanzas). Skill principal del agente.

## When to use
El usuario pide auditar gastos de un viaje o periodo.

## Instructions
1. Leer gastos con get_expenses.
2. Identificar política aplicable (país, fecha, moneda) con read_policy.
3. Comparar contra topes y excepciones aprobadas.
4. Listar excepciones con evidencia.

## Tools que utiliza
`get_expenses`, `read_policy`

## Output
Tabla gasto - tope - diferencia - evidencia - excepción aprobada sí/no

## Guardrails
- No bloquear ni rechazar reembolsos automáticamente.
- Tener en cuenta moneda, fecha, país y excepciones aprobadas.
- Ante falta de datos o permisos, decláralo; no inventes.
- Solo lectura: no modificar sistemas.

## Ejemplo
> Audita los gastos del último viaje y marca los que exceden política.

Resultado esperado: Tabla de excepciones y evidencia, sin rechazos automáticos.
