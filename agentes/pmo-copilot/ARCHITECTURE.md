# Arquitectura - Project PMO Copilot

**Área:** Operaciones - **Harness:** Deep - **Acceso:** Lectura - **Complejidad:** 3/5 (media) - **Impacto:** 3/5 (medio)

## 1. Arquitectura (inputs → configuración → tools → outputs)

```mermaid
flowchart LR
  subgraph IN["Inputs"]
    direction TB
    U(["Usuario corporativo autenticado"])
    Q["Solicitud: Prepara el informe semanal de los proyectos y sus principales riesgos."]
    DOCS[/"Documentos: Plan de proyecto, RACI, Actas, Hitos comprometidos"/]
  end
  subgraph GE["Gemini Enterprise"]
    direction TB
    APP["App ge-operaciones - Custom agent via A2A"]
  end
  subgraph VA["VirtuAI - Project PMO Copilot"]
    direction TB
    GOV{"Governance check: permisos, budget, guardrails"}
    LOOP(("Agentic loop Deep"))
    subgraph CFG["Configuración"]
      direction TB
      H["Harness: Deep - Gemini Pro - T=0.3 - max 6000 tok"]
      SP["System prompt: AGENTS.md"]
      SK["Skills: project-report, meeting-minutes, risk-register"]
      KB[("KB kb-pmo-copilot")]
      MEM["Memoria 16 KB - sin PII"]
      GR["Guardrails: prompt_injection, off_topic"]
      SEC["Security: Read-only"]
    end
  end
  subgraph TL["Tools"]
    direction TB
    T_mcp_drive["MCP predefinido - Google Drive<br/>read_project_docs"]
    T_custom["Custom Tool HTTP - Cloud Run (IAM)<br/>get_milestones"]
    T_mcp_calendar["MCP predefinido - Google Calendar<br/>list_meetings"]
    T_mcp_gmail["MCP predefinido - Gmail<br/>draft_followup (Ask)"]
  end
  subgraph SYS["Sistemas externos"]
    direction TB
    S_mcp_drive[("Google Drive")]
    S_custom[("API privada / Cloud Run")]
    S_mcp_calendar[("Google Calendar")]
    S_mcp_gmail[("Gmail")]
  end
  subgraph OUT["Outputs"]
    direction TB
    O1["Status report, RAG semaforizado y seguimiento propuesto."]
    O3["Worklog - auditoría - métricas de uso"]
    O4["KPI: Horas semanales de reporting, hitos cumplidos."]
  end
  U --> Q --> APP
  APP -->|"A2A JSON-RPC + OAuth a2a:invoke"| GOV --> LOOP
  CFG -.-> LOOP
  DOCS -.->|"indexación"| KB
  LOOP --> T_mcp_drive
  T_mcp_drive -->|OAuth por usuario| S_mcp_drive
  LOOP --> T_custom
  T_custom -->|IAM run.invoker| S_custom
  LOOP --> T_mcp_calendar
  T_mcp_calendar -->|OAuth por usuario| S_mcp_calendar
  LOOP -->|Ask / aprobación| T_mcp_gmail
  T_mcp_gmail -->|OAuth por usuario| S_mcp_gmail
  LOOP --> O1
  LOOP --> O3
  O1 -->|"respuesta A2A streaming"| APP
  classDef inp fill:#e8f0fe,stroke:#1a73e8,color:#15213d
  classDef out fill:#e6f4ea,stroke:#34a853,color:#15213d
  classDef cfg fill:#fff8e1,stroke:#fbbc04,color:#15213d
  classDef tool fill:#fce8e6,stroke:#ea4335,color:#15213d
  class U,Q,DOCS inp
  class O1,O3,O4 out
  class H,SP,SK,KB,GR,SEC cfg
  class MEM cfg
  class T_mcp_drive,T_custom,T_mcp_calendar,T_mcp_gmail tool
```

## 2. Secuencia de una ejecución (Gemini Enterprise → A2A → VirtuAI)

