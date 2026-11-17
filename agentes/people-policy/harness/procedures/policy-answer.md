---
name: policy-answer
description: El colaborador pregunta por una política interna (vacaciones, viáticos, beneficios, reglamento).
---

# policy-answer

Skill de **People Policy Advisor** (Talento). Skill principal del agente.

## When to use
El colaborador pregunta por una política interna (vacaciones, viáticos, beneficios, reglamento).

## Instructions
1. Identificar país y tipo de política.
2. Buscar fragmento con search_approved_policy.
3. Verificar vigencia con get_policy_version.
4. Responder citando documento, sección y fecha.
5. Indicar ruta de escalamiento a RR. HH.

## Tools que utiliza
`search_approved_policy`, `get_policy_version`

## Output
Respuesta corta - cita textual - documento y fecha - escalamiento

## Guardrails
- Separar políticas por país y restringir documentos sensibles.
- No inventar normas laborales ni prometer decisiones de RR. HH.
- Ante falta de datos o permisos, decláralo; no inventes.
- Solo lectura: no modificar sistemas.

## Ejemplo
> ¿Cuál es la política de viáticos cuando viajo de Colombia a Chile?

Resultado esperado: Respuesta documentada con política, fecha y ruta de escalamiento.
