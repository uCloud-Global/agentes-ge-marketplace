# Arquitectura - Employee Onboarding Navigator

**Área:** Talento - **Harness:** Deep - **Acceso:** Escritura con aprobación - **Complejidad:** 4/5 (alta) - **Impacto:** 3/5 (medio)

## 1. Arquitectura (inputs → configuración → tools → outputs)

```mermaid
flowchart LR
  subgraph IN["Inputs"]
    direction TB
    U(["Usuario corporativo autenticado"])
    Q["Solicitud: Prepara el onboarding de una persona que ingresa el próximo lunes al equipo de datos."]
    DOCS[/"Documentos: Manual de bienvenida, Checklist de ingreso, Políticas TI, Beneficios"/]
  end
  subgraph GE["Gemini Enterprise"]
    direction TB
    APP["App ge-talento - Custom agent via A2A"]
  end
  subgraph VA["VirtuAI - Employee Onboarding Navigator"]
    direction TB
    GOV{"Governance check: permisos, budget, guardrails"}
    LOOP(("Agentic loop Deep"))
    subgraph CFG["Configuración"]
      direction TB
      H["Harness: Deep - Gemini Pro - T=0.3 - max 6000 tok"]
      SP["System prompt: AGENTS.md"]
      SK["Skills: employee-onboarding, access-request-builder, first-week-plan"]
      KB[("KB kb-onboarding-agent")]
      MEM["Memoria 16 KB - sin PII"]
      GR["Guardrails: prompt_injection, off_topic"]
      SEC["Security: Ask before each call - HITL"]
    end
  end
  subgraph TL["Tools"]
    direction TB
    T_mcp_drive["MCP predefinido - Google Drive<br/>get_onboarding_plan"]
    T_mcp_calendar["MCP predefinido - Google Calendar<br/>schedule_welcome (Ask)"]
    T_mcp_gmail["MCP predefinido - Gmail<br/>draft_welcome_mail (Ask)"]
    T_custom["Custom Tool HTTP - Cloud Run (IAM)<br/>request_access (Ask)"]
  end
  subgraph SYS["Sistemas externos"]
    direction TB
    S_mcp_drive[("Google Drive")]
    S_mcp_calendar[("Google Calendar")]
    S_mcp_gmail[("Gmail")]
    S_custom[("API privada / Cloud Run")]
  end
  subgraph OUT["Outputs"]
    direction TB
    O1["Checklist por áreas, eventos propuestos, borradores y tareas de acceso."]
    O2["Aprobaciones input-required"]
    O3["Worklog - auditoría - métricas de uso"]
    O4["KPI: Tiempo de incorporación, completitud de checklist."]
  end
  U --> Q --> APP
  APP -->|"A2A JSON-RPC + OAuth a2a:invoke"| GOV --> LOOP
  CFG -.-> LOOP
  DOCS -.->|"indexación"| KB
  LOOP --> T_mcp_drive
  T_mcp_drive -->|OAuth por usuario| S_mcp_drive
  LOOP -->|Ask / aprobación| T_mcp_calendar
  T_mcp_calendar -->|OAuth por usuario| S_mcp_calendar
  LOOP -->|Ask / aprobación| T_mcp_gmail
  T_mcp_gmail -->|OAuth por usuario| S_mcp_gmail
  LOOP -->|Ask / aprobación| T_custom
  T_custom -->|IAM run.invoker| S_custom
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
  class T_mcp_drive,T_mcp_calendar,T_mcp_gmail,T_custom tool
```

## 2. Secuencia de una ejecución (Gemini Enterprise → A2A → VirtuAI)

