---
name: campaign-planning
description: El usuario pide diseñar una campaña, reactivación o lanzamiento.
---

# campaign-planning

Skill de **Campaign Launch Copilot** (Marketing). Skill principal del agente.

## When to use
El usuario pide diseñar una campaña, reactivación o lanzamiento.

## Instructions
1. Definir objetivo, KPI y audiencia.
2. Analizar segmentos con get_segments y validar opt-in.
3. Revisar desempeño histórico con read_campaign_metrics.
4. Redactar piezas con draft_assets alineadas al brandbook.
5. Revisar cumplimiento (consentimiento, opt-out, claims).
6. Proponer calendario y pedir aprobación antes de schedule_campaign.

## Tools que utiliza
`get_segments`, `read_campaign_metrics`, `draft_assets`, `schedule_campaign`

## Output
Brief - segmentos - mensajes A/B - calendario - checklist de cumplimiento

## Guardrails
- No publicar ni enviar campañas automáticamente.
- Cumplimiento de consentimiento y opt-out, evitar segmentos sin autorización.
- Ante falta de datos o permisos, decláralo; no inventes.
- Escrituras solo tras vista previa y aprobación explícita.

## Ejemplo
> Diseña una campaña de reactivación para clientes sin actividad en 90 días.

Resultado esperado: Brief, segmentos, asuntos A/B, borradores y calendario editorial.
