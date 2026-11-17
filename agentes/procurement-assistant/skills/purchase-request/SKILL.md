---
name: purchase-request
description: El usuario expresa una necesidad de compra en lenguaje libre.
---

# purchase-request

Skill de **Purchase Request Assistant** (Compras). Skill principal del agente.

## When to use
El usuario expresa una necesidad de compra en lenguaje libre.

## Instructions
1. Entender necesidad, cantidad, fecha requerida y centro de costo.
2. Validar presupuesto con validate_budget.
3. Buscar ítems/proveedores homologados con get_catalog.
4. Construir requisición con draft_purchase_request.
5. Determinar aprobadores según matriz.
6. Pedir confirmación antes de submit_for_approval.

## Tools que utiliza
`get_catalog`, `validate_budget`, `draft_purchase_request`, `submit_for_approval`

## Output
Requisición: ítems, cantidades, proveedor sugerido, costo estimado, centro de costo, aprobadores

## Guardrails
- Verificar límites de gasto y segregación de funciones.
- Nunca comprar o comprometer fondos sin aprobación.
- Ante falta de datos o permisos, decláralo; no inventes.
- Escrituras solo tras vista previa y aprobación explícita.

## Ejemplo
> Necesitamos 12 portátiles para un nuevo equipo: prepara la solicitud de compra.

Resultado esperado: Requisición estructurada, estimación de costo, checklist y aprobaciones.
