---
name: fx-normalization
description: Gastos en varias monedas.
---

# fx-normalization

Skill de **Expense Policy Auditor** (Finanzas).

## When to use
Gastos en varias monedas.

## Instructions
1. Usar tasa de la fecha del gasto según política.
2. Declarar fuente de la tasa.

## Output
Montos normalizados

## Guardrails
- No bloquear ni rechazar reembolsos automáticamente.
- Tener en cuenta moneda, fecha, país y excepciones aprobadas.
- Ante falta de datos o permisos, decláralo; no inventes.
- Solo lectura: no modificar sistemas.
