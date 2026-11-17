# Lead Qualification Agent

> Enriquece y prioriza leads según ICP, datos CRM y reglas de calificación definidas.

| Área | Harness | Acceso | Complejidad | Impacto | Conectores |
|---|---|---|---|---|---|
| Ventas | Deep | Escritura con aprobación | 3/5 - Media | 4/5 - Alto | HubSpot, BigQuery, Gmail |

## Propósito
Estandariza la calificación y mejora la oportunidad del seguimiento comercial.

**Pregunta de demo:** “Clasifica los leads entrantes y dime cuáles necesita contactar ventas hoy.”

**Resultado esperado:** Ranking de leads, score explicable y tareas pendientes de aprobación.

**KPI:** Tiempo a primer contacto; % leads calificados.

## Calificación

| Dimensión | Score | Justificación |
|---|---|---|
| Complejidad | 3/5 - Media | Requiere Custom Tool de scoring determinístico y versionado, controles anti-sesgo y creación de tareas con aprobación. |
| Impacto | 4/5 - Alto | Reduce el tiempo a primer contacto y mejora la conversión de leads; efecto en ingresos del área comercial. |

Rúbrica en [SCORING.md](../../SCORING.md).

## Cómo funciona con Gemini Enterprise y VirtuAI

1. El usuario abre la app de **Ventas** en Gemini Enterprise y selecciona *Lead Qualification Agent* (registrado como *Custom agent via A2A*).
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
| Skills | `lead-scoring`, `icp-fit-explainer`, `lead-routing` | `skills/` | Build → Skills → Instructions → Skills |
| Reglas | 11 reglas con capa de enforcement | [harness/rules.md](harness/rules.md) | System prompt - Security - Ask - Classifiers |
| Tools | 5 tools: `find_contact`, `get_lead_signals`, `search_mail`, `score_lead`, `create_sales_task` | [tools-manifest.yaml](harness/tools/tools-manifest.yaml) | MCP Servers - Build → Tools - canvas |
| Conectores | HubSpot, BigQuery, Gmail | [mcp-servers.md](harness/tools/mcp-servers.md) | Settings → Workspace settings - MCP Servers |
| Configuración | Modelo, capacidades, memoria, canales, seguridad, publicación, budget | [agent-config.yaml](harness/agent-config.yaml) | Pestañas del agente |
| Knowledge Base | `kb-lead-qualification` - 3 tipos de documento | [knowledge-base.yaml](harness/knowledge-base.yaml) | Build → Knowledge Base |
| Evaluaciones | `eval-lead-qualification` - golden + negativos | [eval-dataset.json](harness/evals/eval-dataset.json) | Monitor → Evaluations |
| A2A | Agent Card de referencia | [agent-card.example.json](harness/a2a/agent-card.example.json) | Channels → A2A - Gemini Enterprise → Agents |

## Tools

| Tool | Ruta | Efecto | Ask | Propósito |
|---|---|---|---|---|
| `find_contact` | MCP predefinido - HubSpot | read | No | Buscar el contacto/empresa en HubSpot y deduplicar. |
| `get_lead_signals` | MCP predefinido - BigQuery | read | No | Leer señales de comportamiento (visitas, descargas, uso de trial) desde vistas allowlisted. |
| `search_mail` (+) | MCP predefinido - Gmail | read | No | Revisar respuestas del lead a campañas o formularios (solo lectura). |
| `score_lead` | Custom Tool HTTP - Cloud Run (IAM) | compute | No | Calcular score ICP determinístico con reglas MQL/SQL versionadas; devuelve puntaje y señales usadas. |
| `create_sales_task` | MCP predefinido - HubSpot | write | Sí | Crear tarea de seguimiento para el owner. Escritura con Ask. |

(+) = tool añadida en el kit para cubrir un conector declarado en el HTML. Los nombres de tools MCP son de diseño: confirmar el nombre real en **List tools**.

## Checklist de implementación

- [ ] **Discovery**: owner del proceso, documentos y accesos de prueba (datos sintéticos) — ICP; Reglas MQL/SQL; Historial comercial
- [ ] **Modelo**: proveedor Vertex AI habilitado en Settings → Models & providers
- [ ] **Agente**: Agents → New agent - tipo Deep - **Enable versioning** - pegar `AGENTS.md` (o importar el repo por Git)
- [ ] **Skills**: Build → Skills (o import Git) y adjuntar en Instructions → Skills
- [ ] **Conectores**: crear MCP predefinidos / Custom Tools según `harness/tools/` y adjuntarlos en el canvas
- [ ] **KB**: crear `kb-lead-qualification`, subir documentos aprobados, esperar `completed`
- [ ] **Seguridad**: Ask en escrituras, read-only si aplica, classifiers en shadow mode, budget
- [ ] **Evals**: dataset `eval-lead-qualification` con tools en Mock; pass-rate ≥ umbral de publicación
- [ ] **A2A**: Channels → A2A activo → Publish → copiar Agent Card y endpoint
- [ ] **Gemini Enterprise**: Agents → Add agents → Custom agent via A2A - OAuth (Client ID/Secret, `/a2a/oauth/authorize`, `/a2a/oauth/token`, scope `a2a:invoke`)
- [ ] **Pruebas E2E**: usuario autorizado, usuario sin permiso, dato faltante, aprobación de escritura
- [ ] **Operar**: Monitor → Conversations, Access log, regresiones por versión

## Archivos

- `AGENTS.md`
- `ARCHITECTURE.md`
- `skills/lead-scoring/SKILL.md`
- `skills/icp-fit-explainer/SKILL.md`
- `skills/lead-routing/SKILL.md`
- `harness/agent-config.yaml`
- `harness/rules.md`
- `harness/knowledge-base.yaml`
- `harness/tools/tools-manifest.yaml`
- `harness/tools/mcp-servers.md`
- `harness/tools/custom/score_lead.tool.json`
- `harness/evals/eval-dataset.json`
- `harness/a2a/agent-card.example.json`

## Referencias
- VirtuAI: [https://docs.imvirtuai.com/getting-started/overview/](https://docs.imvirtuai.com/getting-started/overview/) - [Tools](https://docs.imvirtuai.com/guides/tools/) - [Skills](https://docs.imvirtuai.com/build/skills/) - [Deep agents](https://docs.imvirtuai.com/build/deep-agents/) - [A2A](https://docs.imvirtuai.com/channels/a2a/) - [Evaluations](https://docs.imvirtuai.com/build/evaluations/) - [Import/Export](https://docs.imvirtuai.com/build/import-export/)
- Gemini Enterprise: [Registrar agente A2A](https://docs.cloud.google.com/gemini/enterprise/docs/register-and-manage-an-a2a-agent)
