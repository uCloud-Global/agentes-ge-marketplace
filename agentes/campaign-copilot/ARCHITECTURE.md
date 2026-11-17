# Arquitectura - Campaign Launch Copilot

**Área:** Marketing - **Harness:** Deep - **Acceso:** Escritura con aprobación - **Complejidad:** 4/5 (alta) - **Impacto:** 3/5 (medio)

## 1. Arquitectura (inputs → configuración → tools → outputs)

```mermaid
flowchart LR
  subgraph IN["Inputs"]
    direction TB
    U(["Usuario corporativo autenticado"])
    Q["Solicitud: Diseña una campaña de reactivación para clientes sin actividad en 90 días."]
    DOCS[/"Documentos: Brandbook, Plan de campañas, Guía editorial, Segmentación"/]
  end
  subgraph GE["Gemini Enterprise"]
    direction TB
    APP["App ge-marketing - Custom agent via A2A"]
  end
  subgraph VA["VirtuAI - Campaign Launch Copilot"]
    direction TB
    GOV{"Governance check: permisos, budget, guardrails"}
    LOOP(("Agentic loop Deep"))
    subgraph CFG["Configuración"]
      direction TB
      H["Harness: Deep - Gemini Pro - T=0.6 - max 8000 tok"]
      SP["System prompt: AGENTS.md"]
      SK["Skills: campaign-planning, copy-variants, compliance-check"]
      KB[("KB kb-campaign-copilot")]
      MEM["Memoria 16 KB - sin PII"]
      GR["Guardrails: prompt_injection, off_topic"]
      SEC["Security: Ask before each call - HITL"]
    end
  end
  subgraph TL["Tools"]
    direction TB
    T_mcp_hubspot["MCP predefinido - HubSpot<br/>get_segments"]
    T_custom["Custom Tool HTTP - Cloud Run (IAM)<br/>read_campaign_metrics<br/>schedule_campaign (Ask)"]
    T_mcp_drive["MCP predefinido - Google Drive<br/>search_brand_assets"]
  end
  subgraph SYS["Sistemas externos"]
    direction TB
    S_mcp_hubspot[("HubSpot CRM")]
    S_custom[("API privada / Cloud Run")]
    S_mcp_drive[("Google Drive")]
  end
  subgraph OUT["Outputs"]
    direction TB
    O1["Brief, segmentos, asuntos A/B, borradores y calendario editorial."]
    O2["Aprobaciones input-required"]
    O3["Worklog - auditoría - métricas de uso"]
    O4["KPI: Tiempo de preparación, tasa de respuesta."]
  end
  U --> Q --> APP
  APP -->|"A2A JSON-RPC + OAuth a2a:invoke"| GOV --> LOOP
  CFG -.-> LOOP
  DOCS -.->|"indexación"| KB
  LOOP --> T_mcp_hubspot
  T_mcp_hubspot -->|OAuth por usuario| S_mcp_hubspot
  LOOP -->|Ask / aprobación| T_custom
  T_custom -->|IAM run.invoker| S_custom
  LOOP --> T_mcp_drive
  T_mcp_drive -->|OAuth por usuario| S_mcp_drive
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
  class T_mcp_hubspot,T_custom,T_mcp_drive tool
```

## 2. Secuencia de una ejecución (Gemini Enterprise → A2A → VirtuAI)

```mermaid
sequenceDiagram
  autonumber
  actor U as Usuario
  participant GE as Gemini Enterprise
  participant V as VirtuAI - agente
  participant P_mcp_hubspot as HubSpot
  participant P_custom as Custom Tool
  participant P_mcp_drive as Google Drive
  U->>GE: Diseña una campaña de reactivación para clientes sin actividad en 90 días.
  GE->>V: A2A message/stream (Bearer, scope a2a:invoke)
  V->>V: Governance check y carga de skill campaign-planning
  loop Workflow: Definir objetivo → Analizar audiencias → Redactar piezas
    V->>P_mcp_hubspot: get_segments
    P_mcp_hubspot-->>V: datos (permisos del usuario)
    V->>P_custom: read_campaign_metrics
    P_custom-->>V: datos (permisos del usuario)
    V->>P_mcp_drive: search_brand_assets
    P_mcp_drive-->>V: datos (permisos del usuario)
  end
  V->>V: draft_assets (modelo)
  V-->>GE: task input-required (vista previa + approval_requests)
  GE-->>U: Solicitud de aprobación
  alt Aprobado
    U->>GE: Aprobar
    GE->>V: respuesta de aprobación
    V->>P_custom: schedule_campaign (request_id)
    P_custom-->>V: OK + ID
  else Denegado o expira
    V->>V: acción queda pendiente, sin reintento
  end
  V-->>GE: Brief, segmentos, asuntos A/B, borradores y calendario editorial.
  GE-->>U: Respuesta con fuentes y limitaciones
```

## 3. Workflow de la skill principal `campaign-planning`

```mermaid
flowchart TD
  S0["1. Definir objetivo, KPI y audiencia"]
  S1["2. Analizar segmentos con get_segments y validar opt-in"]
  S0 --> S1
  S1 -.-> X1_get_segments[["get_segments<br/>HubSpot"]]
  S2["3. Revisar desempeño histórico con read_campaign_metrics"]
  S1 --> S2
  S2 -.-> X2_read_campaign_metrics[["read_campaign_metrics<br/>Custom Tool"]]
  S3["4. Redactar piezas con draft_assets alineadas al brandbook"]
  S2 --> S3
  S3 -.-> X3_draft_assets[["draft_assets<br/>Modelo"]]
  S4["5. Revisar cumplimiento (consentimiento, opt-out, claims)"]
  S3 --> S4
  S5["6. Proponer calendario y pedir aprobación antes de schedule_campaign"]
  S4 --> S5
  S5 -.-> X5_schedule_campaign[["schedule_campaign<br/>Custom Tool"]]
  style X5_schedule_campaign fill:#fce8e6,stroke:#ea4335
  S5 --> R(["Brief - segmentos - mensajes A/B - calendario - checklist de cumplimiento"])
```

## 4. Matriz de inputs, configuración, tools y outputs

| Inputs | Configuración | Tools | Outputs |
|---|---|---|---|
| Solicitud en lenguaje natural vía Gemini Enterprise<br>Identidad del usuario (OAuth A2A)<br>Tokens OAuth por conector<br>Doc: Brandbook<br>Doc: Plan de campañas<br>Doc: Guía editorial<br>Doc: Segmentación | Harness **Deep**<br>Modelo Gemini Pro - T=0.6<br>System prompt `AGENTS.md`<br>Skills: `campaign-planning`, `copy-variants`, `compliance-check`<br>KB `kb-campaign-copilot`<br>Guardrails: prompt_injection, off_topic<br>Memoria sin PII | `get_segments` (HubSpot)<br>`read_campaign_metrics` (Custom Tool)<br>`search_brand_assets` (Google Drive)<br>`draft_assets` (Modelo)<br>`schedule_campaign` (Custom Tool, Ask) | Brief, segmentos, asuntos A/B, borradores y calendario editorial.<br>Worklog y auditoría en VirtuAI<br>Acciones pendientes de aprobación |

## 5. Capas de identidad

1. **Gemini Enterprise** — licencia + rol IAM sobre la app del área.
2. **A2A OAuth** — el usuario consiente `a2a:invoke` en VirtuAI (Authorization Code + PKCE).
3. **Conectores** — OAuth individual por MCP; IAM de servicio para Cloud Run con autorización de negocio en backend.
4. **Datos/acciones** — ACL de origen, RBAC, filas y aprobación humana.
