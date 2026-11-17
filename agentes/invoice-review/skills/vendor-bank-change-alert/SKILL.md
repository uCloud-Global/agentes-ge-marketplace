---
name: vendor-bank-change-alert
description: La factura muestra datos bancarios distintos a los registrados.
---

# vendor-bank-change-alert

Skill de **Accounts Payable Reviewer** (Finanzas).

## When to use
La factura muestra datos bancarios distintos a los registrados.

## Instructions
1. Comparar con maestro de proveedor.
2. Marcar alerta de posible fraude.
3. Nunca actualizar datos bancarios.
4. Escalar a tesorería.

## Output
Alerta de fraude con evidencia

## Guardrails
- Nunca ejecutar pagos; revisión financiera obligatoria.
- Evitar pagos automáticos y proteger datos bancarios.
- Ante falta de datos o permisos, decláralo; no inventes.
- Escrituras solo tras vista previa y aprobación explícita.
