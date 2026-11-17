# Commercial Proposal Studio

> Arma propuestas usando contexto de cliente, catálogo de servicios y pricing autorizado.

| Área | Harness | Acceso | Complejidad | Impacto | Conectores |
|---|---|---|---|---|---|
| Ventas | Deep | Escritura con aprobación | 4/5 - Alta | 4/5 - Alto | HubSpot, Drive, Google Docs, BigQuery |

## Propósito
Demostración atractiva para equipos de preventa.

**Pregunta de demo:** “Prepara una propuesta de servicios para la oportunidad ACME en HubSpot.”

**Resultado esperado:** Documento comercial estructurado con supuestos, precio sujeto a validación y entregables.

**KPI:** Tiempo por propuesta; retrabajo de ofertas.

## Calificación

| Dimensión | Score | Justificación |
|---|---|---|
| Complejidad | 4/5 - Alta | Generación de documentos vía Docs API (Custom Tool), gobierno de tarifas y descuentos y plantillas; contenido largo. |
| Impacto | 4/5 - Alto | Ahorra horas de preventa por propuesta y reduce errores de precio; frecuencia media. |

Rúbrica en [SCORING.md](../../SCORING.md).

## Cómo funciona con Gemini Enterprise y VirtuAI

1. El usuario abre la app de **Ventas** en Gemini Enterprise y selecciona *Commercial Proposal Studio* (registrado como *Custom agent via A2A*).
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
| Skills | `proposal-writing`, `scope-estimator`, `pricing-guardrail` | `skills/` | Build → Skills → Instructions → Skills |
| Reglas | 11 reglas con capa de enforcement | [harness/rules.md](harness/rules.md) | System prompt - Security - Ask - Classifiers |
| Tools | 5 tools: `get_company`, `get_rate_card`, `search_templates`, `draft_proposal`, `create_doc` | [tools-manifest.yaml](harness/tools/tools-manifest.yaml) | MCP Servers - Build → Tools - canvas |
| Conectores | HubSpot, Drive, Google Docs, BigQuery | [mcp-servers.md](harness/tools/mcp-servers.md) | Settings → Workspace settings - MCP Servers |
| Configuración | Modelo, capacidades, memoria, canales, seguridad, publicación, budget | [agent-config.yaml](harness/agent-config.yaml) | Pestañas del agente |
| Knowledge Base | `kb-proposal-builder` - 4 tipos de documento | [knowledge-base.yaml](harness/knowledge-base.yaml) | Build → Knowledge Base |
| Evaluaciones | `eval-proposal-builder` - golden + negativos | [eval-dataset.json](harness/evals/eval-dataset.json) | Monitor → Evaluations |
| A2A | Agent Card de referencia | [agent-card.example.json](harness/a2a/agent-card.example.json) | Channels → A2A - Gemini Enterprise → Agents |

## Tools

| Tool | Ruta | Efecto | Ask | Propósito |
|---|---|---|---|---|
| `get_company` | MCP predefinido - HubSpot | read | No | Leer empresa, deal, contactos y notas de discovery asociadas. |
| `get_rate_card` | MCP predefinido - BigQuery | read | No | Leer tarifas vigentes y reglas de descuento desde la tabla oficial de pricing. |
| `search_templates` (+) | MCP predefinido - Google Drive | read | No | Buscar plantillas de propuesta y términos estándar aprobados. |
| `draft_proposal` | Razonamiento del modelo (sin API) | llm | — | Redactar el contenido de la propuesta con supuestos y precios citados. |
| `create_doc` | Custom Tool HTTP - Cloud Run (IAM) | write | Sí | Crear Google Doc desde plantilla en carpeta autorizada (Docs API vía Cloud Run). Escritura con Ask. |

(+) = tool añadida en el kit para cubrir un conector declarado en el HTML. Los nombres de tools MCP son de diseño: confirmar el nombre real en **List tools**.

## Checklist de implementación

- [ ] **Discovery**: owner del proceso, documentos y accesos de prueba (datos sintéticos) — Tarifas vigentes; Portafolio; Plantillas de propuesta; Términos estándar
- [ ] **Modelo**: proveedor Vertex AI habilitado en Settings → Models & providers
- [ ] **Agente**: Agents → New agent - tipo Deep - **Enable versioning** - pegar `AGENTS.md` (o importar el repo por Git)
- [ ] **Skills**: Build → Skills (o import Git) y adjuntar en Instructions → Skills
- [ ] **Conectores**: crear MCP predefinidos / Custom Tools según `harness/tools/` y adjuntarlos en el canvas
- [ ] **KB**: crear `kb-proposal-builder`, subir documentos aprobados, esperar `completed`
- [ ] **Seguridad**: Ask en escrituras, read-only si aplica, classifiers en shadow mode, budget
- [ ] **Evals**: dataset `eval-proposal-builder` con tools en Mock; pass-rate ≥ umbral de publicación
- [ ] **A2A**: Channels → A2A activo → Publish → copiar Agent Card y endpoint
- [ ] **Gemini Enterprise**: Agents → Add agents → Custom agent via A2A - OAuth (Client ID/Secret, `/a2a/oauth/authorize`, `/a2a/oauth/token`, scope `a2a:invoke`)
- [ ] **Pruebas E2E**: usuario autorizado, usuario sin permiso, dato faltante, aprobación de escritura
- [ ] **Operar**: Monitor → Conversations, Access log, regresiones por versión

## Archivos

- `AGENTS.md`
- `ARCHITECTURE.md`
- `skills/proposal-writing/SKILL.md`
- `skills/scope-estimator/SKILL.md`
- `skills/pricing-guardrail/SKILL.md`
- `harness/agent-config.yaml`
- `harness/rules.md`
- `harness/knowledge-base.yaml`
- `harness/tools/tools-manifest.yaml`
- `harness/tools/mcp-servers.md`
- `harness/tools/custom/create_doc.tool.json`
- `harness/evals/eval-dataset.json`
- `harness/a2a/agent-card.example.json`

## Referencias
- VirtuAI: [https://docs.imvirtuai.com/getting-started/overview/](https://docs.imvirtuai.com/getting-started/overview/) - [Tools](https://docs.imvirtuai.com/guides/tools/) - [Skills](https://docs.imvirtuai.com/build/skills/) - [Deep agents](https://docs.imvirtuai.com/build/deep-agents/) - [A2A](https://docs.imvirtuai.com/channels/a2a/) - [Evaluations](https://docs.imvirtuai.com/build/evaluations/) - [Import/Export](https://docs.imvirtuai.com/build/import-export/)
- Gemini Enterprise: [Registrar agente A2A](https://docs.cloud.google.com/gemini/enterprise/docs/register-and-manage-an-a2a-agent)
