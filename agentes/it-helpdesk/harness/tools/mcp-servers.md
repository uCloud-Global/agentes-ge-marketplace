# Conectores y servidores MCP - IT Helpdesk Concierge

Las integraciones se crean primero en el **workspace** y luego se adjuntan al agente en el **canvas**. Tres rutas: **MCP predefinido** (Google/HubSpot), **MCP remoto custom** (`streamable_http`/`sse`, nunca stdio) y **Custom Tool** HTTP.

| Conector (HTML) | Ruta en VirtuAI | Tools del agente |
|---|---|---|
| Drive | MCP predefinido - Google Drive | — (vía KB / Drive) |
| Gmail | MCP predefinido - Gmail | — (vía KB / Drive) |
| API / Cloud Run | Custom Tool HTTP - Cloud Run (IAM) | `lookup_asset`, `create_ticket` |

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

## API / Cloud Run

1. Implementa un endpoint HTTPS (p. ej. FastAPI en Cloud Run) que valide entradas y autorización **por registro** en backend.
2. En Workspace settings configura `CLOUD_RUN_SERVICE_ACCOUNT_JSON` y concede `roles/run.invoker` solo sobre ese servicio.
3. **Build → Tools → Add tool** con los valores de `harness/tools/custom/*.tool.json`.
4. Authentication = **Google Cloud Run (IAM / Service Account)**: autentica a VirtuAI, no al usuario final; nunca autorices por un email generado por el LLM.

## Ejemplo de MCP remoto custom (si se usa en lugar de Custom Tool)

```json
{ "transport": "streamable_http", "url": "https://mcp.tu-dominio.com/mcp", "headers": { "Authorization": "Bearer <set-me>" }, "timeout": 30 }
```

Fuente: https://docs.imvirtuai.com/guides/tools/
