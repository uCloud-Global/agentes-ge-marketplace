# Conectores y servidores MCP - Incident Response Coordinator

Las integraciones se crean primero en el **workspace** y luego se adjuntan al agente en el **canvas**. Tres rutas: **MCP predefinido** (Google/HubSpot), **MCP remoto custom** (`streamable_http`/`sse`, nunca stdio) y **Custom Tool** HTTP.

| Conector (HTML) | Ruta en VirtuAI | Tools del agente |
|---|---|---|
| Cloud Monitoring | MCP predefinido - Cloud Monitoring | `get_alerts` |
| Cloud Logging | MCP predefinido - Cloud Logging | `query_logs` |
| BigQuery | MCP predefinido - BigQuery | `query_deploys` |
| Gmail | MCP predefinido - Gmail | `draft_incident_report` |

## Cloud Monitoring

1. Habilita Monitoring API; rol `roles/monitoring.viewer` para el usuario.
2. Crea **Predefined → Cloud Monitoring** con OAuth Google por usuario; solo tools de lectura.
3. Prueba límites de proyecto con una cuenta de otro proyecto.

## Cloud Logging

1. Habilita Logging API; `roles/logging.viewer` (no `privateLogViewer` salvo necesidad) y exclusiones de PII.
2. Crea **Predefined → Cloud Logging** con OAuth por usuario; solo tools de consulta.
3. Prueba lectura permitida y rechazo a recursos restringidos.

## BigQuery

1. Prepara datasets/vistas allowlisted; concede roles mínimos (`roles/bigquery.dataViewer` sobre vistas + `roles/bigquery.jobUser`), nunca BigQuery Admin.
2. Configura OAuth Google en Workspace settings: `GOOGLE_MCP_CLIENT_ID`, `GOOGLE_MCP_CLIENT_SECRET`, `GOOGLE_MCP_REDIRECT_URI`.
3. Crea **MCP Servers → Predefined → BigQuery**, revisa scopes y adjúntalo al agente.
4. **List tools**: limita a consulta/esquema; política de solo lectura: datasets permitidos, LIMIT, tope de bytes y timeout.
5. Prueba un SELECT permitido, un dataset ajeno (debe fallar) y un DML/DDL (debe bloquearse).

## Gmail

1. Reutiliza el cliente OAuth Google del workspace (el secret nunca va al prompt).
2. Crea **Predefined → Gmail** con scopes mínimos de lectura y creación de borradores.
3. **List tools**: deshabilita send/delete; los borradores con Ask.
4. Cada usuario conecta su propio buzón.
5. Prueba búsqueda, ausencia de consentimiento y que nunca se envíe un correo.

## Ejemplo de MCP remoto custom (si se usa en lugar de Custom Tool)

```json
{ "transport": "streamable_http", "url": "https://mcp.tu-dominio.com/mcp", "headers": { "Authorization": "Bearer <set-me>" }, "timeout": 30 }
```

Fuente: https://docs.imvirtuai.com/guides/tools/
