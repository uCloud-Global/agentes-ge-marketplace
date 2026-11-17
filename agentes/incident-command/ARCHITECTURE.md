# Arquitectura - Incident Response Coordinator

**Área:** Tecnología - **Harness:** Deep - **Acceso:** Lectura - **Complejidad:** 4/5 (alta) - **Impacto:** 4/5 (alto)

## 1. Arquitectura (inputs → configuración → tools → outputs)

```mermaid
flowchart LR
  subgraph IN["Inputs"]
    direction TB
    U(["Usuario corporativo autenticado"])
    Q["Solicitud: Analiza los errores 5xx del servicio de pagos durante la última hora."]
    DOCS[/"Documentos: Runbooks, Postmortems, Matriz severidad, Guardias"/]
  end
  subgraph GE["Gemini Enterprise"]
    direction TB
    APP["App ge-tecnología - Custom agent via A2A"]
  end
  subgraph VA["VirtuAI - Incident Response Coordinator"]
    direction TB
    GOV{"Governance check: permisos, budget, guardrails"}
    LOOP(("Agentic loop Deep"))
    subgraph CFG["Configuración"]
      direction TB
      H["Harness: Deep - Gemini Pro - T=0.1 - max 8000 tok"]
      SP["System prompt: AGENTS.md"]
      SK["Skills: incident-triage, postmortem-draft, log-pii-safe-summary"]
      KB[("KB kb-incident-command")]
      MEM["Memoria 16 KB - sin PII"]
      GR["Guardrails: prompt_injection, off_topic, sql_risk"]
      SEC["Security: Read-only"]
    end
  end
  subgraph TL["Tools"]
    direction TB
    T_mcp_cloud_logging["MCP predefinido - Cloud Logging<br/>query_logs"]
    T_mcp_cloud_monitoring["MCP predefinido - Cloud Monitoring<br/>get_alerts"]
    T_kb["Knowledge Base de VirtuAI (RAG)<br/>search_runbook"]
    T_mcp_bigquery["MCP predefinido - BigQuery<br/>query_deploys"]
    T_mcp_gmail["MCP predefinido - Gmail<br/>draft_incident_report (Ask)"]
  end
  subgraph SYS["Sistemas externos"]
    direction TB
    S_mcp_cloud_logging[("Cloud Logging")]
    S_mcp_cloud_monitoring[("Cloud Monitoring")]
    S_mcp_bigquery[("BigQuery")]
    S_mcp_gmail[("Gmail")]
  end
  subgraph OUT["Outputs"]
    direction TB
    O1["Hipótesis priorizadas, señales de soporte y plan de respuesta."]
    O3["Worklog - auditoría - métricas de uso"]
    O4["KPI: MTTR, tiempo de diagnóstico."]
  end
  U --> Q --> APP
  APP -->|"A2A JSON-RPC + OAuth a2a:invoke"| GOV --> LOOP
  CFG -.-> LOOP
  DOCS -.->|"indexación"| KB
  LOOP --> T_mcp_cloud_logging
  T_mcp_cloud_logging -->|OAuth por usuario| S_mcp_cloud_logging
  LOOP --> T_mcp_cloud_monitoring
  T_mcp_cloud_monitoring -->|OAuth por usuario| S_mcp_cloud_monitoring
  LOOP --> T_kb
  LOOP --> T_mcp_bigquery
  T_mcp_bigquery -->|OAuth por usuario| S_mcp_bigquery
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
  class T_mcp_cloud_logging,T_mcp_cloud_monitoring,T_kb,T_mcp_bigquery,T_mcp_gmail tool
```

## 2. Secuencia de una ejecución (Gemini Enterprise → A2A → VirtuAI)

