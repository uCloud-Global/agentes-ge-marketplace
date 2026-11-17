# Arquitectura - Lead Qualification Agent

**Área:** Ventas - **Harness:** Deep - **Acceso:** Escritura con aprobación - **Complejidad:** 3/5 (media) - **Impacto:** 4/5 (alto)

## 1. Arquitectura (inputs → configuración → tools → outputs)

```mermaid
flowchart LR
  subgraph IN["Inputs"]
    direction TB
    U(["Usuario corporativo autenticado"])
    Q["Solicitud: Clasifica los leads entrantes y dime cuáles necesita contactar ventas hoy."]
    DOCS[/"Documentos: ICP, Reglas MQL/SQL, Historial comercial"/]
  end
  subgraph GE["Gemini Enterprise"]
    direction TB
    APP["App ge-ventas - Custom agent via A2A"]
  end
  subgraph VA["VirtuAI - Lead Qualification Agent"]
    direction TB
    GOV{"Governance check: permisos, budget, guardrails"}
    LOOP(("Agentic loop Deep"))
    subgraph CFG["Configuración"]
      direction TB
      H["Harness: Deep - Gemini Pro - T=0.2 - max 5000 tok"]
      SP["System prompt: AGENTS.md"]
      SK["Skills: lead-scoring, icp-fit-explainer, lead-routing"]
      KB[("KB kb-lead-qualification")]
      MEM["Memoria 16 KB - sin PII"]
      GR["Guardrails: prompt_injection, off_topic, sql_risk"]
      SEC["Security: Ask before each call - HITL"]
    end
  end
  subgraph TL["Tools"]
    direction TB
    T_mcp_hubspot["MCP predefinido - HubSpot<br/>find_contact<br/>create_sales_task (Ask)"]
    T_mcp_bigquery["MCP predefinido - BigQuery<br/>get_lead_signals"]
    T_mcp_gmail["MCP predefinido - Gmail<br/>search_mail"]
    T_custom["Custom Tool HTTP - Cloud Run (IAM)<br/>score_lead"]
  end
  subgraph SYS["Sistemas externos"]
    direction TB
    S_mcp_hubspot[("HubSpot CRM")]
    S_mcp_bigquery[("BigQuery")]
    S_mcp_gmail[("Gmail")]
    S_custom[("API privada / Cloud Run")]
  end
  subgraph OUT["Outputs"]
    direction TB
    O1["Ranking de leads, score explicable y tareas pendientes de aprobación."]
    O2["Aprobaciones input-required"]
    O3["Worklog - auditoría - métricas de uso"]
    O4["KPI: Tiempo a primer contacto, % leads calificados."]
  end
  U --> Q --> APP
  APP -->|"A2A JSON-RPC + OAuth a2a:invoke"| GOV --> LOOP
  CFG -.-> LOOP
  DOCS -.->|"indexación"| KB
  LOOP -->|Ask / aprobación| T_mcp_hubspot
  T_mcp_hubspot -->|OAuth por usuario| S_mcp_hubspot
  LOOP --> T_mcp_bigquery
  T_mcp_bigquery -->|OAuth por usuario| S_mcp_bigquery
  LOOP --> T_mcp_gmail
  T_mcp_gmail -->|OAuth por usuario| S_mcp_gmail
  LOOP --> T_custom
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
  class T_mcp_hubspot,T_mcp_bigquery,T_mcp_gmail,T_custom tool
```

## 2. Secuencia de una ejecución (Gemini Enterprise → A2A → VirtuAI)

