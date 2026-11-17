# Arquitectura - Purchase Request Assistant

**Área:** Compras - **Harness:** Deep - **Acceso:** Escritura con aprobación - **Complejidad:** 4/5 (alta) - **Impacto:** 3/5 (medio)

## 1. Arquitectura (inputs → configuración → tools → outputs)

```mermaid
flowchart LR
  subgraph IN["Inputs"]
    direction TB
    U(["Usuario corporativo autenticado"])
    Q["Solicitud: Necesitamos 12 portátiles para un nuevo equipo: prepara la solicitud de compra."]
    DOCS[/"Documentos: Política de compras, Catálogo proveedores, Matriz de aprobación"/]
  end
  subgraph GE["Gemini Enterprise"]
    direction TB
    APP["App ge-compras - Custom agent via A2A"]
  end
  subgraph VA["VirtuAI - Purchase Request Assistant"]
    direction TB
    GOV{"Governance check: permisos, budget, guardrails"}
    LOOP(("Agentic loop Deep"))
    subgraph CFG["Configuración"]
      direction TB
      H["Harness: Deep - Gemini Pro - T=0.2 - max 5000 tok"]
      SP["System prompt: AGENTS.md"]
      SK["Skills: purchase-request, approval-matrix-check, quote-comparison"]
      KB[("KB kb-procurement-assistant")]
      MEM["Memoria 16 KB - sin PII"]
      GR["Guardrails: prompt_injection, off_topic"]
      SEC["Security: Ask before each call - HITL"]
    end
  end
  subgraph TL["Tools"]
    direction TB
    T_custom["Custom Tool HTTP - Cloud Run (IAM)<br/>get_catalog<br/>validate_budget<br/>submit_for_approval (Ask)"]
    T_mcp_gmail["MCP predefinido - Gmail<br/>search_requests_mail"]
  end
  subgraph SYS["Sistemas externos"]
    direction TB
    S_custom[("API privada / Cloud Run")]
    S_mcp_gmail[("Gmail")]
  end
  subgraph OUT["Outputs"]
    direction TB
    O1["Requisición estructurada, estimación de costo, checklist y aprobaciones."]
    O2["Aprobaciones input-required"]
    O3["Worklog - auditoría - métricas de uso"]
    O4["KPI: Tiempo de requisición, tasa de rechazos por datos incompletos."]
  end
  U --> Q --> APP
  APP -->|"A2A JSON-RPC + OAuth a2a:invoke"| GOV --> LOOP
  CFG -.-> LOOP
  DOCS -.->|"indexación"| KB
  LOOP -->|Ask / aprobación| T_custom
  T_custom -->|IAM run.invoker| S_custom
  LOOP --> T_mcp_gmail
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
  class T_custom,T_mcp_gmail tool
```

## 2. Secuencia de una ejecución (Gemini Enterprise → A2A → VirtuAI)

```mermaid
sequenceDiagram
  autonumber
  actor U as Usuario
  participant GE as Gemini Enterprise
  participant V as VirtuAI - agente
  participant P_custom as Custom Tool
  participant P_mcp_gmail as Gmail
  U->>GE: Necesitamos 12 portátiles para un nuevo equipo: prepara la solicitud de compra.
  GE->>V: A2A message/stream (Bearer, scope a2a:invoke)
  V->>V: Governance check y carga de skill purchase-request
  loop Workflow: Entender necesidad → Validar presupuesto → Buscar proveedor
    V->>P_custom: get_catalog
    P_custom-->>V: datos (permisos del usuario)
    V->>P_custom: validate_budget
    P_custom-->>V: datos (permisos del usuario)
    V->>P_mcp_gmail: search_requests_mail
    P_mcp_gmail-->>V: datos (permisos del usuario)
  end
  V->>V: draft_purchase_request (modelo)
  V-->>GE: task input-required (vista previa + approval_requests)
  GE-->>U: Solicitud de aprobación
  alt Aprobado
    U->>GE: Aprobar
    GE->>V: respuesta de aprobación
    V->>P_custom: submit_for_approval (request_id)
    P_custom-->>V: OK + ID
  else Denegado o expira
    V->>V: acción queda pendiente, sin reintento
  end
  V-->>GE: Requisición estructurada, estimación de costo, checklist y aprobaciones.
  GE-->>U: Respuesta con fuentes y limitaciones
```

## 3. Workflow de la skill principal `purchase-request`

```mermaid
flowchart TD
  S0["1. Entender necesidad, cantidad, fecha requerida y centro de costo"]
  S1["2. Validar presupuesto con validate_budget"]
  S0 --> S1
  S1 -.-> X1_validate_budget[["validate_budget<br/>Custom Tool"]]
  S2["3. Buscar ítems/proveedores homologados con get_catalog"]
  S1 --> S2
  S2 -.-> X2_get_catalog[["get_catalog<br/>Custom Tool"]]
  S3["4. Construir requisición con draft_purchase_request"]
  S2 --> S3
  S3 -.-> X3_draft_purchase_request[["draft_purchase_request<br/>Modelo"]]
  S4["5. Determinar aprobadores según matriz"]
  S3 --> S4
  S5["6. Pedir confirmación antes de submit_for_approval"]
  S4 --> S5
  S5 -.-> X5_submit_for_approval[["submit_for_approval<br/>Custom Tool"]]
  style X5_submit_for_approval fill:#fce8e6,stroke:#ea4335
  S5 --> R(["Requisición: ítems, cantidades, proveedor sugerido, costo estimado, centro de costo, apro…"])
```

## 4. Matriz de inputs, configuración, tools y outputs

| Inputs | Configuración | Tools | Outputs |
|---|---|---|---|
| Solicitud en lenguaje natural vía Gemini Enterprise<br>Identidad del usuario (OAuth A2A)<br>Tokens OAuth por conector<br>Doc: Política de compras<br>Doc: Catálogo proveedores<br>Doc: Matriz de aprobación | Harness **Deep**<br>Modelo Gemini Pro - T=0.2<br>System prompt `AGENTS.md`<br>Skills: `purchase-request`, `approval-matrix-check`, `quote-comparison`<br>KB `kb-procurement-assistant`<br>Guardrails: prompt_injection, off_topic<br>Memoria sin PII | `get_catalog` (Custom Tool)<br>`validate_budget` (Custom Tool)<br>`search_requests_mail` (Gmail)<br>`draft_purchase_request` (Modelo)<br>`submit_for_approval` (Custom Tool, Ask) | Requisición estructurada, estimación de costo, checklist y aprobaciones.<br>Worklog y auditoría en VirtuAI<br>Acciones pendientes de aprobación |

## 5. Capas de identidad

1. **Gemini Enterprise** — licencia + rol IAM sobre la app del área.
2. **A2A OAuth** — el usuario consiente `a2a:invoke` en VirtuAI (Authorization Code + PKCE).
3. **Conectores** — OAuth individual por MCP; IAM de servicio para Cloud Run con autorización de negocio en backend.
4. **Datos/acciones** — ACL de origen, RBAC, filas y aprobación humana.
