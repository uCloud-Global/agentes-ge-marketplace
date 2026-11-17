# Campaign Launch Copilot

> Planea campañas alineadas al CRM y prepara contenidos y audiencias para revisión.

| Área | Harness | Acceso | Complejidad | Impacto | Conectores |
|---|---|---|---|---|---|
| Marketing | Deep | Escritura con aprobación | 4/5 - Alta | 3/5 - Medio | HubSpot, Drive, Google Sheets, Gmail |

## Propósito
Muestra integración clara entre marketing, contenido y CRM.

**Pregunta de demo:** “Diseña una campaña de reactivación para clientes sin actividad en 90 días.”

**Resultado esperado:** Brief, segmentos, asuntos A/B, borradores y calendario editorial.

**KPI:** Tiempo de preparación; tasa de respuesta.

## Calificación

| Dimensión | Score | Justificación |
|---|---|---|
| Complejidad | 4/5 - Alta | Dos Custom Tools (métricas y programación en plataforma), cumplimiento de consentimiento/opt-out y revisión de claims. |
| Impacto | 3/5 - Medio | Acelera la preparación de campañas de un equipo acotado; efecto indirecto en respuesta y conversión. |

Rúbrica en [SCORING.md](../../SCORING.md).

## Cómo funciona con Gemini Enterprise y VirtuAI

1. El usuario abre la app de **Marketing** en Gemini Enterprise y selecciona *Campaign Launch Copilot* (registrado como *Custom agent via A2A*).
2. Gemini Enterprise invoca el endpoint A2A de VirtuAI con el token OAuth del usuario (`a2a:invoke`).
3. VirtuAI valida permisos/presupuesto/guardrails y ejecuta el harness **Deep** con el system prompt de `AGENTS.md`, cargando la skill que corresponda.
4. El agente usa los MCP con el OAuth **de cada usuario**, las Custom Tools (Cloud Run/IAM) y la KB.
5. Las escrituras pasan a `input-required` y esperan aprobación en Gemini Enterprise.
6. La respuesta vuelve por streaming A2A con fuentes; VirtuAI registra worklog, enmascara datos sensibles y contabiliza uso.

Diagramas completos en [ARCHITECTURE.md](ARCHITECTURE.md).

## Agent Harness Kit

| Componente | Contenido | Archivo | Dónde se configura en VirtuAI |
|---|---|---|---|
| System prompt | Rol, alcance, tools, reglas, aprobación, formato | [AGENTS.md](AGENTS.md) | Agent → Instructions (o import Git) |
| Skills | `campaign-planning`, `copy-variants`, `compliance-check` | `skills/` | Build → Skills → Instructions → Skills |
| Reglas | 11 reglas con capa de enforcement | [harness/rules.md](harness/rules.md) | System prompt - Security - Ask - Classifiers |
| Tools | 5 tools: `get_segments`, `read_campaign_metrics`, `search_brand_assets`, `draft_assets`, `schedule_campaign` | [tools-manifest.yaml](harness/tools/tools-manifest.yaml) | MCP Servers - Build → Tools - canvas |
| Conectores | HubSpot, Drive, Google Sheets, Gmail | [mcp-servers.md](harness/tools/mcp-servers.md) | Settings → Workspace settings - MCP Servers |
| Configuración | Modelo, capacidades, memoria, canales, seguridad, publicación, budget | [agent-config.yaml](harness/agent-config.yaml) | Pestañas del agente |
| Knowledge Base | `kb-campaign-copilot` - 4 tipos de documento | [knowledge-base.yaml](harness/knowledge-base.yaml) | Build → Knowledge Base |
| Evaluaciones | `eval-campaign-copilot` - golden + negativos | [eval-dataset.json](harness/evals/eval-dataset.json) | Monitor → Evaluations |
| A2A | Agent Card de referencia | [agent-card.example.json](harness/a2a/agent-card.example.json) | Channels → A2A - Gemini Enterprise → Agents |

## Tools

