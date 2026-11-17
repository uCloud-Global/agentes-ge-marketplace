# Arquitectura - Talent Selection Evidence Analyst

**Área:** Talento - **Harness:** Deep - **Acceso:** Escritura con aprobación - **Complejidad:** 5/5 (muy alta) - **Impacto:** 3/5 (medio)

## 1. Arquitectura (inputs → configuración → tools → outputs)

```mermaid
flowchart LR
  subgraph IN["Inputs"]
    direction TB
    U(["Usuario corporativo autenticado"])
    Q["Solicitud: Para la vacante Analista de Datos, compara tres CV ficticios con criterios predefinidos,…"]
    DOCS[/"Documentos: Descripción y requisitos del cargo, Rúbrica aprobada de competencias y pesos, CVs autoriz…"/]
  end
  subgraph GE["Gemini Enterprise"]
    direction TB
    APP["App ge-talento - Custom agent via A2A"]
  end
  subgraph VA["VirtuAI - Talent Selection Evidence Analyst"]
    direction TB
    GOV{"Governance check: permisos, budget, guardrails"}
    LOOP(("Agentic loop Deep"))
    subgraph CFG["Configuración"]
      direction TB
      H["Harness: Deep - Gemini Pro - T=0.1 - max 10000 tok"]
      SP["System prompt: AGENTS.md"]
      SK["Skills: cv-competency-review, bias-safeguard, interview-guide"]
      KB[("KB kb-talent-selection")]
      MEM["Memoria 16 KB - sin PII"]
      GR["Guardrails: prompt_injection, off_topic, shell_risk"]
      SEC["Security: Ask before each call - HITL"]
    end
  end
  subgraph TL["Tools"]
    direction TB
    T_custom["Custom Tool HTTP - Cloud Run (IAM)<br/>get_job_profile<br/>extract_cv_evidence<br/>standardize_role_rubric"]
    T_workstation["Deep Agent - Workstation / sandbox (Python)<br/>render_skills_radar"]
  end
  subgraph SYS["Sistemas externos"]
    direction TB
    S_custom[("API privada / Cloud Run")]
    S_workstation[("Entorno aislado")]
  end
  subgraph OUT["Outputs"]
    direction TB
    O1["Matriz explicable por competencia, radar Python y preguntas de entrevista, no realiza selección ni descarte a…"]
    O2["Aprobaciones input-required"]
    O3["Worklog - auditoría - métricas de uso"]
    O4["KPI: Cobertura de evidencias, consistencia de rúbrica, tiempo de pre-revisión."]
  end
  U --> Q --> APP
  APP -->|"A2A JSON-RPC + OAuth a2a:invoke"| GOV --> LOOP
  CFG -.-> LOOP
  DOCS -.->|"indexación"| KB
  LOOP --> T_custom
  T_custom -->|IAM run.invoker| S_custom
  LOOP --> T_workstation
  T_workstation --> S_workstation
  LOOP --> O1
  LOOP --> O3
  LOOP --> O2
  O1 -->|"respuesta A2A streaming"| APP
  classDef inp fill:#e8f0fe,stroke:#1a73e8,color:#15213d
  classDef out fill:#e6f4ea,stroke:#34a853,color:#15213d
  classDef cfg fill:#fff8e1,stroke:#fbbc04,color:#15213d
  classDef tool fill:#fce8e6,stroke:#ea4335,color:#15213d
  class U,Q,DOCS inp
  class O1,O3,O4 out
  class H,SP,SK,KB,GR,SEC cfg
  class MEM cfg
  class O2 out
  class T_custom,T_workstation tool
```

## 2. Secuencia de una ejecución (Gemini Enterprise → A2A → VirtuAI)

