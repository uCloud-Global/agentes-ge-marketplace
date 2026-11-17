# Arquitectura - Customer Success Health

**Área:** Clientes - **Harness:** Deep - **Acceso:** Lectura - **Complejidad:** 3/5 (media) - **Impacto:** 4/5 (alto)

## 1. Arquitectura (inputs → configuración → tools → outputs)

```mermaid
flowchart LR
  subgraph IN["Inputs"]
    direction TB
    U(["Usuario corporativo autenticado"])
    Q["Solicitud: ¿Qué clientes están en riesgo de churn y qué acciones recomendarías?"]
    DOCS[/"Documentos: Playbooks CS, Definición health score, Contratos de servicio"/]
  end
  subgraph GE["Gemini Enterprise"]
    direction TB
    APP["App ge-clientes - Custom agent via A2A"]
  end
  subgraph VA["VirtuAI - Customer Success Health"]
    direction TB
    GOV{"Governance check: permisos, budget, guardrails"}
    LOOP(("Agentic loop Deep"))
    subgraph CFG["Configuración"]
      direction TB
      H["Harness: Deep - Gemini Pro - T=0.2 - max 6000 tok"]
      SP["System prompt: AGENTS.md"]
      SK["Skills: customer-health, renewal-prep, churn-signal-review"]
      KB[("KB kb-customer-health")]
      MEM["Memoria 16 KB - sin PII"]
      GR["Guardrails: prompt_injection, off_topic, sql_risk, shell_risk"]
      SEC["Security: Read-only"]
    end
  end
  subgraph TL["Tools"]
    direction TB
    T_mcp_bigquery["MCP predefinido - BigQuery<br/>get_account_usage"]
    T_mcp_hubspot["MCP predefinido - HubSpot<br/>get_support_history"]
    T_workstation["Deep Agent - Workstation / sandbox (Python)<br/>compute_health"]
  end
  subgraph SYS["Sistemas externos"]
    direction TB
    S_mcp_bigquery[("BigQuery")]
    S_mcp_hubspot[("HubSpot CRM")]
    S_workstation[("Entorno aislado")]
  end
  subgraph OUT["Outputs"]
    direction TB
    O1["Ranking de cuentas con señales, plan y nivel de confianza."]
    O3["Worklog - auditoría - métricas de uso"]
    O4["KPI: Retención neta, alertas oportunas."]
  end
  U --> Q --> APP
  APP -->|"A2A JSON-RPC + OAuth a2a:invoke"| GOV --> LOOP
  CFG -.-> LOOP
  DOCS -.->|"indexación"| KB
  LOOP --> T_mcp_bigquery
  T_mcp_bigquery -->|OAuth por usuario| S_mcp_bigquery
  LOOP --> T_mcp_hubspot
  T_mcp_hubspot -->|OAuth por usuario| S_mcp_hubspot
  LOOP --> T_workstation
  T_workstation --> S_workstation
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
  class T_mcp_bigquery,T_mcp_hubspot,T_workstation tool
```

## 2. Secuencia de una ejecución (Gemini Enterprise → A2A → VirtuAI)

```mermaid
sequenceDiagram
  autonumber
  actor U as Usuario
  participant GE as Gemini Enterprise
  participant V as VirtuAI - agente
  participant P_mcp_bigquery as BigQuery
  participant P_mcp_hubspot as HubSpot
  participant P_workstation as Workstation
  U->>GE: ¿Qué clientes están en riesgo de churn y qué acciones recomendarías?
  GE->>V: A2A message/stream (Bearer, scope a2a:invoke)
  V->>V: Governance check y carga de skill customer-health
  loop Workflow: Consultar uso → Analizar tickets → Estimar riesgo
    V->>P_mcp_bigquery: get_account_usage
    P_mcp_bigquery-->>V: datos (permisos del usuario)
    V->>P_mcp_hubspot: get_support_history
    P_mcp_hubspot-->>V: datos (permisos del usuario)
    V->>P_workstation: compute_health
    P_workstation-->>V: datos (permisos del usuario)
  end
  V->>V: draft_retention_plan (modelo)
  V-->>GE: Ranking de cuentas con señales, plan y nivel de confianza.
  GE-->>U: Respuesta con fuentes y limitaciones
```

## 3. Workflow de la skill principal `customer-health`

```mermaid
flowchart TD
  S0["1. Leer uso con get_account_usage"]
  S0 -.-> X0_get_account_usage[["get_account_usage<br/>BigQuery"]]
  S1["2. Leer historial de soporte con get_support_history"]
  S0 --> S1
  S1 -.-> X1_get_support_history[["get_support_history<br/>HubSpot"]]
  S2["3. Calcular score con compute_health (fórmula versionada)"]
  S1 --> S2
  S2 -.-> X2_compute_health[["compute_health<br/>Workstation"]]
  S3["4. Explicar señales y nivel de confianza por cuenta"]
  S2 --> S3
  S4["5. Proponer plan de retención con draft_retention_plan"]
  S3 --> S4
  S4 -.-> X4_draft_retention_plan[["draft_retention_plan<br/>Modelo"]]
  S4 --> R(["Ranking - score - señales - confianza - plan de acción con responsable y fecha"])
```

## 4. Matriz de inputs, configuración, tools y outputs

| Inputs | Configuración | Tools | Outputs |
|---|---|---|---|
| Solicitud en lenguaje natural vía Gemini Enterprise<br>Identidad del usuario (OAuth A2A)<br>Tokens OAuth por conector<br>Doc: Playbooks CS<br>Doc: Definición health score<br>Doc: Contratos de servicio | Harness **Deep**<br>Modelo Gemini Pro - T=0.2<br>System prompt `AGENTS.md`<br>Skills: `customer-health`, `renewal-prep`, `churn-signal-review`<br>KB `kb-customer-health`<br>Guardrails: prompt_injection, off_topic, sql_risk, shell_risk<br>Memoria sin PII | `get_account_usage` (BigQuery)<br>`get_support_history` (HubSpot)<br>`compute_health` (Workstation, Ask)<br>`draft_retention_plan` (Modelo) | Ranking de cuentas con señales, plan y nivel de confianza.<br>Worklog y auditoría en VirtuAI<br>Sin efectos en sistemas (solo lectura) |

## 5. Capas de identidad

1. **Gemini Enterprise** — licencia + rol IAM sobre la app del área.
2. **A2A OAuth** — el usuario consiente `a2a:invoke` en VirtuAI (Authorization Code + PKCE).
3. **Conectores** — OAuth individual por MCP; IAM de servicio para Cloud Run con autorización de negocio en backend.
4. **Datos/acciones** — ACL de origen, RBAC, filas y aprobación humana.
