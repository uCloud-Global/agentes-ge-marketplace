# Conectores y servidores MCP - Data Quality Sentinel

Las integraciones se crean primero en el **workspace** y luego se adjuntan al agente en el **canvas**. Tres rutas: **MCP predefinido** (Google/HubSpot), **MCP remoto custom** (`streamable_http`/`sse`, nunca stdio) y **Custom Tool** HTTP.

| Conector (HTML) | Ruta en VirtuAI | Tools del agente |
|---|---|---|
| BigQuery | MCP predefinido - BigQuery | `get_freshness`, `run_quality_checks` |
| Cloud Logging | MCP predefinido - Cloud Logging | `query_pipeline_logs` |
| Google Sheets | Custom Tool HTTP - Cloud Run (IAM) | — (vía KB / Drive) |

## BigQuery

1. Prepara datasets/vistas allowlisted; concede roles mínimos (`roles/bigquery.dataViewer` sobre vistas + `roles/bigquery.jobUser`), nunca BigQuery Admin.
2. Configura OAuth Google en Workspace settings: `GOOGLE_MCP_CLIENT_ID`, `GOOGLE_MCP_CLIENT_SECRET`, `GOOGLE_MCP_REDIRECT_URI`.
3. Crea **MCP Servers → Predefined → BigQuery**, revisa scopes y adjúntalo al agente.
4. **List tools**: limita a consulta/esquema; política de solo lectura: datasets permitidos, LIMIT, tope de bytes y timeout.
5. Prueba un SELECT permitido, un dataset ajeno (debe fallar) y un DML/DDL (debe bloquearse).

## Cloud Logging

1. Habilita Logging API; `roles/logging.viewer` (no `privateLogViewer` salvo necesidad) y exclusiones de PII.
2. Crea **Predefined → Cloud Logging** con OAuth por usuario; solo tools de consulta.
3. Prueba lectura permitida y rechazo a recursos restringidos.

## Google Sheets

1. VirtuAI no lista un MCP predefinido de Google Sheets.
2. Lecturas no sensibles: documento aprobado en la KB. Lectura/escritura en vivo: **Custom Tool** a Cloud Run (Sheets API) con hoja/rango allowlisted.
3. Escrituras con **Ask before each call** e idempotencia (`request_id`).

## Ejemplo de MCP remoto custom (si se usa en lugar de Custom Tool)

```json
{ "transport": "streamable_http", "url": "https://mcp.tu-dominio.com/mcp", "headers": { "Authorization": "Bearer <set-me>" }, "timeout": 30 }
```

Fuente: https://docs.imvirtuai.com/guides/tools/