```mermaid
sequenceDiagram
  autonumber
  actor U as Usuario
  participant GE as Gemini Enterprise
  participant V as VirtuAI - agente
  participant P_custom as Custom Tool
  participant P_workstation as Workstation
  U->>GE: Para la vacante Analista de Datos, compara tres CV ficticios con criterios pred…
  GE->>V: A2A message/stream (Bearer, scope a2a:invoke)
  V->>V: Governance check y carga de skill cv-competency-review
  loop Workflow: Leer requisitos y rúbrica → Extraer evidencias pertinentes de CVs → Estandarizar habilidades y anotar vacíos
    V->>P_custom: get_job_profile
    P_custom-->>V: datos (permisos del usuario)
    V->>P_custom: extract_cv_evidence
    P_custom-->>V: datos (permisos del usuario)
    V->>P_custom: standardize_role_rubric
    P_custom-->>V: datos (permisos del usuario)
    V->>P_workstation: render_skills_radar
    P_workstation-->>V: datos (permisos del usuario)
  end
  V->>V: build_evidence_matrix, draft_interview_questions (modelo)
  V-->>GE: Matriz explicable por competencia, radar Python y preguntas de entrevista, no r…
  GE-->>U: Respuesta con fuentes y limitaciones
```

## 3. Workflow de la skill principal `cv-competency-review`

```mermaid
flowchart TD
  S0["1. Leer requisitos con get_job_profile y rúbrica con standardize_role_rubric"]
  S0 -.-> X0_get_job_profile[["get_job_profile<br/>Custom Tool"]]
  S0 -.-> X0_standardize_role_rubric[["standardize_role_rubric<br/>Custom Tool"]]
  S1["2. Extraer evidencias con extract_cv_evidence (sin atributos protegidos)"]
  S0 --> S1
  S1 -.-> X1_extract_cv_evidence[["extract_cv_evidence<br/>Custom Tool"]]
  S2["3. Estandarizar habilidades y anotar NO OBSERVADO cuando falte evidencia"]
  S1 --> S2
  S3["4. Construir matriz con build_evidence_matrix"]
  S2 --> S3
  S3 -.-> X3_build_evidence_matrix[["build_evidence_matrix<br/>Modelo"]]
  S4["5. Generar radar con render_skills_radar"]
  S3 --> S4
  S4 -.-> X4_render_skills_radar[["render_skills_radar<br/>Workstation"]]
  S5["6. Proponer preguntas de entrevista y remitir a RR. HH."]
  S4 --> S5
  S5 --> R(["Matriz explicable por competencia (evidencia citada) - radar PNG - preguntas de entrevist…"])
```

## 4. Matriz de inputs, configuración, tools y outputs

| Inputs | Configuración | Tools | Outputs |
|---|---|---|---|
| Solicitud en lenguaje natural vía Gemini Enterprise<br>Identidad del usuario (OAuth A2A)<br>Tokens OAuth por conector<br>Doc: Descripción y requisitos del cargo<br>Doc: Rúbrica aprobada de competencias y pesos<br>Doc: CVs autorizados y minimizados<br>Doc: Matriz de evidencias<br>Doc: Política de datos de candidatos | Harness **Deep**<br>Modelo Gemini Pro - T=0.1<br>System prompt `AGENTS.md`<br>Skills: `cv-competency-review`, `bias-safeguard`, `interview-guide`<br>KB `kb-talent-selection`<br>Guardrails: prompt_injection, off_topic, shell_risk<br>Memoria sin PII | `get_job_profile` (Custom Tool)<br>`extract_cv_evidence` (Custom Tool)<br>`standardize_role_rubric` (Custom Tool)<br>`build_evidence_matrix` (Modelo)<br>`render_skills_radar` (Workstation, Ask)<br>`draft_interview_questions` (Modelo) | Matriz explicable por competencia, radar Python y preguntas de entrevista; no realiza selección ni descarte automático.<br>Worklog y auditoría en VirtuAI<br>Acciones pendientes de aprobación |

## 5. Capas de identidad

1. **Gemini Enterprise** — licencia + rol IAM sobre la app del área.
2. **A2A OAuth** — el usuario consiente `a2a:invoke` en VirtuAI (Authorization Code + PKCE).
3. **Conectores** — OAuth individual por MCP; IAM de servicio para Cloud Run con autorización de negocio en backend.
4. **Datos/acciones** — ACL de origen, RBAC, filas y aprobación humana.