```mermaid
sequenceDiagram
  autonumber
  actor U as Usuario
  participant GE as Gemini Enterprise
  participant V as VirtuAI - agente
  participant P_mcp_hubspot as HubSpot
  participant P_mcp_bigquery as BigQuery
  participant P_mcp_gmail as Gmail
  participant P_custom as Custom Tool
  U->>GE: Clasifica los leads entrantes y dime cuáles necesita contactar ventas hoy.
  GE->>V: A2A message/stream (Bearer, scope a2a:invoke)
  V->>V: Governance check y carga de skill lead-scoring
  loop Workflow: Capturar lead → Validar identidad → Evaluar encaje
    V->>P_mcp_hubspot: find_contact
    P_mcp_hubspot-->>V: datos (permisos del usuario)
    V->>P_mcp_bigquery: get_lead_signals
    P_mcp_bigquery-->>V: datos (permisos del usuario)
    V->>P_mcp_gmail: search_mail
    P_mcp_gmail-->>V: datos (permisos del usuario)
    V->>P_custom: score_lead
    P_custom-->>V: datos (permisos del usuario)
  end
  V-->>GE: task input-required (vista previa + approval_requests)
  GE-->>U: Solicitud de aprobación
  alt Aprobado
    U->>GE: Aprobar
    GE->>V: respuesta de aprobación
    V->>P_mcp_hubspot: create_sales_task (request_id)
    P_mcp_hubspot-->>V: OK + ID
  else Denegado o expira
    V->>V: acción queda pendiente, sin reintento
  end
  V-->>GE: Ranking de leads, score explicable y tareas pendientes de aprobación.
  GE-->>U: Respuesta con fuentes y limitaciones
```

## 3. Workflow de la skill principal `lead-scoring`

```mermaid
flowchart TD
  S0["1. Recuperar leads del periodo y deduplicar con find_contact"]
  S0 -.-> X0_find_contact[["find_contact<br/>HubSpot"]]
  S1["2. Obtener señales con get_lead_signals"]
  S0 --> S1
  S1 -.-> X1_get_lead_signals[["get_lead_signals<br/>BigQuery"]]
  S2["3. Calcular score con score_lead (reglas versionadas, no a criterio del modelo)"]
  S1 --> S2
  S2 -.-> X2_score_lead[["score_lead<br/>Custom Tool"]]
  S3["4. Explicar score: señales presentes, ausentes y peso"]
  S2 --> S3
  S4["5. Proponer tareas para leads SQL y pedir aprobación antes de create_sales_task"]
  S3 --> S4
  S4 -.-> X4_create_sales_task[["create_sales_task<br/>HubSpot"]]
  style X4_create_sales_task fill:#fce8e6,stroke:#ea4335
  S4 --> R(["Ranking - score - categoría MQL/SQL - señales usadas - datos faltantes - tarea propuesta"])
```

## 4. Matriz de inputs, configuración, tools y outputs

| Inputs | Configuración | Tools | Outputs |
|---|---|---|---|
| Solicitud en lenguaje natural vía Gemini Enterprise<br>Identidad del usuario (OAuth A2A)<br>Tokens OAuth por conector<br>Doc: ICP<br>Doc: Reglas MQL/SQL<br>Doc: Historial comercial | Harness **Deep**<br>Modelo Gemini Pro - T=0.2<br>System prompt `AGENTS.md`<br>Skills: `lead-scoring`, `icp-fit-explainer`, `lead-routing`<br>KB `kb-lead-qualification`<br>Guardrails: prompt_injection, off_topic, sql_risk<br>Memoria sin PII | `find_contact` (HubSpot)<br>`get_lead_signals` (BigQuery)<br>`search_mail` (Gmail)<br>`score_lead` (Custom Tool)<br>`create_sales_task` (HubSpot, Ask) | Ranking de leads, score explicable y tareas pendientes de aprobación.<br>Worklog y auditoría en VirtuAI<br>Acciones pendientes de aprobación |

## 5. Capas de identidad

1. **Gemini Enterprise** — licencia + rol IAM sobre la app del área.
2. **A2A OAuth** — el usuario consiente `a2a:invoke` en VirtuAI (Authorization Code + PKCE).
3. **Conectores** — OAuth individual por MCP; IAM de servicio para Cloud Run con autorización de negocio en backend.
4. **Datos/acciones** — ACL de origen, RBAC, filas y aprobación humana.