```mermaid
sequenceDiagram
  autonumber
  actor U as Usuario
  participant GE as Gemini Enterprise
  participant V as VirtuAI - agente
  participant P_mcp_drive as Google Drive
  participant P_mcp_calendar as Google Calendar
  participant P_mcp_gmail as Gmail
  participant P_custom as Custom Tool
  U->>GE: Prepara el onboarding de una persona que ingresa el próximo lunes al equipo de…
  GE->>V: A2A message/stream (Bearer, scope a2a:invoke)
  V->>V: Governance check y carga de skill employee-onboarding
  loop Workflow: Crear checklist → Buscar políticas → Agendar bienvenida
    V->>P_mcp_drive: get_onboarding_plan
    P_mcp_drive-->>V: datos (permisos del usuario)
  end
  V-->>GE: task input-required (vista previa + approval_requests)
  GE-->>U: Solicitud de aprobación
  alt Aprobado
    U->>GE: Aprobar
    GE->>V: respuesta de aprobación
    V->>P_mcp_calendar: schedule_welcome (request_id)
    P_mcp_calendar-->>V: OK + ID
    V->>P_mcp_gmail: draft_welcome_mail (request_id)
    P_mcp_gmail-->>V: OK + ID
    V->>P_custom: request_access (request_id)
    P_custom-->>V: OK + ID
  else Denegado o expira
    V->>V: acción queda pendiente, sin reintento
  end
  V-->>GE: Checklist por áreas, eventos propuestos, borradores y tareas de acceso.
  GE-->>U: Respuesta con fuentes y limitaciones
```

## 3. Workflow de la skill principal `employee-onboarding`

```mermaid
flowchart TD
  S0["1. Confirmar área, rol, fecha de ingreso y manager"]
  S1["2. Generar checklist por área con get_onboarding_plan"]
  S0 --> S1
  S1 -.-> X1_get_onboarding_plan[["get_onboarding_plan<br/>Google Drive"]]
  S2["3. Proponer agenda de bienvenida y pedir aprobación antes de schedule_welcome"]
  S1 --> S2
  S2 -.-> X2_schedule_welcome[["schedule_welcome<br/>Google Calendar"]]
  style X2_schedule_welcome fill:#fce8e6,stroke:#ea4335
  S3["4. Preparar borrador de bienvenida con draft_welcome_mail"]
  S2 --> S3
  S3 -.-> X3_draft_welcome_mail[["draft_welcome_mail<br/>Gmail"]]
  style X3_draft_welcome_mail fill:#fce8e6,stroke:#ea4335
  S4["5. Preparar solicitudes de acceso mínimas por rol y pedir aprobación antes de requ…"]
  S3 --> S4
  S4 -.-> X4_request_access[["request_access<br/>Custom Tool"]]
  style X4_request_access fill:#fce8e6,stroke:#ea4335
  S4 --> R(["Checklist por área - eventos propuestos - borradores - solicitudes de acceso pendientes"])
```

## 4. Matriz de inputs, configuración, tools y outputs

| Inputs | Configuración | Tools | Outputs |
|---|---|---|---|
| Solicitud en lenguaje natural vía Gemini Enterprise<br>Identidad del usuario (OAuth A2A)<br>Tokens OAuth por conector<br>Doc: Manual de bienvenida<br>Doc: Checklist de ingreso<br>Doc: Políticas TI<br>Doc: Beneficios | Harness **Deep**<br>Modelo Gemini Pro - T=0.3<br>System prompt `AGENTS.md`<br>Skills: `employee-onboarding`, `access-request-builder`, `first-week-plan`<br>KB `kb-onboarding-agent`<br>Guardrails: prompt_injection, off_topic<br>Memoria sin PII | `get_onboarding_plan` (Google Drive)<br>`schedule_welcome` (Google Calendar, Ask)<br>`draft_welcome_mail` (Gmail, Ask)<br>`request_access` (Custom Tool, Ask) | Checklist por áreas, eventos propuestos, borradores y tareas de acceso.<br>Worklog y auditoría en VirtuAI<br>Acciones pendientes de aprobación |

## 5. Capas de identidad

1. **Gemini Enterprise** — licencia + rol IAM sobre la app del área.
2. **A2A OAuth** — el usuario consiente `a2a:invoke` en VirtuAI (Authorization Code + PKCE).
3. **Conectores** — OAuth individual por MCP; IAM de servicio para Cloud Run con autorización de negocio en backend.
4. **Datos/acciones** — ACL de origen, RBAC, filas y aprobación humana.
