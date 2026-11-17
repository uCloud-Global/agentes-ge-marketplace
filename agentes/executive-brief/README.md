# Executive Intelligence

> Sintetiza indicadores, riesgos, clientes clave y decisiones en un briefing verificable para líderes.

| Área | Harness | Acceso | Complejidad | Impacto | Conectores |
|---|---|---|---|---|---|
| Dirección | Deep | Lectura | 2/5 - Baja | 4/5 - Alto | BigQuery, Drive, Gmail |

## Propósito
Una visión ejecutiva unificada para apoyar decisiones estratégicas.

**Pregunta de demo:** “Resume resultados de esta semana, riesgos y decisiones pendientes para comité.”

**Resultado esperado:** Resumen ejecutivo con KPIs, tendencias, riesgos, decisiones y links a fuentes.

**KPI:** Tiempo ahorrado por reporte; % afirmaciones con fuente.

## Calificación

| Dimensión | Score | Justificación |
|---|---|---|
| Complejidad | 2/5 - Baja | Solo lectura sobre 3 MCP predefinidos (BigQuery, Drive, Gmail); sin backend propio. La dificultad está en la trazabilidad de cifras, no en la integración. |
| Impacto | 4/5 - Alto | Pocos usuarios (comité directivo) pero decisiones de alto valor y ahorro semanal de consolidación de reportes. |

Rúbrica en [SCORING.md](../../SCORING.md).

## Cómo funciona con Gemini Enterprise y VirtuAI

1. El usuario abre la app de **Dirección** en Gemini Enterprise y selecciona *Executive Intelligence* (registrado como *Custom agent via A2A*).
2. Gemini Enterprise invoca el endpoint A2A de VirtuAI con el token OAuth del usuario (`a2a:invoke`).
3. VirtuAI valida permisos/presupuesto/guardrails y ejecuta el harness **Deep** con el system prompt de `AGENTS.md`, cargando la skill que corresponda.
4. El agente usa los MCP con el OAuth **de cada usuario**, las Custom Tools (Cloud Run/IAM) y la KB.
5. Opera en solo lectura: no hay efectos en los sistemas.
6. La respuesta vuelve por streaming A2A con fuentes; VirtuAI registra worklog, enmascara datos sensibles y contabiliza uso.

Diagramas completos en [ARCHITECTURE.md](ARCHITECTURE.md).

## Agent Harness Kit

| Componente | Contenido | Archivo | Dónde se configura en VirtuAI |
|---|---|---|---|
| System prompt | Rol, alcance, tools, reglas, aprobación, formato | [AGENTS.md](AGENTS.md) | Agent → Instructions (o import Git) |
| Skills | `executive-report`, `kpi-variance-explainer`, `decision-log-tracker` | `skills/` | Build → Skills → Instructions → Skills |
| Reglas | 11 reglas con capa de enforcement | [harness/rules.md](harness/rules.md) | System prompt - Security - Ask - Classifiers |
| Tools | 4 tools: `get_kpis`, `search_drive`, `search_mail`, `draft_executive_brief` | [tools-manifest.yaml](harness/tools/tools-manifest.yaml) | MCP Servers - Build → Tools - canvas |
| Conectores | BigQuery, Drive, Gmail | [mcp-servers.md](harness/tools/mcp-servers.md) | Settings → Workspace settings - MCP Servers |
| Configuración | Modelo, capacidades, memoria, canales, seguridad, publicación, budget | [agent-config.yaml](harness/agent-config.yaml) | Pestañas del agente |
| Knowledge Base | `kb-executive-brief` - 3 tipos de documento | [knowledge-base.yaml](harness/knowledge-base.yaml) | Build → Knowledge Base |
| Evaluaciones | `eval-executive-brief` - golden + negativos | [eval-dataset.json](harness/evals/eval-dataset.json) | Monitor → Evaluations |
| A2A | Agent Card de referencia | [agent-card.example.json](harness/a2a/agent-card.example.json) | Channels → A2A - Gemini Enterprise → Agents |

## Tools

| Tool | Ruta | Efecto | Ask | Propósito |
|---|---|---|---|---|
| `get_kpis` | MCP predefinido - BigQuery | read | No | Leer KPIs/OKR certificados del periodo desde las vistas de dirección (solo SELECT sobre datasets allowlisted). |
| `search_drive` | MCP predefinido - Google Drive | read | No | Buscar actas ejecutivas y reportes de dirección del periodo con permisos del usuario. |
| `search_mail` (+) | MCP predefinido - Gmail | read | No | Buscar hilos con decisiones pendientes o escalamientos dirigidos al comité. |
| `draft_executive_brief` | Razonamiento del modelo (sin API) | llm | — | Redactar el briefing a partir de evidencia citada; no requiere API externa. |

(+) = tool añadida en el kit para cubrir un conector declarado en el HTML. Los nombres de tools MCP son de diseño: confirmar el nombre real en **List tools**.

## Checklist de implementación

- [ ] **Discovery**: owner del proceso, documentos y accesos de prueba (datos sintéticos) — OKR y KPIs; Actas ejecutivas; Reportes de dirección
- [ ] **Modelo**: proveedor Vertex AI habilitado en Settings → Models & providers
- [ ] **Agente**: Agents → New agent - tipo Deep - **Enable versioning** - pegar `AGENTS.md` (o importar el repo por Git)
- [ ] **Skills**: Build → Skills (o import Git) y adjuntar en Instructions → Skills
- [ ] **Conectores**: crear MCP predefinidos / Custom Tools según `harness/tools/` y adjuntarlos en el canvas
- [ ] **KB**: crear `kb-executive-brief`, subir documentos aprobados, esperar `completed`
- [ ] **Seguridad**: Ask en escrituras, read-only si aplica, classifiers en shadow mode, budget
- [ ] **Evals**: dataset `eval-executive-brief` con tools en Mock; pass-rate ≥ umbral de publicación
- [ ] **A2A**: Channels → A2A activo → Publish → copiar Agent Card y endpoint
- [ ] **Gemini Enterprise**: Agents → Add agents → Custom agent via A2A - OAuth (Client ID/Secret, `/a2a/oauth/authorize`, `/a2a/oauth/token`, scope `a2a:invoke`)
- [ ] **Pruebas E2E**: usuario autorizado, usuario sin permiso, dato faltante, aprobación de escritura
- [ ] **Operar**: Monitor → Conversations, Access log, regresiones por versión

## Archivos

- `AGENTS.md`
- `ARCHITECTURE.md`
- `skills/executive-report/SKILL.md`
- `skills/kpi-variance-explainer/SKILL.md`
- `skills/decision-log-tracker/SKILL.md`
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
