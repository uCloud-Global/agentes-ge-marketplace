---
name: control-audit
description: El usuario pide el estado de controles o evidencias del periodo.
---

# control-audit

Skill de **Compliance Control Monitor** (Legal). Skill principal del agente.

## When to use
El usuario pide el estado de controles o evidencias del periodo.

## Instructions
1. Leer controles con get_controls.
2. Buscar evidencia por control con find_evidence.
3. Clasificar: completa, incompleta, vencida, sin evidencia.
4. Priorizar por criticidad.
5. Preparar remediación y alertas en borrador.

## Tools que utiliza
`get_controls`, `find_evidence`

## Output
Registro de brechas - responsable - criticidad - plan de remediación

## Guardrails
- Sin cerrar controles ni enviar alertas masivas automáticamente.
- Registrar evidencias y no declarar cumplimiento sin validación humana.
- Ante falta de datos o permisos, decláralo; no inventes.
- Escrituras solo tras vista previa y aprobación explícita.

## Ejemplo
> ¿Qué controles de cumplimiento tienen evidencia incompleta este mes?

Resultado esperado: Registro de brechas, responsables y plan de remediación.