| Tool | Ruta | Efecto | Ask | Propósito |
|---|---|---|---|---|
| `get_segments` | MCP predefinido - HubSpot | read | No | Leer listas/segmentos con conteo y criterio de consentimiento. |
| `read_campaign_metrics` | Custom Tool HTTP - Cloud Run (IAM) | read | No | Leer métricas históricas de campañas desde Sheets de marketing (API controlada). |
| `search_brand_assets` (+) | MCP predefinido - Google Drive | read | No | Buscar brandbook, guía editorial y piezas aprobadas. |
| `draft_assets` | Razonamiento del modelo (sin API) | llm | — | Redactar asuntos A/B, cuerpos y copies siguiendo guía editorial. |
| `schedule_campaign` | Custom Tool HTTP - Cloud Run (IAM) | write | Sí | Programar campaña en estado BORRADOR para revisión. Escritura con Ask; nunca publica. |

(+) = tool añadida en el kit para cubrir un conector declarado en el HTML. Los nombres de tools MCP son de diseño: confirmar el nombre real en **List tools**.

## Checklist de implementación

- [ ] **Discovery**: owner del proceso, documentos y accesos de prueba (datos sintéticos) — Brandbook; Plan de campañas; Guía editorial; Segmentación
- [ ] **Modelo**: proveedor Vertex AI habilitado en Settings → Models & providers
- [ ] **Agente**: Agents → New agent - tipo Deep - **Enable versioning** - pegar `AGENTS.md` (o importar el repo por Git)
- [ ] **Skills**: Build → Skills (o import Git) y adjuntar en Instructions → Skills
- [ ] **Conectores**: crear MCP predefinidos / Custom Tools según `harness/tools/` y adjuntarlos en el canvas
- [ ] **KB**: crear `kb-campaign-copilot`, subir documentos aprobados, esperar `completed`
- [ ] **Seguridad**: Ask en escrituras, read-only si aplica, classifiers en shadow mode, budget
- [ ] **Evals**: dataset `eval-campaign-copilot` con tools en Mock; pass-rate ≥ umbral de publicación
- [ ] **A2A**: Channels → A2A activo → Publish → copiar Agent Card y endpoint
- [ ] **Gemini Enterprise**: Agents → Add agents → Custom agent via A2A - OAuth (Client ID/Secret, `/a2a/oauth/authorize`, `/a2a/oauth/token`, scope `a2a:invoke`)
- [ ] **Pruebas E2E**: usuario autorizado, usuario sin permiso, dato faltante, aprobación de escritura
- [ ] **Operar**: Monitor → Conversations, Access log, regresiones por versión

## Archivos

- `AGENTS.md`
- `ARCHITECTURE.md`
- `skills/campaign-planning/SKILL.md`
- `skills/copy-variants/SKILL.md`
- `skills/compliance-check/SKILL.md`
- `harness/agent-config.yaml`
- `harness/rules.md`
- `harness/knowledge-base.yaml`
- `harness/tools/tools-manifest.yaml`
- `harness/tools/mcp-servers.md`
- `harness/tools/custom/read_campaign_metrics.tool.json`
- `harness/tools/custom/schedule_campaign.tool.json`
- `harness/evals/eval-dataset.json`
- `harness/a2a/agent-card.example.json`

## Referencias
- VirtuAI: [https://docs.imvirtuai.com/getting-started/overview/](https://docs.imvirtuai.com/getting-started/overview/) - [Tools](https://docs.imvirtuai.com/guides/tools/) - [Skills](https://docs.imvirtuai.com/build/skills/) - [Deep agents](https://docs.imvirtuai.com/build/deep-agents/) - [A2A](https://docs.imvirtuai.com/channels/a2a/) - [Evaluations](https://docs.imvirtuai.com/build/evaluations/) - [Import/Export](https://docs.imvirtuai.com/build/import-export/)
- Gemini Enterprise: [Registrar agente A2A](https://docs.cloud.google.com/gemini/enterprise/docs/register-and-manage-an-a2a-agent)
