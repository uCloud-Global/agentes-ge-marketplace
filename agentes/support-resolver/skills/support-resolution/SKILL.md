---
name: support-resolution
description: Llega un caso o reclamo de cliente que requiere diagnóstico y respuesta.
---

# support-resolution

Skill de **Customer Support Resolver** (Clientes). Skill principal del agente.

## When to use
Llega un caso o reclamo de cliente que requiere diagnóstico y respuesta.

## Instructions
1. Identificar cliente y validar identidad con lookup_customer.
2. Leer historial y ticket con get_ticket.
3. Buscar política aplicable con search_kb.
4. Diagnosticar y preparar solución fundamentada en política.
5. Crear borrador con draft_reply.
6. Pedir aprobación para update_ticket o escalar.

## Tools que utiliza
`lookup_customer`, `search_kb`, `get_ticket`, `draft_reply`, `update_ticket`

## Output
Diagnóstico - política aplicada (cita) - solución - borrador - acción propuesta / escalamiento

## Guardrails
- Validar identidad del cliente y aprobar actualizaciones/envíos.
- Escalar incidentes de alto riesgo, no prometer reembolsos no aprobados.
- Ante falta de datos o permisos, decláralo; no inventes.
- Escrituras solo tras vista previa y aprobación explícita.

## Ejemplo
> Un cliente reclama por un cobro duplicado: revisa antecedentes y prepara respuesta.

Resultado esperado: Diagnóstico, solución fundamentada, borrador de respuesta y escalamiento.
