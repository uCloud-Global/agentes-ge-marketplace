# Conectores y servidores MCP - Commercial Proposal Studio

Las integraciones se crean primero en el **workspace** y luego se adjuntan al agente en el **canvas**. Tres rutas: **MCP predefinido** (Google/HubSpot), **MCP remoto custom** (`streamable_http`/`sse`, nunca stdio) y **Custom Tool** HTTP.

| Conector (HTML) | Ruta en VirtuAI | Tools del agente |
|---|---|---|
| HubSpot | MCP predefinido - HubSpot | `get_company` |
| Drive | MCP predefinido - Google Drive | `search_templates` |
| Google Docs | Custom Tool HTTP - Cloud Run (IAM) | `create_doc` |
| BigQuery | MCP predefinido - BigQuery | `get_rate_card` |

## HubSpot

1. En **Settings → Workspace settings** añade `HUBSPOT_MCP_CLIENT_ID` y `HUBSPOT_MCP_CLIENT_SECRET` de la app OAuth de HubSpot y registra en HubSpot la redirect URI que indique tu instancia VirtuAI.
2. En **Build → MCP Servers → Create server → Predefined** selecciona **HubSpot**; nombre sin espacios; revisa **Required OAuth Scopes**.
3. **List tools**: deja habilitadas solo las tools del manifiesto; activa **Ask** en escrituras.
4. Adjunta el servidor en el **canvas** del agente. Cada usuario conecta **su** cuenta HubSpot (nunca tokens de admin compartidos).
5. Prueba: el usuario solo ve contactos/deals permitidos por HubSpot; un usuario sin permiso recibe 403.

## Drive

1. Cliente OAuth web en Google Auth Platform con la **redirect URI exacta** de VirtuAI.
2. Configura `GOOGLE_MCP_CLIENT_ID/SECRET/REDIRECT_URI` en Workspace settings.
3. Crea **Predefined → Google Drive**; en **List tools** conserva solo búsqueda/lectura (y creación si el manifiesto lo exige, con Ask).
4. Adjunta al canvas; cada usuario conecta su cuenta Google.
5. Prueba acceso a documento permitido y rechazo a documento restringido a otra área.

## Google Docs

1. VirtuAI no lista un MCP predefinido de Google Docs: lectura vía Drive MCP.
2. Para crear/editar documentos usa una **Custom Tool** hacia Cloud Run (Docs API) o un **MCP remoto** (`streamable_http`) en **MCP Servers → Custom**.
3. No uses una cuenta privilegiada global; valida permisos en carpeta destino y aprobación de escrituras.

## BigQuery

1. Prepara datasets/vistas allowlisted; concede roles mínimos (`roles/bigquery.dataViewer` sobre vistas + `roles/bigquery.jobUser`), nunca BigQuery Admin.
2. Configura OAuth Google en Workspace settings: `GOOGLE_MCP_CLIENT_ID`, `GOOGLE_MCP_CLIENT_SECRET`, `GOOGLE_MCP_REDIRECT_URI`.
3. Crea **MCP Servers → Predefined → BigQuery**, revisa scopes y adjúntalo al agente.
4. **List tools**: limita a consulta/esquema; política de solo lectura: datasets permitidos, LIMIT, tope de bytes y timeout.
5. Prueba un SELECT permitido, un dataset ajeno (debe fallar) y un DML/DDL (debe bloquearse).

## Ejemplo de MCP remoto custom (si se usa en lugar de Custom Tool)

```json
{ "transport": "streamable_http", "url": "https://mcp.tu-dominio.com/mcp", "headers": { "Authorization": "Bearer <set-me>" }, "timeout": 30 }
```

Fuente: https://docs.imvirtuai.com/guides/tools/
