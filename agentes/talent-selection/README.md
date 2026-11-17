# Talent Selection Evidence Analyst

> Contrasta los requisitos objetivos de una vacante con evidencias aportadas por CVs, construye una matriz uniforme y genera un radar polar para revisión humana. No decide contrataciones.

| Área | Harness | Acceso | Complejidad | Impacto | Conectores |
|---|---|---|---|---|---|
| Talento | Deep | Escritura con aprobación | 5/5 - Muy alta | 3/5 - Medio | Drive, Google Docs, Google Sheets, API / Cloud Run |

## Propósito
Demo con datos sintéticos, rúbrica validada y gráfico polar generado por Matplotlib.

**Pregunta de demo:** “Para la vacante Analista de Datos, compara tres CV ficticios con criterios predefinidos; muestra evidencias, vacíos y un gráfico radar para revisión de RR. HH.”

**Resultado esperado:** Matriz explicable por competencia, radar Python y preguntas de entrevista; no realiza selección ni descarte automático.

**KPI:** Cobertura de evidencias; consistencia de rúbrica; tiempo de pre-revisión.

## Calificación

| Dimensión | Score | Justificación |
|---|---|---|
| Complejidad | 5/5 - Muy alta | Tres Custom Tools (ATS, extracción de CV, rúbrica) + Workstation para el radar, PII de candidatos, controles de sesgo y workspace aislado. |
| Impacto | 3/5 - Medio | Reduce el tiempo de pre-revisión de CVs; el impacto se limita por diseño: la decisión siempre es humana. |

Rúbrica en [SCORING.md](../../SCORING.md).

## Cómo funciona con Gemini Enterprise y VirtuAI

1. El usuario abre la app de **Talento** en Gemini Enterprise y selecciona *Talent Selection Evidence Analyst* (registrado como *Custom agent via A2A*).
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
| Skills | `cv-competency-review`, `bias-safeguard`, `interview-guide` | `skills/` | Build → Skills → Instructions → Skills |
| Reglas | 12 reglas con capa de enforcement | [harness/rules.md](harness/rules.md) | System prompt - Security - Ask - Classifiers |
| Tools | 6 tools: `get_job_profile`, `extract_cv_evidence`, `standardize_role_rubric`, `build_evidence_matrix`, `render_skills_radar`, `draft_interview_questions` | [tools-manifest.yaml](harness/tools/tools-manifest.yaml) | MCP Servers - Build → Tools - canvas |
| Conectores | Drive, Google Docs, Google Sheets, API / Cloud Run | [mcp-servers.md](harness/tools/mcp-servers.md) | Settings → Workspace settings - MCP Servers |
| Configuración | Modelo, capacidades, memoria, canales, seguridad, publicación, budget | [agent-config.yaml](harness/agent-config.yaml) | Pestañas del agente |
| Knowledge Base | `kb-talent-selection` - 5 tipos de documento | [knowledge-base.yaml](harness/knowledge-base.yaml) | Build → Knowledge Base |
| Evaluaciones | `eval-talent-selection` - golden + negativos | [eval-dataset.json](harness/evals/eval-dataset.json) | Monitor → Evaluations |
| A2A | Agent Card de referencia | [agent-card.example.json](harness/a2a/agent-card.example.json) | Channels → A2A - Gemini Enterprise → Agents |

## Tools

| Tool | Ruta | Efecto | Ask | Propósito |
|---|---|---|---|---|
| `get_job_profile` | Custom Tool HTTP - Cloud Run (IAM) | read | No | Leer descripción y requisitos de la vacante autorizada (ATS vía Cloud Run). |
| `extract_cv_evidence` | Custom Tool HTTP - Cloud Run (IAM) | compute | No | Extraer evidencias profesionales pertinentes de un CV autorizado, eliminando atributos protegidos. |
| `standardize_role_rubric` | Custom Tool HTTP - Cloud Run (IAM) | compute | No | Obtener rúbrica versionada (competencias, pesos, objetivos) aprobada por Talento. |
| `build_evidence_matrix` | Razonamiento del modelo (sin API) | llm | — | Construir matriz uniforme candidato × competencia con cita de evidencia o NO OBSERVADO. |
| `render_skills_radar` | Deep Agent - Workstation / sandbox (Python) | compute | Sí | Generar radar polar con harness/tools/scripts/render_skills_radar.py (Workstation o Cloud Run). |
| `draft_interview_questions` | Razonamiento del modelo (sin API) | llm | — | Proponer preguntas de entrevista para validar vacíos de evidencia. |

