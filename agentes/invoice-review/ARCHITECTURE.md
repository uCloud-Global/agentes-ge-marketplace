# Arquitectura - Accounts Payable Reviewer

**Área:** Finanzas - **Harness:** Deep - **Acceso:** Escritura con aprobación - **Complejidad:** 5/5 (muy alta) - **Impacto:** 5/5 (muy alto)

## 1. Arquitectura (inputs → configuración → tools → outputs)

```mermaid
flowchart LR
  subgraph IN["Inputs"]
    direction TB
    U(["Usuario corporativo autenticado"])
    Q["Solicitud: Revisa las facturas recibidas hoy y detecta diferencias frente a sus órdenes."]
    DOCS[/"Documentos: Política de compras, Órdenes de compra, Condiciones de pago"/]
  end
  subgraph GE["Gemini Enterprise"]
    direction TB
    APP["App ge-finanzas - Custom agent via A2A"]
  end
  subgraph VA["VirtuAI - Accounts Payable Reviewer"]
    direction TB
    GOV{"Governance check: permisos, budget, guardrails"}
    LOOP(("Agentic loop Deep"))
    subgraph CFG["Configuración"]
      direction TB
      H["Harness: Deep - Gemini Pro - T=0.1 - max 6000 tok"]
      SP["System prompt: AGENTS.md"]
      SK["Skills: invoice-matching, vendor-bank-change-alert, duplicate-invoice-check"]
      KB[("KB kb-invoice-review")]
      MEM["Memoria 16 KB - sin PII"]
      GR["Guardrails: prompt_injection, off_topic, sql_risk"]
      SEC["Security: Ask before each call - HITL"]
    end
  end
  subgraph TL["Tools"]
    direction TB
    T_custom["Custom Tool HTTP - Cloud Run (IAM)<br/>extract_invoice<br/>check_vendor<br/>create_review_case (Ask)"]
    T_mcp_bigquery["MCP predefinido - BigQuery<br/>match_po"]
    T_mcp_gmail["MCP predefinido - Gmail<br/>search_invoices_mail"]
  end
  subgraph SYS["Sistemas externos"]
    direction TB
    S_custom[("API privada / Cloud Run")]
    S_mcp_bigquery[("BigQuery")]
    S_mcp_gmail[("Gmail")]
  end
  subgraph OUT["Outputs"]
    direction TB
    O1["Informe de coincidencias, excepciones y borradores de casos de revisión."]
    O2["Aprobaciones input-required"]
    O3["Worklog - auditoría - métricas de uso"]
    O4["KPI: Tiempo por factura, % errores detectados."]
  end
  U --> Q --> APP
  APP -->|"A2A JSON-RPC + OAuth a2a:invoke"| GOV --> LOOP
  CFG -.-> LOOP
  DOCS -.->|"indexación"| KB
  LOOP -->|Ask / aprobación| T_custom
  T_custom -->|IAM run.invoker| S_custom
  LOOP --> T_mcp_bigquery
  T_mcp_bigquery -->|OAuth por usuario| S_mcp_bigquery
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
  class T_custom,T_mcp_bigquery,T_mcp_gmail tool
```

## 2. Secuencia de una ejecución (Gemini Enterprise → A2A → VirtuAI)

```mermaid
sequenceDiagram
  autonumber
  actor U as Usuario
  participant GE as Gemini Enterprise
  participant V as VirtuAI - agente
  participant P_custom as Custom Tool
  participant P_mcp_bigquery as BigQuery
  participant P_mcp_gmail as Gmail
  U->>GE: Revisa las facturas recibidas hoy y detecta diferencias frente a sus órdenes.
  GE->>V: A2A message/stream (Bearer, scope a2a:invoke)
  V->>V: Governance check y carga de skill invoice-matching
  loop Workflow: Leer factura → Cruzar orden → Validar proveedor
    V->>P_custom: extract_invoice
    P_custom-->>V: datos (permisos del usuario)
    V->>P_mcp_bigquery: match_po
    P_mcp_bigquery-->>V: datos (permisos del usuario)
    V->>P_custom: check_vendor
    P_custom-->>V: datos (permisos del usuario)
    V->>P_mcp_gmail: search_invoices_mail
    P_mcp_gmail-->>V: datos (permisos del usuario)
  end
  V-->>GE: task input-required (vista previa + approval_requests)
  GE-->>U: Solicitud de aprobación
  alt Aprobado
    U->>GE: Aprobar
    GE->>V: respuesta de aprobación
    V->>P_custom: create_review_case (request_id)
    P_custom-->>V: OK + ID
  else Denegado o expira
    V->>V: acción queda pendiente, sin reintento
  end
  V-->>GE: Informe de coincidencias, excepciones y borradores de casos de revisión.
  GE-->>U: Respuesta con fuentes y limitaciones
```

## 3. Workflow de la skill principal `invoice-matching`

```mermaid
flowchart TD
  S0["1. Localizar facturas del periodo"]
  S1["2. Extraer campos con extract_invoice"]
  S0 --> S1
  S1 -.-> X1_extract_invoice[["extract_invoice<br/>Custom Tool"]]
  S2["3. Cruzar contra OC y recepción con match_po (cantidad, precio, impuestos)"]
  S1 --> S2
  S2 -.-> X2_match_po[["match_po<br/>BigQuery"]]
  S3["4. Validar proveedor con check_vendor"]
  S2 --> S3
  S3 -.-> X3_check_vendor[["check_vendor<br/>Custom Tool"]]
  S4["5. Clasificar: conforme, excepción menor, excepción mayor"]
  S3 --> S4
  S5["6. Proponer casos de revisión y pedir aprobación antes de create_review_case"]
  S4 --> S5
  S5 -.-> X5_create_review_case[["create_review_case<br/>Custom Tool"]]
  style X5_create_review_case fill:#fce8e6,stroke:#ea4335
  S5 --> R(["Tabla factura - OC - diferencias (cantidad/precio/impuesto) - severidad - caso propuesto"])
```

## 4. Matriz de inputs, configuración, tools y outputs

| Inputs | Configuración | Tools | Outputs |
|---|---|---|---|
| Solicitud en lenguaje natural vía Gemini Enterprise<br>Identidad del usuario (OAuth A2A)<br>Tokens OAuth por conector<br>Doc: Política de compras<br>Doc: Órdenes de compra<br>Doc: Condiciones de pago | Harness **Deep**<br>Modelo Gemini Pro - T=0.1<br>System prompt `AGENTS.md`<br>Skills: `invoice-matching`, `vendor-bank-change-alert`, `duplicate-invoice-check`<br>KB `kb-invoice-review`<br>Guardrails: prompt_injection, off_topic, sql_risk<br>Memoria sin PII | `extract_invoice` (Custom Tool)<br>`match_po` (BigQuery)<br>`check_vendor` (Custom Tool)<br>`search_invoices_mail` (Gmail)<br>`create_review_case` (Custom Tool, Ask) | Informe de coincidencias, excepciones y borradores de casos de revisión.<br>Worklog y auditoría en VirtuAI<br>Acciones pendientes de aprobación |

## 5. Capas de identidad

1. **Gemini Enterprise** — licencia + rol IAM sobre la app del área.
2. **A2A OAuth** — el usuario consiente `a2a:invoke` en VirtuAI (Authorization Code + PKCE).
3. **Conectores** — OAuth individual por MCP; IAM de servicio para Cloud Run con autorización de negocio en backend.
4. **Datos/acciones** — ACL de origen, RBAC, filas y aprobación humana.
