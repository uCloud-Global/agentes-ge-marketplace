---
name: proposal-writing
description: El usuario pide preparar una propuesta, cotización u oferta de servicios.
---

# proposal-writing

Skill de **Commercial Proposal Studio** (Ventas). Skill principal del agente.

## When to use
El usuario pide preparar una propuesta, cotización u oferta de servicios.

## Instructions
1. Leer contexto del cliente y del deal con get_company.
2. Seleccionar servicios del portafolio que responden a la necesidad.
3. Estimar alcance y obtener precios exclusivamente con get_rate_card.
4. Redactar con draft_proposal usando plantilla y términos estándar.
5. Mostrar vista previa y pedir aprobación antes de create_doc.

## Tools que utiliza
`get_company`, `get_rate_card`, `draft_proposal`, `create_doc`

## Output
Propuesta: contexto, solución, alcance, entregables, cronograma, precio (sujeto a validación), supuestos, términos

## Guardrails
- Ningún envío externo ni descuento sin aprobación.
- No inventar precios ni compromisos; validar tarifas y cláusulas.
- Ante falta de datos o permisos, decláralo; no inventes.
- Escrituras solo tras vista previa y aprobación explícita.

## Ejemplo
> Prepara una propuesta de servicios para la oportunidad ACME en HubSpot.

Resultado esperado: Documento comercial estructurado con supuestos, precio sujeto a validación y entregables.