(+) = tool añadida en el kit para cubrir un conector declarado en el HTML. Los nombres de tools MCP son de diseño: confirmar el nombre real en **List tools**.

## Checklist de implementación

- [ ] **Discovery**: owner del proceso, documentos y accesos de prueba (datos sintéticos) — Descripción y requisitos del cargo; Rúbrica aprobada de competencias y pesos; CVs autorizados y minimizados; Matriz de evidencias; Política de datos de candidatos
- [ ] **Modelo**: proveedor Vertex AI habilitado en Settings → Models & providers
- [ ] **Agente**: Agents → New agent - tipo Deep - **Enable versioning** - pegar `AGENTS.md` (o importar el repo por Git)
- [ ] **Skills**: Build → Skills (o import Git) y adjuntar en Instructions → Skills
- [ ] **Conectores**: crear MCP predefinidos / Custom Tools según `harness/tools/` y adjuntarlos en el canvas
- [ ] **KB**: crear `kb-talent-selection`, subir documentos aprobados, esperar `completed`
- [ ] **Seguridad**: Ask en escrituras, read-only si aplica, classifiers en shadow mode, budget
- [ ] **Evals**: dataset `eval-talent-selection` con tools en Mock; pass-rate ≥ umbral de publicación
- [ ] **A2A**: Channels → A2A activo → Publish → copiar Agent Card y endpoint
- [ ] **Gemini Enterprise**: Agents → Add agents → Custom agent via A2A - OAuth (Client ID/Secret, `/a2a/oauth/authorize`, `/a2a/oauth/token`, scope `a2a:invoke`)
- [ ] **Pruebas E2E**: usuario autorizado, usuario sin permiso, dato faltante, aprobación de escritura
- [ ] **Operar**: Monitor → Conversations, Access log, regresiones por versión

## Archivos

- `AGENTS.md`
- `ARCHITECTURE.md`
- `skills/cv-competency-review/SKILL.md`
- `skills/bias-safeguard/SKILL.md`
- `skills/interview-guide/SKILL.md`
- `harness/agent-config.yaml`
- `harness/rules.md`
- `harness/knowledge-base.yaml`
- `harness/tools/tools-manifest.yaml`
- `harness/tools/mcp-servers.md`
- `harness/tools/custom/get_job_profile.tool.json`
- `harness/tools/custom/extract_cv_evidence.tool.json`
- `harness/tools/custom/standardize_role_rubric.tool.json`
- `harness/evals/eval-dataset.json`
- `harness/a2a/agent-card.example.json`
- `harness/tools/scripts/render_skills_radar.py`
- `harness/tools/scripts/radar_demo.png`

## Referencias
- VirtuAI: [https://docs.imvirtuai.com/getting-started/overview/](https://docs.imvirtuai.com/getting-started/overview/) - [Tools](https://docs.imvirtuai.com/guides/tools/) - [Skills](https://docs.imvirtuai.com/build/skills/) - [Deep agents](https://docs.imvirtuai.com/build/deep-agents/) - [A2A](https://docs.imvirtuai.com/channels/a2a/) - [Evaluations](https://docs.imvirtuai.com/build/evaluations/) - [Import/Export](https://docs.imvirtuai.com/build/import-export/)
- Gemini Enterprise: [Registrar agente A2A](https://docs.cloud.google.com/gemini/enterprise/docs/register-and-manage-an-a2a-agent)
