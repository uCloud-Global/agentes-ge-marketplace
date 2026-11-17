# Cashflow Forecast Analyst

> Genera proyecciones de caja con datos operativos, escenarios y supuestos explícitos.

| Área | Harness | Acceso | Complejidad | Impacto | Conectores |
|---|---|---|---|---|---|
| Finanzas | Deep | Lectura | 4/5 - Alta | 4/5 - Alto | BigQuery, Google Sheets, Drive |

## Propósito
Demo útil para CFO y planeación.

**Pregunta de demo:** “Proyecta el flujo de caja de las próximas 12 semanas con escenarios.”

**Resultado esperado:** Pronóstico por semana, rango de incertidumbre y principales riesgos.

**KPI:** Tiempo de forecast; error de proyección.

## Calificación

| Dimensión | Score | Justificación |
|---|---|---|
| Complejidad | 4/5 - Alta | Modelado de escenarios en Workstation con conciliación de saldos, aislamiento por entidad y exigencia alta de exactitud. |
| Impacto | 4/5 - Alto | Decisiones de liquidez de alto valor para Finanzas; frecuencia semanal y pocos usuarios. |

Rúbrica en [SCORING.md](../../SCORING.md).

## Cómo funciona con Gemini Enterprise y VirtuAI

1. El usuario abre la app de **Finanzas** en Gemini Enterprise y selecciona *Cashflow Forecast Analyst* (registrado como *Custom agent via A2A*).
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
| Skills | `forecast-model`, `liquidity-alert`, `forecast-backtest` | `skills/` | Build → Skills → Instructions → Skills |
| Reglas | 11 reglas con capa de enforcement | [harness/rules.md](harness/rules.md) | System prompt - Security - Ask - Classifiers |
| Tools | 4 tools: `read_cashflow`, `get_ar_ap`, `calculate_scenarios`, `draft_forecast` | [tools-manifest.yaml](harness/tools/tools-manifest.yaml) | MCP Servers - Build → Tools - canvas |
| Conectores | BigQuery, Google Sheets, Drive | [mcp-servers.md](harness/tools/mcp-servers.md) | Settings → Workspace settings - MCP Servers |
| Configuración | Modelo, capacidades, memoria, canales, seguridad, publicación, budget | [agent-config.yaml](harness/agent-config.yaml) | Pestañas del agente |
| Knowledge Base | `kb-cashflow-analyst` - 3 tipos de documento | [knowledge-base.yaml](harness/knowledge-base.yaml) | Build → Knowledge Base |
| Evaluaciones | `eval-cashflow-analyst` - golden + negativos | [eval-dataset.json](harness/evals/eval-dataset.json) | Monitor → Evaluations |
| A2A | Agent Card de referencia | [agent-card.example.json](harness/a2a/agent-card.example.json) | Channels → A2A - Gemini Enterprise → Agents |

## Tools

| Tool | Ruta | Efecto | Ask | Propósito |
|---|---|---|---|---|
| `read_cashflow` | MCP predefinido - BigQuery | read | No | Leer históricos de caja por cuenta y entidad. |
| `get_ar_ap` | MCP predefinido - BigQuery | read | No | Leer cartera (AR) y cuentas por pagar (AP) con vencimientos. |
| `calculate_scenarios` | Deep Agent - Workstation / sandbox (Python) | compute | Sí | Proyectar 12 semanas en Python (pandas) con escenarios base/optimista/pesimista. |
| `draft_forecast` | Razonamiento del modelo (sin API) | llm | — | Redactar el informe de pronóstico con supuestos explícitos. |

(+) = tool añadida en el kit para cubrir un conector declarado en el HTML. Los nombres de tools MCP son de diseño: confirmar el nombre real en **List tools**.

## Checklist de implementación

- [ ] **Discovery**: owner del proceso, documentos y accesos de prueba (datos sintéticos) — Políticas financieras; Plan presupuestal; Supuestos de forecasting
- [ ] **Modelo**: proveedor Vertex AI habilitado en Settings → Models & providers
- [ ] **Agente**: Agents → New agent - tipo Deep - **Enable versioning** - pegar `AGENTS.md` (o importar el repo por Git)
- [ ] **Skills**: Build → Skills (o import Git) y adjuntar en Instructions → Skills
- [ ] **Conectores**: crear MCP predefinidos / Custom Tools según `harness/tools/` y adjuntarlos en el canvas
- [ ] **KB**: crear `kb-cashflow-analyst`, subir documentos aprobados, esperar `completed`
- [ ] **Seguridad**: Ask en escrituras, read-only si aplica, classifiers en shadow mode, budget
- [ ] **Evals**: dataset `eval-cashflow-analyst` con tools en Mock; pass-rate ≥ umbral de publicación
- [ ] **A2A**: Channels → A2A activo → Publish → copiar Agent Card y endpoint
- [ ] **Gemini Enterprise**: Agents → Add agents → Custom agent via A2A - OAuth (Client ID/Secret, `/a2a/oauth/authorize`, `/a2a/oauth/token`, scope `a2a:invoke`)
- [ ] **Pruebas E2E**: usuario autorizado, usuario sin permiso, dato faltante, aprobación de escritura
- [ ] **Operar**: Monitor → Conversations, Access log, regresiones por versión

## Archivos

- `AGENTS.md`
- `ARCHITECTURE.md`
- `skills/forecast-model/SKILL.md`
- `skills/liquidity-alert/SKILL.md`
- `skills/forecast-backtest/SKILL.md`
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
