# Data Quality Sentinel

> Supervisa frescura, duplicados y reglas de calidad de datasets críticos.

| Área | Harness | Acceso | Complejidad | Impacto | Conectores |
|---|---|---|---|---|---|
| Datos | Deep | Lectura | 3/5 - Media | 3/5 - Medio | BigQuery, Cloud Logging, Google Sheets |

## Propósito
Interesante para DataOps y gobierno de datos.

**Pregunta de demo:** “¿Qué datasets críticos incumplieron sus SLA de calidad esta semana?”

**Resultado esperado:** Scorecard de calidad, tablas afectadas y tickets propuestos.

**KPI:** Incidentes detectados antes de consumo; SLA.

## Calificación

| Dimensión | Score | Justificación |
|---|---|---|
| Complejidad | 3/5 - Media | Reglas de calidad como SQL de lectura más correlación con logs de pipelines; sin remediación automática. |
| Impacto | 3/5 - Medio | Detecta problemas antes del consumo; valor transversal pero indirecto. |

Rúbrica en [SCORING.md](../../SCORING.md).

## Cómo funciona con Gemini Enterprise y VirtuAI

1. El usuario abre la app de **Datos** en Gemini Enterprise y selecciona *Data Quality Sentinel* (registrado como *Custom agent via A2A*).
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
| Skills | `quality-report`, `anomaly-explain`, `data-contract-check` | `skills/` | Build → Skills → Instructions → Skills |
| Reglas | 10 reglas con capa de enforcement | [harness/rules.md](harness/rules.md) | System prompt - Security - Ask - Classifiers |
| Tools | 4 tools: `get_freshness`, `run_quality_checks`, `query_pipeline_logs`, `draft_issue` | [tools-manifest.yaml](harness/tools/tools-manifest.yaml) | MCP Servers - Build → Tools - canvas |
| Conectores | BigQuery, Cloud Logging, Google Sheets | [mcp-servers.md](harness/tools/mcp-servers.md) | Settings → Workspace settings - MCP Servers |
| Configuración | Modelo, capacidades, memoria, canales, seguridad, publicación, budget | [agent-config.yaml](harness/agent-config.yaml) | Pestañas del agente |
| Knowledge Base | `kb-data-quality` - 3 tipos de documento | [knowledge-base.yaml](harness/knowledge-base.yaml) | Build → Knowledge Base |
| Evaluaciones | `eval-data-quality` - golden + negativos | [eval-dataset.json](harness/evals/eval-dataset.json) | Monitor → Evaluations |
| A2A | Agent Card de referencia | [agent-card.example.json](harness/a2a/agent-card.example.json) | Channels → A2A - Gemini Enterprise → Agents |

## Tools

| Tool | Ruta | Efecto | Ask | Propósito |
|---|---|---|---|---|
| `get_freshness` | MCP predefinido - BigQuery | read | No | Leer última actualización por tabla desde INFORMATION_SCHEMA. |
| `run_quality_checks` | MCP predefinido - BigQuery | compute | No | Ejecutar reglas de calidad (nulos, duplicados, rangos) como SELECT. |
| `query_pipeline_logs` (+) | MCP predefinido - Cloud Logging | read | No | Leer errores de pipelines asociados a las tablas. |
| `draft_issue` | Razonamiento del modelo (sin API) | llm | — | Redactar incidente de calidad propuesto. |

(+) = tool añadida en el kit para cubrir un conector declarado en el HTML. Los nombres de tools MCP son de diseño: confirmar el nombre real en **List tools**.

## Checklist de implementación

- [ ] **Discovery**: owner del proceso, documentos y accesos de prueba (datos sintéticos) — Contratos de datos; Reglas de calidad; SLA de actualización
- [ ] **Modelo**: proveedor Vertex AI habilitado en Settings → Models & providers
- [ ] **Agente**: Agents → New agent - tipo Deep - **Enable versioning** - pegar `AGENTS.md` (o importar el repo por Git)
- [ ] **Skills**: Build → Skills (o import Git) y adjuntar en Instructions → Skills
- [ ] **Conectores**: crear MCP predefinidos / Custom Tools según `harness/tools/` y adjuntarlos en el canvas
- [ ] **KB**: crear `kb-data-quality`, subir documentos aprobados, esperar `completed`
- [ ] **Seguridad**: Ask en escrituras, read-only si aplica, classifiers en shadow mode, budget
- [ ] **Evals**: dataset `eval-data-quality` con tools en Mock; pass-rate ≥ umbral de publicación
- [ ] **A2A**: Channels → A2A activo → Publish → copiar Agent Card y endpoint
- [ ] **Gemini Enterprise**: Agents → Add agents → Custom agent via A2A - OAuth (Client ID/Secret, `/a2a/oauth/authorize`, `/a2a/oauth/token`, scope `a2a:invoke`)
- [ ] **Pruebas E2E**: usuario autorizado, usuario sin permiso, dato faltante, aprobación de escritura
- [ ] **Operar**: Monitor → Conversations, Access log, regresiones por versión

## Archivos

- `AGENTS.md`
- `ARCHITECTURE.md`
- `skills/quality-report/SKILL.md`
- `skills/anomaly-explain/SKILL.md`
- `skills/data-contract-check/SKILL.md`
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
