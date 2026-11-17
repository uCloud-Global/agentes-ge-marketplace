---
name: invoice-matching
description: El usuario pide revisar facturas recibidas o conciliar contra órdenes de compra.
---

# invoice-matching

Skill de **Accounts Payable Reviewer** (Finanzas). Skill principal del agente.

## When to use
El usuario pide revisar facturas recibidas o conciliar contra órdenes de compra.

## Instructions
1. Localizar facturas del periodo.
2. Extraer campos con extract_invoice.
3. Cruzar contra OC y recepción con match_po (cantidad, precio, impuestos).
4. Validar proveedor con check_vendor.
5. Clasificar: conforme, excepción menor, excepción mayor.
6. Proponer casos de revisión y pedir aprobación antes de create_review_case.

## Tools que utiliza
`extract_invoice`, `match_po`, `check_vendor`, `create_review_case`

## Output
Tabla factura - OC - diferencias (cantidad/precio/impuesto) - severidad - caso propuesto

## Guardrails
- Nunca ejecutar pagos; revisión financiera obligatoria.
- Evitar pagos automáticos y proteger datos bancarios.
- Ante falta de datos o permisos, decláralo; no inventes.
- Escrituras solo tras vista previa y aprobación explícita.

## Ejemplo
> Revisa las facturas recibidas hoy y detecta diferencias frente a sus órdenes.

Resultado esperado: Informe de coincidencias, excepciones y borradores de casos de revisión.
