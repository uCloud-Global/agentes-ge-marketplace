# People Policy Advisor

> Responde preguntas sobre políticas internas con referencias, país y vigencia.

| Área | Harness | Acceso | Complejidad | Impacto | Conectores |
|---|---|---|---|---|---|
| Talento | Classic | Lectura | 1/5 - Muy baja | 4/5 - Alto | Drive, Google Docs |

## Propósito
Una solución de bajo riesgo para acelerar el acceso al conocimiento institucional.

**Pregunta de demo:** “¿Cuál es la política de viáticos cuando viajo de Colombia a Chile?”

**Resultado esperado:** Respuesta documentada con política, fecha y ruta de escalamiento.

**KPI:** Reducción de preguntas repetidas; precisión normativa.

## Calificación

| Dimensión | Score | Justificación |
|---|---|---|
| Complejidad | 1/5 - Muy baja | Classic con KB y verificación de versión en Drive; solo lectura y sin backend. |
| Impacto | 4/5 - Alto | Alcance a todos los colaboradores y alto volumen de preguntas repetidas; bajo riesgo y adopción rápida. |

Rúbrica en [SCORING.md](../../SCORING.md).

## Cómo funciona con Gemini Enterprise y VirtuAI

1. El usuario abre la app de **Talento** en Gemini Enterprise y selecciona *People Policy Advisor* (registrado como *Custom agent via A2A*).
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
| Procedimientos | `policy-answer`, `policy-gap-escalation` | `harness/procedures/` | Embebidos en AGENTS.md (Classic no admite skills) |
| Reglas | 11 reglas con capa de enforcement | [harness/rules.md](harness/rules.md) | System prompt - Security - Ask - Classifiers |
| Tools | 2 tools: `search_approved_policy`, `get_policy_version` | [tools-manifest.yaml](harness/tools/tools-manifest.yaml) | MCP Servers - Build → Tools - canvas |
| Conectores | Drive, Google Docs | [mcp-servers.md](harness/tools/mcp-servers.md) | Settings → Workspace settings - MCP Servers |
| Configuración | Modelo, capacidades, memoria, canales, seguridad, publicación, budget | [agent-config.yaml](harness/agent-config.yaml) | Pestañas del agente |
| Knowledge Base | `kb-people-policy` - 5 tipos de documento | [knowledge-base.yaml](harness/knowledge-base.yaml) | Build → Knowledge Base |
| Evaluaciones | `eval-people-policy` - golden + negativos | [eval-dataset.json](harness/evals/eval-dataset.json) | Monitor → Evaluations |
| A2A | Agent Card de referencia | [agent-card.example.json](harness/a2a/agent-card.example.json) | Channels → A2A - Gemini Enterprise → Agents |

## Tools

| Tool | Ruta | Efecto | Ask | Propósito |
|---|---|---|---|---|
| `search_approved_policy` | Knowledge Base de VirtuAI (RAG) | read | — | Buscar el fragmento exacto de política aprobada por país y vigencia. |
| `get_policy_version` | MCP predefinido - Google Drive | read | No | Verificar versión y fecha de vigencia del documento fuente en Drive. |

(+) = tool añadida en el kit para cubrir un conector declarado en el HTML. Los nombres de tools MCP son de diseño: confirmar el nombre real en **List tools**.

## Checklist de implementación

- [ ] **Discovery**: owner del proceso, documentos y accesos de prueba (datos sintéticos) — Reglamento interno; Vacaciones; Viáticos; Beneficios; Políticas por país
- [ ] **Modelo**: proveedor Vertex AI habilitado en Settings → Models & providers
- [ ] **Agente**: Agents → New agent - tipo Classic - **Enable versioning** - pegar `AGENTS.md` (o importar el repo por Git)
- [ ] **Procedimientos**: ya incluidos en AGENTS.md
- [ ] **Conectores**: crear MCP predefinidos / Custom Tools según `harness/tools/` y adjuntarlos en el canvas
- [ ] **KB**: crear `kb-people-policy`, subir documentos aprobados, esperar `completed`
- [ ] **Seguridad**: Ask en escrituras, read-only si aplica, classifiers en shadow mode, budget
- [ ] **Evals**: dataset `eval-people-policy` con tools en Mock; pass-rate ≥ umbral de publicación
- [ ] **A2A**: Channels → A2A activo → Publish → copiar Agent Card y endpoint
- [ ] **Gemini Enterprise**: Agents → Add agents → Custom agent via A2A - OAuth (Client ID/Secret, `/a2a/oauth/authorize`, `/a2a/oauth/token`, scope `a2a:invoke`)
- [ ] **Pruebas E2E**: usuario autorizado, usuario sin permiso, dato faltante, aprobación de escritura
- [ ] **Operar**: Monitor → Conversations, Access log, regresiones por versión

## Archivos

- `AGENTS.md`
- `ARCHITECTURE.md`
- `harness/procedures/policy-answer.md`
- `harness/procedures/policy-gap-escalation.md`
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
