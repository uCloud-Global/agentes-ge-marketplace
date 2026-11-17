# Conectores y servidores MCP - Executive Intelligence

Las integraciones se crean primero en el **workspace** y luego se adjuntan al agente en el **canvas**. Tres rutas: **MCP predefinido** (Google/HubSpot), **MCP remoto custom** (`streamable_http`/`sse`, nunca stdio) y **Custom Tool** HTTP.

| Conector (HTML) | Ruta en VirtuAI | Tools del agente |
|---|---|---|
| BigQuery | MCP predefinido - BigQuery | `get_kpis` |
| Drive | MCP predefinido - Google Drive | `search_drive` |
| Gmail | MCP predefinido - Gmail | `search_mail` |

## BigQuery

1. Prepara datasets/vistas allowlisted; concede roles mínimos (`roles/bigquery.dataViewer` sobre vistas + `roles/bigquery.jobUser`), nunca BigQuery Admin.
2. Configura OAuth Google en Workspace settings: `GOOGLE_MCP_CLIENT_ID`, `GOOGLE_MCP_CLIENT_SECRET`, `GOOGLE_MCP_REDIRECT_URI`.
3. Crea **MCP Servers → Predefined → BigQuery**, revisa scopes y adjúntalo al agente.
4. **List tools**: limita a consulta/esquema; política de solo lectura: datasets permitidos, LIMIT, tope de bytes y timeout.
5. Prueba un SELECT permitido, un dataset ajeno (debe fallar) y un DML/DDL (debe bloquearse).

## Drive

1. Cliente OAuth web en Google Auth Platform con la **redirect URI exacta** de VirtuAI.
2. Configura `GOOGLE_MCP_CLIENT_ID/SECRET/REDIRECT_URI` en Workspace settings.
3. Crea **Predefined → Google Drive**; en **List tools** conserva solo búsqueda/lectura (y creación si el manifiesto lo exige, con Ask).
4. Adjunta al canvas; cada usuario conecta su cuenta Google.
5. Prueba acceso a documento permitido y rechazo a documento restringido a otra área.

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
