# Conectores y servidores MCP - Supplier Risk Analyst

Las integraciones se crean primero en el **workspace** y luego se adjuntan al agente en el **canvas**. Tres rutas: **MCP predefinido** (Google/HubSpot), **MCP remoto custom** (`streamable_http`/`sse`, nunca stdio) y **Custom Tool** HTTP.

| Conector (HTML) | Ruta en VirtuAI | Tools del agente |
|---|---|---|
| BigQuery | MCP predefinido - BigQuery | `get_supplier_kpis` |
| Drive | MCP predefinido - Google Drive | `search_contract` |
| Google Sheets | Custom Tool HTTP - Cloud Run (IAM) | `score_risk` |
| API / Cloud Run | Custom Tool HTTP - Cloud Run (IAM) | `score_risk` |

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

## Google Sheets

1. VirtuAI no lista un MCP predefinido de Google Sheets.
2. Lecturas no sensibles: documento aprobado en la KB. Lectura/escritura en vivo: **Custom Tool** a Cloud Run (Sheets API) con hoja/rango allowlisted.
3. Escrituras con **Ask before each call** e idempotencia (`request_id`).

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
