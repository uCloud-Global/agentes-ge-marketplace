# Arquitectura - Compliance Control Monitor

**Área:** Legal - **Harness:** Deep - **Acceso:** Escritura con aprobación - **Complejidad:** 3/5 (media) - **Impacto:** 4/5 (alto)

## 1. Arquitectura (inputs → configuración → tools → outputs)

```mermaid
flowchart LR
  subgraph IN["Inputs"]
    direction TB
    U(["Usuario corporativo autenticado"])
    Q["Solicitud: ¿Qué controles de cumplimiento tienen evidencia incompleta este mes?"]
    DOCS[/"Documentos: Matriz controles, Manual compliance, Calendario de obligaciones"/]
  end
  subgraph GE["Gemini Enterprise"]
    direction TB
    APP["App ge-legal - Custom agent via A2A"]
  end
  subgraph VA["VirtuAI - Compliance Control Monitor"]
    direction TB
    GOV{"Governance check: permisos, budget, guardrails"}
    LOOP(("Agentic loop Deep"))
    subgraph CFG["Configuración"]
      direction TB
      H["Harness: Deep - Gemini Pro - T=0.1 - max 6000 tok"]
      SP["System prompt: AGENTS.md"]
      SK["Skills: control-audit, deadline-watch, evidence-quality-check"]
      KB[("KB kb-compliance-monitor")]
      MEM["Memoria 16 KB - sin PII"]
      GR["Guardrails: prompt_injection, off_topic, sql_risk"]
      SEC["Security: Ask before each call - HITL"]
    end
  end
  subgraph TL["Tools"]
    direction TB
    T_custom["Custom Tool HTTP - Cloud Run (IAM)<br/>get_controls"]
    T_mcp_drive["MCP predefinido - Google Drive<br/>find_evidence"]
    T_mcp_bigquery["MCP predefinido - BigQuery<br/>query_obligations"]
    T_mcp_gmail["MCP predefinido - Gmail<br/>create_alert (Ask)"]
  end
  subgraph SYS["Sistemas externos"]
    direction TB
    S_custom[("API privada / Cloud Run")]
    S_mcp_drive[("Google Drive")]
    S_mcp_bigquery[("BigQuery")]
    S_mcp_gmail[("Gmail")]
  end
  subgraph OUT["Outputs"]
    direction TB
    O1["Registro de brechas, responsables y plan de remediación."]
    O2["Aprobaciones input-required"]
    O3["Worklog - auditoría - métricas de uso"]
    O4["KPI: % controles al día, tiempo de auditoría."]
  end
  U --> Q --> APP
  APP -->|"A2A JSON-RPC + OAuth a2a:invoke"| GOV --> LOOP
  CFG -.-> LOOP
  DOCS -.->|"indexación"| KB
  LOOP --> T_custom
  T_custom -->|IAM run.invoker| S_custom
  LOOP --> T_mcp_drive
  T_mcp_drive -->|OAuth por usuario| S_mcp_drive
  LOOP --> T_mcp_bigquery
  T_mcp_bigquery -->|OAuth por usuario| S_mcp_bigquery
  LOOP -->|Ask / aprobación| T_mcp_gmail
  T_mcp_gmail -->|OAuth por usuario| S_mcp_gmail
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
  class T_custom,T_mcp_drive,T_mcp_bigquery,T_mcp_gmail tool
```

## 2. Secuencia de una ejecución (Gemini Enterprise → A2A → VirtuAI)

```mermaid
sequenceDiagram
  autonumber
  actor U as Usuario
  participant GE as Gemini Enterprise
  participant V as VirtuAI - agente
  participant P_custom as Custom Tool
  participant P_mcp_drive as Google Drive
  participant P_mcp_bigquery as BigQuery
  participant P_mcp_gmail as Gmail
  U->>GE: ¿Qué controles de cumplimiento tienen evidencia incompleta este mes?
  GE->>V: A2A message/stream (Bearer, scope a2a:invoke)
  V->>V: Governance check y carga de skill control-audit
  loop Workflow: Consultar controles → Revisar evidencias → Detectar faltantes
    V->>P_custom: get_controls
    P_custom-->>V: datos (permisos del usuario)
    V->>P_mcp_drive: find_evidence
    P_mcp_drive-->>V: datos (permisos del usuario)
    V->>P_mcp_bigquery: query_obligations
    P_mcp_bigquery-->>V: datos (permisos del usuario)
  end
  V->>V: draft_remediation (modelo)
  V-->>GE: task input-required (vista previa + approval_requests)
  GE-->>U: Solicitud de aprobación
  alt Aprobado
    U->>GE: Aprobar
    GE->>V: respuesta de aprobación
    V->>P_mcp_gmail: create_alert (request_id)
    P_mcp_gmail-->>V: OK + ID
  else Denegado o expira
    V->>V: acción queda pendiente, sin reintento
  end
  V-->>GE: Registro de brechas, responsables y plan de remediación.
  GE-->>U: Respuesta con fuentes y limitaciones
```

## 3. Workflow de la skill principal `control-audit`

```mermaid
flowchart TD
  S0["1. Leer controles con get_controls"]
  S0 -.-> X0_get_controls[["get_controls<br/>Custom Tool"]]
  S1["2. Buscar evidencia por control con find_evidence"]
  S0 --> S1
  S1 -.-> X1_find_evidence[["find_evidence<br/>Google Drive"]]
  S2["3. Clasificar: completa, incompleta, vencida, sin evidencia"]
  S1 --> S2
  S3["4. Priorizar por criticidad"]
  S2 --> S3
  S4["5. Preparar remediación y alertas en borrador"]
  S3 --> S4
  S4 --> R(["Registro de brechas - responsable - criticidad - plan de remediación"])
```

## 4. Matriz de inputs, configuración, tools y outputs

| Inputs | Configuración | Tools | Outputs |
|---|---|---|---|
| Solicitud en lenguaje natural vía Gemini Enterprise<br>Identidad del usuario (OAuth A2A)<br>Tokens OAuth por conector<br>Doc: Matriz controles<br>Doc: Manual compliance<br>Doc: Calendario de obligaciones | Harness **Deep**<br>Modelo Gemini Pro - T=0.1<br>System prompt `AGENTS.md`<br>Skills: `control-audit`, `deadline-watch`, `evidence-quality-check`<br>KB `kb-compliance-monitor`<br>Guardrails: prompt_injection, off_topic, sql_risk<br>Memoria sin PII | `get_controls` (Custom Tool)<br>`find_evidence` (Google Drive)<br>`query_obligations` (BigQuery)<br>`draft_remediation` (Modelo)<br>`create_alert` (Gmail, Ask) | Registro de brechas, responsables y plan de remediación.<br>Worklog y auditoría en VirtuAI<br>Acciones pendientes de aprobación |

## 5. Capas de identidad

1. **Gemini Enterprise** — licencia + rol IAM sobre la app del área.
2. **A2A OAuth** — el usuario consiente `a2a:invoke` en VirtuAI (Authorization Code + PKCE).
3. **Conectores** — OAuth individual por MCP; IAM de servicio para Cloud Run con autorización de negocio en backend.
4. **Datos/acciones** — ACL de origen, RBAC, filas y aprobación humana.
