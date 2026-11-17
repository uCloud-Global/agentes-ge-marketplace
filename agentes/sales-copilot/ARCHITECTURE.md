# Arquitectura - Sales CRM Copilot

**Área:** Ventas - **Harness:** Deep - **Acceso:** Escritura con aprobación - **Complejidad:** 3/5 (media) - **Impacto:** 5/5 (muy alto)

## 1. Arquitectura (inputs → configuración → tools → outputs)

```mermaid
flowchart LR
  subgraph IN["Inputs"]
    direction TB
    U(["Usuario corporativo autenticado"])
    Q["Solicitud: Revisa mis 10 oportunidades en riesgo y prepara seguimientos personalizados."]
    DOCS[/"Documentos: Playbook comercial, Criterios de pipeline, Política de descuentos"/]
  end
  subgraph GE["Gemini Enterprise"]
    direction TB
    APP["App ge-ventas - Custom agent via A2A"]
  end
  subgraph VA["VirtuAI - Sales CRM Copilot"]
    direction TB
    GOV{"Governance check: permisos, budget, guardrails"}
    LOOP(("Agentic loop Deep"))
    subgraph CFG["Configuración"]
      direction TB
      H["Harness: Deep - Gemini Pro - T=0.3 - max 6000 tok"]
      SP["System prompt: AGENTS.md"]
      SK["Skills: sales-followup, deal-risk-review, crm-update-approval"]
      KB[("KB kb-sales-copilot")]
      MEM["Memoria 16 KB - sin PII"]
      GR["Guardrails: prompt_injection, off_topic, sentiment"]
      SEC["Security: Ask before each call - HITL"]
    end
  end
  subgraph TL["Tools"]
    direction TB
    T_mcp_hubspot["MCP predefinido - HubSpot<br/>search_deals<br/>get_contact_timeline<br/>update_deal_stage (Ask)"]
    T_mcp_calendar["MCP predefinido - Google Calendar<br/>list_meetings"]
    T_mcp_gmail["MCP predefinido - Gmail<br/>draft_followup (Ask)"]
  end
  subgraph SYS["Sistemas externos"]
    direction TB
    S_mcp_hubspot[("HubSpot CRM")]
    S_mcp_calendar[("Google Calendar")]
    S_mcp_gmail[("Gmail")]
  end
  subgraph OUT["Outputs"]
    direction TB
    O1["Tabla de deals en riesgo, correos borrador y actividades sugeridas."]
    O2["Aprobaciones input-required"]
    O3["Worklog - auditoría - métricas de uso"]
    O4["KPI: Tiempo por preparación, cobertura de seguimientos."]
  end
  U --> Q --> APP
  APP -->|"A2A JSON-RPC + OAuth a2a:invoke"| GOV --> LOOP
  CFG -.-> LOOP
  DOCS -.->|"indexación"| KB
  LOOP -->|Ask / aprobación| T_mcp_hubspot
  T_mcp_hubspot -->|OAuth por usuario| S_mcp_hubspot
  LOOP --> T_mcp_calendar
  T_mcp_calendar -->|OAuth por usuario| S_mcp_calendar
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
  class T_mcp_hubspot,T_mcp_calendar,T_mcp_gmail tool
```

## 2. Secuencia de una ejecución (Gemini Enterprise → A2A → VirtuAI)