```mermaid
sequenceDiagram
  autonumber
  actor U as Usuario
  participant GE as Gemini Enterprise
  participant V as VirtuAI - agente
  participant P_mcp_drive as Google Drive
  participant P_custom as Custom Tool
  participant P_mcp_calendar as Google Calendar
  participant P_mcp_gmail as Gmail
  U->>GE: Prepara el informe semanal de los proyectos y sus principales riesgos.
  GE->>V: A2A message/stream (Bearer, scope a2a:invoke)
  V->>V: Governance check y carga de skill project-report
  loop Workflow: Reunir estado → Detectar bloqueos → Cruzar hitos
    V->>P_mcp_drive: read_project_docs
    P_mcp_drive-->>V: datos (permisos del usuario)
    V->>P_custom: get_milestones
    P_custom-->>V: datos (permisos del usuario)
    V->>P_mcp_calendar: list_meetings
    P_mcp_calendar-->>V: datos (permisos del usuario)
  end
  V->>V: draft_status (modelo)
  V-->>GE: task input-required (vista previa + approval_requests)
  GE-->>U: Solicitud de aprobación
  alt Aprobado
    U->>GE: Aprobar
    GE->>V: respuesta de aprobación
    V->>P_mcp_gmail: draft_followup (request_id)
    P_mcp_gmail-->>V: OK + ID
  else Denegado o expira
    V->>V: acción queda pendiente, sin reintento
  end
  V-->>GE: Status report, RAG semaforizado y seguimiento propuesto.
  GE-->>U: Respuesta con fuentes y limitaciones
```

## 3. Workflow de la skill principal `project-report`

```mermaid
flowchart TD
  S0["1. Reunir estado con read_project_docs y get_milestones"]
  S0 -.-> X0_read_project_docs[["read_project_docs<br/>Google Drive"]]
  S0 -.-> X0_get_milestones[["get_milestones<br/>Custom Tool"]]
  S1["2. Detectar hitos vencidos o en riesgo"]
  S0 --> S1
  S2["3. Extraer bloqueos de actas"]
  S1 --> S2
  S3["4. Semaforizar RAG con criterio explícito"]
  S2 --> S3
  S4["5. Redactar reporte y borradores de seguimiento"]
  S3 --> S4
  S4 --> R(["Status report: RAG por proyecto - hitos - riesgos - bloqueos - próximos compromisos"])
```

## 4. Matriz de inputs, configuración, tools y outputs

| Inputs | Configuración | Tools | Outputs |
|---|---|---|---|
| Solicitud en lenguaje natural vía Gemini Enterprise<br>Identidad del usuario (OAuth A2A)<br>Tokens OAuth por conector<br>Doc: Plan de proyecto<br>Doc: RACI<br>Doc: Actas<br>Doc: Hitos comprometidos | Harness **Deep**<br>Modelo Gemini Pro - T=0.3<br>System prompt `AGENTS.md`<br>Skills: `project-report`, `meeting-minutes`, `risk-register`<br>KB `kb-pmo-copilot`<br>Guardrails: prompt_injection, off_topic<br>Memoria sin PII | `read_project_docs` (Google Drive)<br>`get_milestones` (Custom Tool)<br>`list_meetings` (Google Calendar)<br>`draft_status` (Modelo)<br>`draft_followup` (Gmail, Ask) | Status report, RAG semaforizado y seguimiento propuesto.<br>Worklog y auditoría en VirtuAI<br>Sin efectos en sistemas (solo lectura) |

## 5. Capas de identidad

1. **Gemini Enterprise** — licencia + rol IAM sobre la app del área.
2. **A2A OAuth** — el usuario consiente `a2a:invoke` en VirtuAI (Authorization Code + PKCE).
3. **Conectores** — OAuth individual por MCP; IAM de servicio para Cloud Run con autorización de negocio en backend.
4. **Datos/acciones** — ACL de origen, RBAC, filas y aprobación humana.
