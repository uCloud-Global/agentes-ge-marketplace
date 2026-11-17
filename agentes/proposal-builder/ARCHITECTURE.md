# Arquitectura - Commercial Proposal Studio

**Área:** Ventas - **Harness:** Deep - **Acceso:** Escritura con aprobación - **Complejidad:** 4/5 (alta) - **Impacto:** 4/5 (alto)

## 1. Arquitectura (inputs → configuración → tools → outputs)

```mermaid
flowchart LR
  subgraph IN["Inputs"]
    direction TB
    U(["Usuario corporativo autenticado"])
    Q["Solicitud: Prepara una propuesta de servicios para la oportunidad ACME en HubSpot."]
    DOCS[/"Documentos: Tarifas vigentes, Portafolio, Plantillas de propuesta, Términos estándar"/]
  end
  subgraph GE["Gemini Enterprise"]
    direction TB
    APP["App ge-ventas - Custom agent via A2A"]
  end
  subgraph VA["VirtuAI - Commercial Proposal Studio"]
    direction TB
    GOV{"Governance check: permisos, budget, guardrails"}
    LOOP(("Agentic loop Deep"))
    subgraph CFG["Configuración"]
      direction TB
      H["Harness: Deep - Gemini Pro - T=0.4 - max 10000 tok"]
      SP["System prompt: AGENTS.md"]
      SK["Skills: proposal-writing, scope-estimator, pricing-guardrail"]
      KB[("KB kb-proposal-builder")]
      MEM["Memoria 16 KB - sin PII"]
      GR["Guardrails: prompt_injection, off_topic"]
      SEC["Security: Ask before each call - HITL"]
    end
  end
  subgraph TL["Tools"]
    direction TB
    T_mcp_hubspot["MCP predefinido - HubSpot<br/>get_company"]
    T_mcp_bigquery["MCP predefinido - BigQuery<br/>get_rate_card"]
    T_mcp_drive["MCP predefinido - Google Drive<br/>search_templates"]
    T_custom["Custom Tool HTTP - Cloud Run (IAM)<br/>create_doc (Ask)"]
  end
  subgraph SYS["Sistemas externos"]
    direction TB
    S_mcp_hubspot[("HubSpot CRM")]
    S_mcp_bigquery[("BigQuery")]
    S_mcp_drive[("Google Drive")]
    S_custom[("API privada / Cloud Run")]
  end
  subgraph OUT["Outputs"]
    direction TB
    O1["Documento comercial estructurado con supuestos, precio sujeto a validación y entregables."]
    O2["Aprobaciones input-required"]
    O3["Worklog - auditoría - métricas de uso"]
    O4["KPI: Tiempo por propuesta, retrabajo de ofertas."]
  end
  U --> Q --> APP
  APP -->|"A2A JSON-RPC + OAuth a2a:invoke"| GOV --> LOOP
  CFG -.-> LOOP
  DOCS -.->|"indexación"| KB
  LOOP --> T_mcp_hubspot
  T_mcp_hubspot -->|OAuth por usuario| S_mcp_hubspot
  LOOP --> T_mcp_bigquery
  T_mcp_bigquery -->|OAuth por usuario| S_mcp_bigquery
  LOOP --> T_mcp_drive
  T_mcp_drive -->|OAuth por usuario| S_mcp_drive
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
  class T_mcp_hubspot,T_mcp_bigquery,T_mcp_drive,T_custom tool
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
  participant P_mcp_drive as Google Drive
  participant P_custom as Custom Tool
  U->>GE: Prepara una propuesta de servicios para la oportunidad ACME en HubSpot.
  GE->>V: A2A message/stream (Bearer, scope a2a:invoke)
  V->>V: Governance check y carga de skill proposal-writing
  loop Workflow: Buscar oportunidad → Seleccionar servicios → Estimar alcance
    V->>P_mcp_hubspot: get_company
    P_mcp_hubspot-->>V: datos (permisos del usuario)
    V->>P_mcp_bigquery: get_rate_card
    P_mcp_bigquery-->>V: datos (permisos del usuario)
    V->>P_mcp_drive: search_templates
    P_mcp_drive-->>V: datos (permisos del usuario)
  end
  V->>V: draft_proposal (modelo)
  V-->>GE: task input-required (vista previa + approval_requests)
  GE-->>U: Solicitud de aprobación
  alt Aprobado
    U->>GE: Aprobar
    GE->>V: respuesta de aprobación
    V->>P_custom: create_doc (request_id)
    P_custom-->>V: OK + ID
  else Denegado o expira
    V->>V: acción queda pendiente, sin reintento
  end
  V-->>GE: Documento comercial estructurado con supuestos, precio sujeto a validación y en…
  GE-->>U: Respuesta con fuentes y limitaciones
```

## 3. Workflow de la skill principal `proposal-writing`

```mermaid
flowchart TD
  S0["1. Leer contexto del cliente y del deal con get_company"]
  S0 -.-> X0_get_company[["get_company<br/>HubSpot"]]
  S1["2. Seleccionar servicios del portafolio que responden a la necesidad"]
  S0 --> S1
  S2["3. Estimar alcance y obtener precios exclusivamente con get_rate_card"]
  S1 --> S2
  S2 -.-> X2_get_rate_card[["get_rate_card<br/>BigQuery"]]
  S3["4. Redactar con draft_proposal usando plantilla y términos estándar"]
  S2 --> S3
  S3 -.-> X3_draft_proposal[["draft_proposal<br/>Modelo"]]
  S4["5. Mostrar vista previa y pedir aprobación antes de create_doc"]
  S3 --> S4
  S4 -.-> X4_create_doc[["create_doc<br/>Custom Tool"]]
  style X4_create_doc fill:#fce8e6,stroke:#ea4335
  S4 --> R(["Propuesta: contexto, solución, alcance, entregables, cronograma, precio (sujeto a validac…"])
```

## 4. Matriz de inputs, configuración, tools y outputs

| Inputs | Configuración | Tools | Outputs |
|---|---|---|---|
| Solicitud en lenguaje natural vía Gemini Enterprise<br>Identidad del usuario (OAuth A2A)<br>Tokens OAuth por conector<br>Doc: Tarifas vigentes<br>Doc: Portafolio<br>Doc: Plantillas de propuesta<br>Doc: Términos estándar | Harness **Deep**<br>Modelo Gemini Pro - T=0.4<br>System prompt `AGENTS.md`<br>Skills: `proposal-writing`, `scope-estimator`, `pricing-guardrail`<br>KB `kb-proposal-builder`<br>Guardrails: prompt_injection, off_topic<br>Memoria sin PII | `get_company` (HubSpot)<br>`get_rate_card` (BigQuery)<br>`search_templates` (Google Drive)<br>`draft_proposal` (Modelo)<br>`create_doc` (Custom Tool, Ask) | Documento comercial estructurado con supuestos, precio sujeto a validación y entregables.<br>Worklog y auditoría en VirtuAI<br>Acciones pendientes de aprobación |

## 5. Capas de identidad

1. **Gemini Enterprise** — licencia + rol IAM sobre la app del área.
2. **A2A OAuth** — el usuario consiente `a2a:invoke` en VirtuAI (Authorization Code + PKCE).
3. **Conectores** — OAuth individual por MCP; IAM de servicio para Cloud Run con autorización de negocio en backend.
4. **Datos/acciones** — ACL de origen, RBAC, filas y aprobación humana.
