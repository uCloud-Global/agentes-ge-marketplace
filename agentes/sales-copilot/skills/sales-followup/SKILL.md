---
name: sales-followup
description: El usuario pide preparar seguimientos, próximos pasos o correos para oportunidades.
---

# sales-followup

Skill de **Sales CRM Copilot** (Ventas). Skill principal del agente.

## When to use
El usuario pide preparar seguimientos, próximos pasos o correos para oportunidades.

## Instructions
1. Recuperar deals objetivo con search_deals.
2. Leer timeline con get_contact_timeline y detectar última interacción y compromisos.
3. Proponer siguiente paso concreto por deal (reunión, propuesta, llamada).
4. Crear borradores con draft_followup personalizados con contexto real.
5. Presentar vista previa y pedir aprobación antes de cualquier update_deal_stage.

## Tools que utiliza
`search_deals`, `get_contact_timeline`, `draft_followup`, `update_deal_stage`

## Output
Tabla deal - etapa - riesgo - próximo paso - borrador (enlace) - acción pendiente de aprobación

## Guardrails
- Actualizar CRM solo con aprobación y permisos del propietario.
- No modificar deal ni enviar correo sin confirmación y registro.
- Ante falta de datos o permisos, decláralo; no inventes.
- Escrituras solo tras vista previa y aprobación explícita.

## Ejemplo
> Revisa mis 10 oportunidades en riesgo y prepara seguimientos personalizados.

Resultado esperado: Tabla de deals en riesgo, correos borrador y actividades sugeridas.
