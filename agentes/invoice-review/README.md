# Accounts Payable Reviewer

> Concilia facturas, órdenes y proveedores; marca discrepancias antes del pago.

| Área | Harness | Acceso | Complejidad | Impacto | Conectores |
|---|---|---|---|---|---|
| Finanzas | Deep | Escritura con aprobación | 5/5 - Muy alta | 5/5 - Muy alto | Drive, BigQuery, Gmail, API / Cloud Run |

## Propósito
Caso de alto ROI; empezar con documentos sintéticos.

**Pregunta de demo:** “Revisa las facturas recibidas hoy y detecta diferencias frente a sus órdenes.”

**Resultado esperado:** Informe de coincidencias, excepciones y borradores de casos de revisión.

**KPI:** Tiempo por factura; % errores detectados.

## Calificación

| Dimensión | Score | Justificación |
|---|---|---|
| Complejidad | 5/5 - Muy alta | Extracción documental (Document AI) + 3-way match con ERP + validación de proveedor: tres Custom Tools, datos bancarios y control de fraude. |
| Impacto | 5/5 - Muy alto | Alto volumen de facturas, ahorro por factura y prevención de pagos erróneos o fraudulentos; ROI directo. |

Rúbrica en [SCORING.md](../../SCORING.md).

## Cómo funciona con Gemini Enterprise y VirtuAI

1. El usuario abre la app de **Finanzas** en Gemini Enterprise y selecciona *Accounts Payable Reviewer* (registrado como *Custom agent via A2A*).
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
| Skills | `invoice-matching`, `vendor-bank-change-alert`, `duplicate-invoice-check` | `skills/` | Build → Skills → Instructions → Skills |
| Reglas | 11 reglas con capa de enforcement | [harness/rules.md](harness/rules.md) | System prompt - Security - Ask - Classifiers |
| Tools | 5 tools: `extract_invoice`, `match_po`, `check_vendor`, `search_invoices_mail`, `create_review_case` | [tools-manifest.yaml](harness/tools/tools-manifest.yaml) | MCP Servers - Build → Tools - canvas |
| Conectores | Drive, BigQuery, Gmail, API / Cloud Run | [mcp-servers.md](harness/tools/mcp-servers.md) | Settings → Workspace settings - MCP Servers |
| Configuración | Modelo, capacidades, memoria, canales, seguridad, publicación, budget | [agent-config.yaml](harness/agent-config.yaml) | Pestañas del agente |
| Knowledge Base | `kb-invoice-review` - 3 tipos de documento | [knowledge-base.yaml](harness/knowledge-base.yaml) | Build → Knowledge Base |
| Evaluaciones | `eval-invoice-review` - golden + negativos | [eval-dataset.json](harness/evals/eval-dataset.json) | Monitor → Evaluations |
| A2A | Agent Card de referencia | [agent-card.example.json](harness/a2a/agent-card.example.json) | Channels → A2A - Gemini Enterprise → Agents |

## Tools

| Tool | Ruta | Efecto | Ask | Propósito |
|---|---|---|---|---|
| `extract_invoice` | Custom Tool HTTP - Cloud Run (IAM) | compute | No | Extraer campos de factura (proveedor, NIT, fecha, ítems, totales, impuestos) vía Document AI en Cloud Run. |
| `match_po` | MCP predefinido - BigQuery | compute | No | Cruzar factura contra orden de compra y recepción (3-way match) en vistas ERP allowlisted. |
| `check_vendor` | Custom Tool HTTP - Cloud Run (IAM) | compute | No | Validar proveedor en maestro ERP (estado, cuenta bancaria registrada, listas restrictivas). |
| `search_invoices_mail` (+) | MCP predefinido - Gmail | read | No | Buscar facturas recibidas en el buzón de cuentas por pagar. |
| `create_review_case` | Custom Tool HTTP - Cloud Run (IAM) | write | Sí | Crear caso de revisión en el sistema de AP. Escritura con Ask. |

(+) = tool añadida en el kit para cubrir un conector declarado en el HTML. Los nombres de tools MCP son de diseño: confirmar el nombre real en **List tools**.

## Checklist de implementación

- [ ] **Discovery**: owner del proceso, documentos y accesos de prueba (datos sintéticos) — Política de compras; Órdenes de compra; Condiciones de pago
- [ ] **Modelo**: proveedor Vertex AI habilitado en Settings → Models & providers
- [ ] **Agente**: Agents → New agent - tipo Deep - **Enable versioning** - pegar `AGENTS.md` (o importar el repo por Git)
- [ ] **Skills**: Build → Skills (o import Git) y adjuntar en Instructions → Skills
- [ ] **Conectores**: crear MCP predefinidos / Custom Tools según `harness/tools/` y adjuntarlos en el canvas
- [ ] **KB**: crear `kb-invoice-review`, subir documentos aprobados, esperar `completed`
- [ ] **Seguridad**: Ask en escrituras, read-only si aplica, classifiers en shadow mode, budget
- [ ] **Evals**: dataset `eval-invoice-review` con tools en Mock; pass-rate ≥ umbral de publicación
- [ ] **A2A**: Channels → A2A activo → Publish → copiar Agent Card y endpoint
- [ ] **Gemini Enterprise**: Agents → Add agents → Custom agent via A2A - OAuth (Client ID/Secret, `/a2a/oauth/authorize`, `/a2a/oauth/token`, scope `a2a:invoke`)
- [ ] **Pruebas E2E**: usuario autorizado, usuario sin permiso, dato faltante, aprobación de escritura
- [ ] **Operar**: Monitor → Conversations, Access log, regresiones por versión

## Archivos

- `AGENTS.md`
- `ARCHITECTURE.md`
- `skills/invoice-matching/SKILL.md`
- `skills/vendor-bank-change-alert/SKILL.md`
- `skills/duplicate-invoice-check/SKILL.md`
- `harness/agent-config.yaml`
- `harness/rules.md`
- `harness/knowledge-base.yaml`
- `harness/tools/tools-manifest.yaml`
- `harness/tools/mcp-servers.md`
- `harness/tools/custom/extract_invoice.tool.json`
- `harness/tools/custom/check_vendor.tool.json`
- `harness/tools/custom/create_review_case.tool.json`
- `harness/evals/eval-dataset.json`
- `harness/a2a/agent-card.example.json`

## Referencias
- VirtuAI: [https://docs.imvirtuai.com/getting-started/overview/](https://docs.imvirtuai.com/getting-started/overview/) - [Tools](https://docs.imvirtuai.com/guides/tools/) - [Skills](https://docs.imvirtuai.com/build/skills/) - [Deep agents](https://docs.imvirtuai.com/build/deep-agents/) - [A2A](https://docs.imvirtuai.com/channels/a2a/) - [Evaluations](https://docs.imvirtuai.com/build/evaluations/) - [Import/Export](https://docs.imvirtuai.com/build/import-export/)
- Gemini Enterprise: [Registrar agente A2A](https://docs.cloud.google.com/gemini/enterprise/docs/register-and-manage-an-a2a-agent)