```mermaid
sequenceDiagram
  autonumber
  actor U as Usuario
  participant GE as Gemini Enterprise
  participant V as VirtuAI - agente
  participant P_mcp_cloud_logging as Cloud Logging
  participant P_mcp_cloud_monitoring as Cloud Monitoring
  participant P_kb as Knowledge Base
  participant P_mcp_bigquery as BigQuery
  participant P_mcp_gmail as Gmail
  U->>GE: Analiza los errores 5xx del servicio de pagos durante la última hora.
  GE->>V: A2A message/stream (Bearer, scope a2a:invoke)
  V->>V: Governance check y carga de skill incident-triage
  loop Workflow: Recibir señal → Correlacionar logs → Consultar runbook
    V->>P_mcp_cloud_logging: query_logs
    P_mcp_cloud_logging-->>V: datos (permisos del usuario)
    V->>P_mcp_cloud_monitoring: get_alerts
    P_mcp_cloud_monitoring-->>V: datos (permisos del usuario)
    V->>P_kb: search_runbook
    P_kb-->>V: datos (permisos del usuario)
    V->>P_mcp_bigquery: query_deploys
    P_mcp_bigquery-->>V: datos (permisos del usuario)
  end
  V-->>GE: task input-required (vista previa + approval_requests)
  GE-->>U: Solicitud de aprobación
  alt Aprobado
    U->>GE: Aprobar
    GE->>V: respuesta de aprobación
    V->>P_mcp_gmail: draft_incident_report (request_id)
    P_mcp_gmail-->>V: OK + ID
  else Denegado o expira
    V->>V: acción queda pendiente, sin reintento
  end
  V-->>GE: Hipótesis priorizadas, señales de soporte y plan de respuesta.
  GE-->>U: Respuesta con fuentes y limitaciones
```

## 3. Workflow de la skill principal `incident-triage`

```mermaid
flowchart TD
  S0["1. Definir servicio, ventana y síntoma"]
  S1["2. Leer alertas y métricas con get_alerts"]
  S0 --> S1
  S1 -.-> X1_get_alerts[["get_alerts<br/>Cloud Monitoring"]]
  S2["3. Correlacionar logs con query_logs (top errores, primer timestamp)"]
  S1 --> S2
  S2 -.-> X2_query_logs[["query_logs<br/>Cloud Logging"]]
  S3["4. Correlacionar con despliegues recientes"]
  S2 --> S3
  S4["5. Consultar runbook y severidad"]
  S3 --> S4
  S5["6. Formar hipótesis priorizadas con evidencia"]
  S4 --> S5
  S6["7. Redactar informe y escalar al responsable de guardia"]
  S5 --> S6
  S6 --> R(["Severidad - línea de tiempo - hipótesis priorizadas con evidencia - acciones sugeridas (n…"])
```

## 4. Matriz de inputs, configuración, tools y outputs

| Inputs | Configuración | Tools | Outputs |
|---|---|---|---|
| Solicitud en lenguaje natural vía Gemini Enterprise<br>Identidad del usuario (OAuth A2A)<br>Tokens OAuth por conector<br>Doc: Runbooks<br>Doc: Postmortems<br>Doc: Matriz severidad<br>Doc: Guardias | Harness **Deep**<br>Modelo Gemini Pro - T=0.1<br>System prompt `AGENTS.md`<br>Skills: `incident-triage`, `postmortem-draft`, `log-pii-safe-summary`<br>KB `kb-incident-command`<br>Guardrails: prompt_injection, off_topic, sql_risk<br>Memoria sin PII | `query_logs` (Cloud Logging)<br>`get_alerts` (Cloud Monitoring)<br>`search_runbook` (Knowledge Base)<br>`query_deploys` (BigQuery)<br>`draft_incident_report` (Gmail, Ask) | Hipótesis priorizadas, señales de soporte y plan de respuesta.<br>Worklog y auditoría en VirtuAI<br>Sin efectos en sistemas (solo lectura) |

## 5. Capas de identidad

1. **Gemini Enterprise** — licencia + rol IAM sobre la app del área.
2. **A2A OAuth** — el usuario consiente `a2a:invoke` en VirtuAI (Authorization Code + PKCE).
3. **Conectores** — OAuth individual por MCP; IAM de servicio para Cloud Run con autorización de negocio en backend.
4. **Datos/acciones** — ACL de origen, RBAC, filas y aprobación humana.
