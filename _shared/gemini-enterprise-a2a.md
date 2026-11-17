# Publicar agentes VirtuAI en Gemini Enterprise (A2A)

## Parte A - VirtuAI
1. **Settings → SSO, A2A and CLI → A2A Clients** → crear cliente `Gemini Enterprise` (uno por workspace). Copiar *Client ID*, *Client secret* (se muestra una sola vez), *Token URL* y *Scopes*.
2. En cada agente: **Channels → A2A** activo → **Publish** (con versioning).
3. **Channels → Integration URLs**: copiar
   - Agent Card: `https://<host>/a2a/<agent-id>/.well-known/agent-card.json` (pública)
   - Endpoint JSON-RPC: `https://<host>/a2a/<agent-id>` (Bearer)

| OAuth | Valor |
|---|---|
| Authorization URL | `https://<host>/a2a/oauth/authorize` |
| Token URL | `https://<host>/a2a/oauth/token` |
| Scope | `a2a:invoke` |
| Grant | Authorization Code (+PKCE) - tokens 1 h, refresh 30 días, consentimiento máx. 90 días |

## Parte B - Gemini Enterprise
1. Google Cloud → **Gemini Enterprise** → app del área (p. ej. `ge-comercial`, `ge-talento-confidencial`).
2. **Agents → Add agents → Custom agent via A2A** → pegar el **JSON real** de la Agent Card → *Preview agent details* → *Next*.
3. OAuth: Client ID, Client Secret, Authorization URI, Token URI, scope `a2a:invoke`.
4. Usuarios: licencia + `roles/discoveryengine.agentspaceRestrictedUser` (proyecto) y `roles/discoveryengine.agentspaceUser` solo en la app correspondiente.
5. Primer uso: el usuario consiente VirtuAI (A2A) y luego conecta sus cuentas en cada MCP.

## Aprobaciones
Cuando una tool con *Ask* se invoca, la tarea A2A pasa a `input-required`; la solicitud viaja en `metadata.approval_requests` (extensión `https://imvirtuai.com/a2a/extensions/approvals/v1`). El usuario responde con 1–5 o una palabra (Allow once / chat / 60 min / Always / Deny). Sin respuesta: denegada a los 10 min en canales.

## Mapa app Gemini Enterprise ↔ workspace VirtuAI
| App GE | Workspace VirtuAI | Agentes |
|---|---|---|
| ge-direccion / ge-comercial / ge-operaciones | ge-general | executive-brief, strategy-radar, sales-copilot, lead-qualification, proposal-builder, campaign-copilot, marketing-analytics, support-resolver, customer-health, it-helpdesk, incident-command, sql-analyst, data-quality, pmo-copilot, process-optimizer |
| ge-finanzas-legal | ge-finanzas-legal | invoice-review, cashflow-analyst, expense-auditor, supplier-risk, procurement-assistant, contract-reviewer, compliance-monitor |
| ge-talento-confidencial | ge-talento-confidencial | onboarding-agent, people-policy, talent-selection |
| ge-seguridad | ge-seguridad | access-auditor |

Fuentes: https://docs.imvirtuai.com/channels/a2a/ - https://docs.cloud.google.com/gemini/enterprise/docs/register-and-manage-an-a2a-agent