```mermaid
sequenceDiagram
  autonumber
  actor U as Usuario
  participant GE as Gemini Enterprise
  participant V as VirtuAI - agente
  participant P_mcp_hubspot as HubSpot
  participant P_mcp_calendar as Google Calendar
  participant P_mcp_gmail as Gmail
  U->>GE: Revisa mis 10 oportunidades en riesgo y prepara seguimientos personalizados.
  GE->>V: A2A message/stream (Bearer, scope a2a:invoke)
  V->>V: Governance check y carga de skill sales-followup
  loop Workflow: Consultar oportunidad → Revisar interacciones → Evaluar probabilidad
    V->>P_mcp_hubspot: search_deals
    P_mcp_hubspot-->>V: datos (permisos del usuario)
    V->>P_mcp_hubspot: get_contact_timeline
    P_mcp_hubspot-->>V: datos (permisos del usuario)
    V->>P_mcp_calendar: list_meetings
    P_mcp_calendar-->>V: datos (permisos del usuario)
  end
  V-->>GE: task input-required (vista previa + approval_requests)
  GE-->>U: Solicitud de aprobación
  alt Aprobado
    U->>GE: Aprobar
    GE->>V: respuesta de aprobación
    V->>P_mcp_gmail: draft_followup (request_id)
    P_mcp_gmail-->>V: OK + ID
    V->>P_mcp_hubspot: update_deal_stage (request_id)
    P_mcp_hubspot-->>V: OK + ID
  else Denegado o expira
    V->>V: acción queda pendiente, sin reintento
  end
  V-->>GE: Tabla de deals en riesgo, correos borrador y actividades sugeridas.
  GE-->>U: Respuesta con fuentes y limitaciones
```

## 3. Workflow de la skill principal `sales-followup`

```mermaid
flowchart TD
  S0["1. Recuperar deals objetivo con search_deals"]
  S0 -.-> X0_search_deals[["search_deals<br/>HubSpot"]]
  S1["2. Leer timeline con get_contact_timeline y detectar última interacción y compromi…"]
  S0 --> S1
  S1 -.-> X1_get_contact_timeline[["get_contact_timeline<br/>HubSpot"]]
  S2["3. Proponer siguiente paso concreto por deal (reunión, propuesta, llamada)"]
  S1 --> S2
  S3["4. Crear borradores con draft_followup personalizados con contexto real"]
  S2 --> S3
  S3 -.-> X3_draft_followup[["draft_followup<br/>Gmail"]]
  style X3_draft_followup fill:#fce8e6,stroke:#ea4335
  S4["5. Presentar vista previa y pedir aprobación antes de cualquier update_deal_stage"]
  S3 --> S4
  S4 -.-> X4_update_deal_stage[["update_deal_stage<br/>HubSpot"]]
  style X4_update_deal_stage fill:#fce8e6,stroke:#ea4335
  S4 --> R(["Tabla deal - etapa - riesgo - próximo paso - borrador (enlace) - acción pendiente de apro…"])
```

## 4. Matriz de inputs, configuración, tools y outputs

| Inputs | Configuración | Tools | Outputs |
|---|---|---|---|
| Solicitud en lenguaje natural vía Gemini Enterprise<br>Identidad del usuario (OAuth A2A)<br>Tokens OAuth por conector<br>Doc: Playbook comercial<br>Doc: Criterios de pipeline<br>Doc: Política de descuentos | Harness **Deep**<br>Modelo Gemini Pro - T=0.3<br>System prompt `AGENTS.md`<br>Skills: `sales-followup`, `deal-risk-review`, `crm-update-approval`<br>KB `kb-sales-copilot`<br>Guardrails: prompt_injection, off_topic, sentiment<br>Memoria sin PII | `search_deals` (HubSpot)<br>`get_contact_timeline` (HubSpot)<br>`list_meetings` (Google Calendar)<br>`draft_followup` (Gmail, Ask)<br>`update_deal_stage` (HubSpot, Ask) | Tabla de deals en riesgo, correos borrador y actividades sugeridas.<br>Worklog y auditoría en VirtuAI<br>Acciones pendientes de aprobación |

## 5. Capas de identidad

1. **Gemini Enterprise** — licencia + rol IAM sobre la app del área.
2. **A2A OAuth** — el usuario consiente `a2a:invoke` en VirtuAI (Authorization Code + PKCE).
3. **Conectores** — OAuth individual por MCP; IAM de servicio para Cloud Run con autorización de negocio en backend.
4. **Datos/acciones** — ACL de origen, RBAC, filas y aprobación humana.
