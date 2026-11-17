# Employee Onboarding Navigator

> Coordina incorporaciones: checklist, documentos, calendario y solicitudes de acceso.

| Área | Harness | Acceso | Complejidad | Impacto | Conectores |
|---|---|---|---|---|---|
| Talento | Deep | Escritura con aprobación | 4/5 - Alta | 3/5 - Medio | Drive, Gmail, Calendar, API / Cloud Run |

## Propósito
Una experiencia coordinada que conecta talento humano, tecnología y equipos operativos.

**Pregunta de demo:** “Prepara el onboarding de una persona que ingresa el próximo lunes al equipo de datos.”

**Resultado esperado:** Checklist por áreas, eventos propuestos, borradores y tareas de acceso.

**KPI:** Tiempo de incorporación; completitud de checklist.

## Calificación

| Dimensión | Score | Justificación |
|---|---|---|
| Complejidad | 4/5 - Alta | Coordina varias áreas: solicitud de accesos vía ITSM (Custom Tool), eventos de calendario y datos de RR. HH., todo con aprobación. |
| Impacto | 3/5 - Medio | Mejora la experiencia de ingreso; volumen ligado a contrataciones, ahorro moderado por caso. |

Rúbrica en [SCORING.md](../../SCORING.md).

## Cómo funciona con Gemini Enterprise y VirtuAI

1. El usuario abre la app de **Talento** en Gemini Enterprise y selecciona *Employee Onboarding Navigator* (registrado como *Custom agent via A2A*).
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
| Skills | `employee-onboarding`, `access-request-builder`, `first-week-plan` | `skills/` | Build → Skills → Instructions → Skills |
| Reglas | 11 reglas con capa de enforcement | [harness/rules.md](harness/rules.md) | System prompt - Security - Ask - Classifiers |
| Tools | 4 tools: `get_onboarding_plan`, `schedule_welcome`, `draft_welcome_mail`, `request_access` | [tools-manifest.yaml](harness/tools/tools-manifest.yaml) | MCP Servers - Build → Tools - canvas |
| Conectores | Drive, Gmail, Calendar, API / Cloud Run | [mcp-servers.md](harness/tools/mcp-servers.md) | Settings → Workspace settings - MCP Servers |
| Configuración | Modelo, capacidades, memoria, canales, seguridad, publicación, budget | [agent-config.yaml](harness/agent-config.yaml) | Pestañas del agente |
| Knowledge Base | `kb-onboarding-agent` - 4 tipos de documento | [knowledge-base.yaml](harness/knowledge-base.yaml) | Build → Knowledge Base |
| Evaluaciones | `eval-onboarding-agent` - golden + negativos | [eval-dataset.json](harness/evals/eval-dataset.json) | Monitor → Evaluations |
| A2A | Agent Card de referencia | [agent-card.example.json](harness/a2a/agent-card.example.json) | Channels → A2A - Gemini Enterprise → Agents |

## Tools

| Tool | Ruta | Efecto | Ask | Propósito |
|---|---|---|---|---|
| `get_onboarding_plan` | MCP predefinido - Google Drive | read | No | Leer checklist de ingreso y manual de bienvenida por área. |
| `schedule_welcome` | MCP predefinido - Google Calendar | write | Sí | Crear eventos de bienvenida/inducción. Escritura con Ask (validar invitados). |
| `draft_welcome_mail` | MCP predefinido - Gmail | draft | Sí | Crear BORRADOR de correo de bienvenida. |
| `request_access` | Custom Tool HTTP - Cloud Run (IAM) | write | Sí | Crear solicitud de accesos en ITSM (Cloud Run). Escritura con Ask y visto bueno de TI. |

(+) = tool añadida en el kit para cubrir un conector declarado en el HTML. Los nombres de tools MCP son de diseño: confirmar el nombre real en **List tools**.

## Checklist de implementación

- [ ] **Discovery**: owner del proceso, documentos y accesos de prueba (datos sintéticos) — Manual de bienvenida; Checklist de ingreso; Políticas TI; Beneficios
- [ ] **Modelo**: proveedor Vertex AI habilitado en Settings → Models & providers
- [ ] **Agente**: Agents → New agent - tipo Deep - **Enable versioning** - pegar `AGENTS.md` (o importar el repo por Git)
- [ ] **Skills**: Build → Skills (o import Git) y adjuntar en Instructions → Skills
- [ ] **Conectores**: crear MCP predefinidos / Custom Tools según `harness/tools/` y adjuntarlos en el canvas
- [ ] **KB**: crear `kb-onboarding-agent`, subir documentos aprobados, esperar `completed`
- [ ] **Seguridad**: Ask en escrituras, read-only si aplica, classifiers en shadow mode, budget
- [ ] **Evals**: dataset `eval-onboarding-agent` con tools en Mock; pass-rate ≥ umbral de publicación
- [ ] **A2A**: Channels → A2A activo → Publish → copiar Agent Card y endpoint
- [ ] **Gemini Enterprise**: Agents → Add agents → Custom agent via A2A - OAuth (Client ID/Secret, `/a2a/oauth/authorize`, `/a2a/oauth/token`, scope `a2a:invoke`)
- [ ] **Pruebas E2E**: usuario autorizado, usuario sin permiso, dato faltante, aprobación de escritura
- [ ] **Operar**: Monitor → Conversations, Access log, regresiones por versión

## Archivos

- `AGENTS.md`
- `ARCHITECTURE.md`
- `skills/employee-onboarding/SKILL.md`
- `skills/access-request-builder/SKILL.md`
- `skills/first-week-plan/SKILL.md`
- `harness/agent-config.yaml`
- `harness/rules.md`
- `harness/knowledge-base.yaml`
- `harness/tools/tools-manifest.yaml`
- `harness/tools/mcp-servers.md`
- `harness/tools/custom/request_access.tool.json`
- `harness/evals/eval-dataset.json`
- `harness/a2a/agent-card.example.json`

## Referencias
- VirtuAI: [https://docs.imvirtuai.com/getting-started/overview/](https://docs.imvirtuai.com/getting-started/overview/) - [Tools](https://docs.imvirtuai.com/guides/tools/) - [Skills](https://docs.imvirtuai.com/build/skills/) - [Deep agents](https://docs.imvirtuai.com/build/deep-agents/) - [A2A](https://docs.imvirtuai.com/channels/a2a/) - [Evaluations](https://docs.imvirtuai.com/build/evaluations/) - [Import/Export](https://docs.imvirtuai.com/build/import-export/)
- Gemini Enterprise: [Registrar agente A2A](https://docs.cloud.google.com/gemini/enterprise/docs/register-and-manage-an-a2a-agent)
