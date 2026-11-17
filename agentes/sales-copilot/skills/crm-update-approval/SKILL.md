---
name: crm-update-approval
description: Se requiere modificar un deal, etapa, monto o propiedad en HubSpot.
---

# crm-update-approval

Skill de **Sales CRM Copilot** (Ventas).

## When to use
Se requiere modificar un deal, etapa, monto o propiedad en HubSpot.

## Instructions
1. Mostrar valores actuales vs. propuestos.
2. Pedir aprobación explícita (input-required en A2A).
3. Ejecutar update_deal_stage solo tras aprobación.
4. Confirmar resultado y registrar ID del deal.

## Tools que utiliza
`update_deal_stage`

## Output
Diff antes/después - confirmación - ID de registro

## Guardrails
- Actualizar CRM solo con aprobación y permisos del propietario.
- No modificar deal ni enviar correo sin confirmación y registro.
- Ante falta de datos o permisos, decláralo; no inventes.
- Escrituras solo tras vista previa y aprobación explícita.
