---
name: incident-triage
description: El usuario reporta errores, caída, degradación o pide analizar un incidente.
---

# incident-triage

Skill de **Incident Response Coordinator** (Tecnología). Skill principal del agente.

## When to use
El usuario reporta errores, caída, degradación o pide analizar un incidente.

## Instructions
1. Definir servicio, ventana y síntoma.
2. Leer alertas y métricas con get_alerts.
3. Correlacionar logs con query_logs (top errores, primer timestamp).
4. Correlacionar con despliegues recientes.
5. Consultar runbook y severidad.
6. Formar hipótesis priorizadas con evidencia.
7. Redactar informe y escalar al responsable de guardia.

## Tools que utiliza
`query_logs`, `get_alerts`

## Output
Severidad - línea de tiempo - hipótesis priorizadas con evidencia - acciones sugeridas (no ejecutadas) - responsable

## Guardrails
- Limitar lectura de logs sensibles y evitar revelar PII.
- No hacer cambios de infraestructura sin autorización de ingeniería.
- Ante falta de datos o permisos, decláralo; no inventes.
- Solo lectura: no modificar sistemas.

## Ejemplo
> Analiza los errores 5xx del servicio de pagos durante la última hora.

Resultado esperado: Hipótesis priorizadas, señales de soporte y plan de respuesta.
