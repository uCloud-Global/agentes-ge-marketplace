# Marketing Performance Analyst

> Atribuye resultados y explica variaciones de campañas utilizando CRM y métricas de rendimiento.

| Área | Harness | Acceso | Complejidad | Impacto | Conectores |
|---|---|---|---|---|---|
| Marketing | Classic | Lectura | 2/5 - Baja | 3/5 - Medio | HubSpot, BigQuery, Google Sheets |

## Propósito
Análisis práctico basado en indicadores y fuentes empresariales autorizadas.

**Pregunta de demo:** “¿Qué campañas generaron más oportunidades calificadas el último mes?”

**Resultado esperado:** Tabla comparativa con conversiones, costos si están disponibles y fuentes.

**KPI:** Tiempo de reporting; adopción de insights.

## Calificación

| Dimensión | Score | Justificación |
|---|---|---|
| Complejidad | 2/5 - Baja | Classic de solo lectura con HubSpot y SQL acotado en BigQuery; sin backend. |
| Impacto | 3/5 - Medio | Reduce tiempo de reporting de marketing; valor analítico para un equipo. |

Rúbrica en [SCORING.md](../../SCORING.md).

## Cómo funciona con Gemini Enterprise y VirtuAI

1. El usuario abre la app de **Marketing** en Gemini Enterprise y selecciona *Marketing Performance Analyst* (registrado como *Custom agent via A2A*).
2. Gemini Enterprise invoca el endpoint A2A de VirtuAI con el token OAuth del usuario (`a2a:invoke`).
3. VirtuAI valida permisos/presupuesto/guardrails y ejecuta el harness **Classic** con el system prompt de `AGENTS.md`.
4. El agente usa los MCP con el OAuth **de cada usuario**, las Custom Tools (Cloud Run/IAM) y la KB.
5. Opera en solo lectura: no hay efectos en los sistemas.
6. La respuesta vuelve por streaming A2A con fuentes; VirtuAI registra worklog, enmascara datos sensibles y contabiliza uso.

Diagramas completos en [ARCHITECTURE.md](ARCHITECTURE.md).

## Agent Harness Kit

| Componente | Contenido | Archivo | Dónde se configura en VirtuAI |
|---|---|---|---|
| System prompt | Rol, alcance, tools, reglas, aprobación, formato | [AGENTS.md](AGENTS.md) | Agent → Instructions (o import Git) |
| Procedimientos | `campaign-attribution`, `metric-variance` | `harness/procedures/` | Embebidos en AGENTS.md (Classic no admite skills) |
| Reglas | 10 reglas con capa de enforcement | [harness/rules.md](harness/rules.md) | System prompt - Security - Ask - Classifiers |
| Tools | 3 tools: `get_campaigns`, `run_readonly_query`, `draft_insights` | [tools-manifest.yaml](harness/tools/tools-manifest.yaml) | MCP Servers - Build → Tools - canvas |
| Conectores | HubSpot, BigQuery, Google Sheets | [mcp-servers.md](harness/tools/mcp-servers.md) | Settings → Workspace settings - MCP Servers |
| Configuración | Modelo, capacidades, memoria, canales, seguridad, publicación, budget | [agent-config.yaml](harness/agent-config.yaml) | Pestañas del agente |
| Knowledge Base | `kb-marketing-analytics` - 3 tipos de documento | [knowledge-base.yaml](harness/knowledge-base.yaml) | Build → Knowledge Base |
| Evaluaciones | `eval-marketing-analytics` - golden + negativos | [eval-dataset.json](harness/evals/eval-dataset.json) | Monitor → Evaluations |
| A2A | Agent Card de referencia | [agent-card.example.json](harness/a2a/agent-card.example.json) | Channels → A2A - Gemini Enterprise → Agents |

## Tools

| Tool | Ruta | Efecto | Ask | Propósito |
|---|---|---|---|---|
| `get_campaigns` | MCP predefinido - HubSpot | read | No | Leer campañas, fuentes y oportunidades asociadas. |
| `run_readonly_query` | MCP predefinido - BigQuery | read | No | Ejecutar SELECT sobre datasets de marketing allowlisted con límite de filas. |
| `draft_insights` | Razonamiento del modelo (sin API) | llm | — | Redactar insights y explicación de variaciones. |

(+) = tool añadida en el kit para cubrir un conector declarado en el HTML. Los nombres de tools MCP son de diseño: confirmar el nombre real en **List tools**.

## Checklist de implementación

- [ ] **Discovery**: owner del proceso, documentos y accesos de prueba (datos sintéticos) — Definición de métricas; UTM standards; Objetivos de campañas
- [ ] **Modelo**: proveedor Vertex AI habilitado en Settings → Models & providers
- [ ] **Agente**: Agents → New agent - tipo Classic - **Enable versioning** - pegar `AGENTS.md` (o importar el repo por Git)
- [ ] **Procedimientos**: ya incluidos en AGENTS.md
- [ ] **Conectores**: crear MCP predefinidos / Custom Tools según `harness/tools/` y adjuntarlos en el canvas
- [ ] **KB**: crear `kb-marketing-analytics`, subir documentos aprobados, esperar `completed`
- [ ] **Seguridad**: Ask en escrituras, read-only si aplica, classifiers en shadow mode, budget
- [ ] **Evals**: dataset `eval-marketing-analytics` con tools en Mock; pass-rate ≥ umbral de publicación
- [ ] **A2A**: Channels → A2A activo → Publish → copiar Agent Card y endpoint
- [ ] **Gemini Enterprise**: Agents → Add agents → Custom agent via A2A - OAuth (Client ID/Secret, `/a2a/oauth/authorize`, `/a2a/oauth/token`, scope `a2a:invoke`)
- [ ] **Pruebas E2E**: usuario autorizado, usuario sin permiso, dato faltante, aprobación de escritura
- [ ] **Operar**: Monitor → Conversations, Access log, regresiones por versión

## Archivos

- `AGENTS.md`
- `ARCHITECTURE.md`
- `harness/procedures/campaign-attribution.md`
- `harness/procedures/metric-variance.md`
- `harness/agent-config.yaml`
- `harness/rules.md`
- `harness/knowledge-base.yaml`
- `harness/tools/tools-manifest.yaml`
- `harness/tools/mcp-servers.md`
- `harness/evals/eval-dataset.json`
- `harness/a2a/agent-card.example.json`

## Referencias
- VirtuAI: [https://docs.imvirtuai.com/getting-started/overview/](https://docs.imvirtuai.com/getting-started/overview/) - [Tools](https://docs.imvirtuai.com/guides/tools/) - [Skills](https://docs.imvirtuai.com/build/skills/) - [Deep agents](https://docs.imvirtuai.com/build/deep-agents/) - [A2A](https://docs.imvirtuai.com/channels/a2a/) - [Evaluations](https://docs.imvirtuai.com/build/evaluations/) - [Import/Export](https://docs.imvirtuai.com/build/import-export/)
- Gemini Enterprise: [Registrar agente A2A](https://docs.cloud.google.com/gemini/enterprise/docs/register-and-manage-an-a2a-agent)
