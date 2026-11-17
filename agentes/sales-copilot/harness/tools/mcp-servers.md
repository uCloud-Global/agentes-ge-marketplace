# Conectores y servidores MCP - Sales CRM Copilot

Las integraciones se crean primero en el **workspace** y luego se adjuntan al agente en el **canvas**. Tres rutas: **MCP predefinido** (Google/HubSpot), **MCP remoto custom** (`streamable_http`/`sse`, nunca stdio) y **Custom Tool** HTTP.

| Conector (HTML) | Ruta en VirtuAI | Tools del agente |
|---|---|---|
| HubSpot | MCP predefinido - HubSpot | `search_deals`, `get_contact_timeline`, `update_deal_stage` |
| Gmail | MCP predefinido - Gmail | `draft_followup` |
| Calendar | MCP predefinido - Google Calendar | `list_meetings` |

## HubSpot

1. En **Settings → Workspace settings** añade `HUBSPOT_MCP_CLIENT_ID` y `HUBSPOT_MCP_CLIENT_SECRET` de la app OAuth de HubSpot y registra en HubSpot la redirect URI que indique tu instancia VirtuAI.
2. En **Build → MCP Servers → Create server → Predefined** selecciona **HubSpot**; nombre sin espacios; revisa **Required OAuth Scopes**.
3. **List tools**: deja habilitadas solo las tools del manifiesto; activa **Ask** en escrituras.
4. Adjunta el servidor en el **canvas** del agente. Cada usuario conecta **su** cuenta HubSpot (nunca tokens de admin compartidos).
5. Prueba: el usuario solo ve contactos/deals permitidos por HubSpot; un usuario sin permiso recibe 403.

## Gmail

1. Reutiliza el cliente OAuth Google del workspace (el secret nunca va al prompt).
2. Crea **Predefined → Gmail** con scopes mínimos de lectura y creación de borradores.
3. **List tools**: deshabilita send/delete; los borradores con Ask.
4. Cada usuario conecta su propio buzón.
5. Prueba búsqueda, ausencia de consentimiento y que nunca se envíe un correo.

## Calendar

1. OAuth Google corporativo con scopes mínimos.
2. Crea **Predefined → Google Calendar**; habilita consulta de eventos/disponibilidad.
3. Activa **Ask** para crear/modificar eventos y valida invitados.
4. Adjunta al canvas; conexión por usuario en la primera invocación.
5. Prueba disponibilidad, calendario ajeno (rechazo) y creación pendiente de confirmación.

## Ejemplo de MCP remoto custom (si se usa en lugar de Custom Tool)

```json
{ "transport": "streamable_http", "url": "https://mcp.tu-dominio.com/mcp", "headers": { "Authorization": "Bearer <set-me>" }, "timeout": 30 }
```

Fuente: https://docs.imvirtuai.com/guides/tools/
