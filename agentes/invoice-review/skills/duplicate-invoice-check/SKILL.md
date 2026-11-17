---
name: duplicate-invoice-check
description: Se sospecha factura duplicada.
---

# duplicate-invoice-check

Skill de **Accounts Payable Reviewer** (Finanzas).

## When to use
Se sospecha factura duplicada.

## Instructions
1. Buscar mismo proveedor, monto y fecha cercana.
2. Comparar número y CUFE/folio.
3. Reportar coincidencias.

## Output
Lista de posibles duplicados

## Guardrails
- Nunca ejecutar pagos; revisión financiera obligatoria.
- Evitar pagos automáticos y proteger datos bancarios.
- Ante falta de datos o permisos, decláralo; no inventes.
- Escrituras solo tras vista previa y aprobación explícita.
