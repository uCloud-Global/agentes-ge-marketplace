# Arquitectura - Data Quality Sentinel

**Área:** Datos - **Harness:** Deep - **Acceso:** Lectura - **Complejidad:** 3/5 (media) - **Impacto:** 3/5 (medio)

## 1. Arquitectura (inputs → configuración → tools → outputs)

```mermaid
flowchart LR
  subgraph IN["Inputs"]
    direction TB
    U(["Usuario corporativo autenticado"])
    Q["Solicitud: ¿Qué datasets críticos incumplieron sus SLA de calidad esta semana?"]
    DOCS[/"Documentos: Contratos de datos, Reglas de calidad, SLA de actualización"/]
  end
  subgraph GE["Gemini Enterprise"]
    direction TB
    APP["App ge-datos - Custom agent via A2A"]
  end
  subgraph VA["VirtuAI - Data Quality Sentinel"]
    direction TB
    GOV{"Governance check: permisos, budget, guardrails"}
    LOOP(("Agentic loop Deep"))
    subgraph CFG["Configuración"]
      direction TB
      H["Harness: Deep - Gemini Pro - T=0.1 - max 5000 tok"]
      SP["System prompt: AGENTS.md"]
      SK["Skills: quality-report, anomaly-explain, data-contract-check"]
      KB[("KB kb-data-quality")]
      MEM["Memoria 16 KB - sin PII"]
      GR["Guardrails: prompt_injection, off_topic, sql_risk"]
      SEC["Security: Read-only"]
    end
  end
  subgraph TL["Tools"]
    direction TB
    T_mcp_bigquery["MCP predefinido - BigQuery<br/>get_freshness<br/>run_quality_checks"]
    T_mcp_cloud_logging["MCP predefinido - Cloud Logging<br/>query_pipeline_logs"]
  end
  subgraph SYS["Sistemas externos"]
    direction TB
    S_mcp_bigquery[("BigQuery")]
    S_mcp_cloud_logging[("Cloud Logging")]
  end
  subgraph OUT["Outputs"]
    direction TB
    O1["Scorecard de calidad, tablas afectadas y tickets propuestos."]
    O3["Worklog - auditoría - métricas de uso"]
    O4["KPI: Incidentes detectados antes de consumo, SLA."]
  end
  U --> Q --> APP
  APP -->|"A2A JSON-RPC + OAuth a2a:invoke"| GOV --> LOOP
  CFG -.-> LOOP
  DOCS -.->|"indexación"| KB
  LOOP --> T_mcp_bigquery
  T_mcp_bigquery -->|OAuth por usuario| S_mcp_bigquery
  LOOP --> T_mcp_cloud_logging
  T_mcp_cloud_logging -->|OAuth por usuario| S_mcp_cloud_logging
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
  class T_mcp_bigquery,T_mcp_cloud_logging tool
```

## 2. Secuencia de una ejecución (Gemini Enterprise → A2A → VirtuAI)

```mermaid
sequenceDiagram
  autonumber
  actor U as Usuario
  participant GE as Gemini Enterprise
  participant V as VirtuAI - agente
  participant P_mcp_bigquery as BigQuery
  participant P_mcp_cloud_logging as Cloud Logging
  U->>GE: ¿Qué datasets críticos incumplieron sus SLA de calidad esta semana?
  GE->>V: A2A message/stream (Bearer, scope a2a:invoke)
  V->>V: Governance check y carga de skill quality-report
  loop Workflow: Seleccionar datasets → Verificar frescura → Probar reglas
    V->>P_mcp_bigquery: get_freshness
    P_mcp_bigquery-->>V: datos (permisos del usuario)
    V->>P_mcp_bigquery: run_quality_checks
    P_mcp_bigquery-->>V: datos (permisos del usuario)
    V->>P_mcp_cloud_logging: query_pipeline_logs
    P_mcp_cloud_logging-->>V: datos (permisos del usuario)
  end
  V->>V: draft_issue (modelo)
  V-->>GE: Scorecard de calidad, tablas afectadas y tickets propuestos.
  GE-->>U: Respuesta con fuentes y limitaciones
```

## 3. Workflow de la skill principal `quality-report`

```mermaid
flowchart TD
  S0["1. Seleccionar datasets críticos según contratos de datos"]
  S1["2. Verificar frescura con get_freshness"]
  S0 --> S1
  S1 -.-> X1_get_freshness[["get_freshness<br/>BigQuery"]]
  S2["3. Ejecutar reglas con run_quality_checks"]
  S1 --> S2
  S2 -.-> X2_run_quality_checks[["run_quality_checks<br/>BigQuery"]]
  S3["4. Correlacionar con logs de pipeline"]
  S2 --> S3
  S4["5. Priorizar anomalías por impacto"]
  S3 --> S4
  S5["6. Preparar incidente con draft_issue"]
  S4 --> S5
  S5 -.-> X5_draft_issue[["draft_issue<br/>Modelo"]]
  S5 --> R(["Scorecard tabla - regla - resultado - SLA - impacto - incidente propuesto"])
```

## 4. Matriz de inputs, configuración, tools y outputs

| Inputs | Configuración | Tools | Outputs |
|---|---|---|---|
| Solicitud en lenguaje natural vía Gemini Enterprise<br>Identidad del usuario (OAuth A2A)<br>Tokens OAuth por conector<br>Doc: Contratos de datos<br>Doc: Reglas de calidad<br>Doc: SLA de actualización | Harness **Deep**<br>Modelo Gemini Pro - T=0.1<br>System prompt `AGENTS.md`<br>Skills: `quality-report`, `anomaly-explain`, `data-contract-check`<br>KB `kb-data-quality`<br>Guardrails: prompt_injection, off_topic, sql_risk<br>Memoria sin PII | `get_freshness` (BigQuery)<br>`run_quality_checks` (BigQuery)<br>`query_pipeline_logs` (Cloud Logging)<br>`draft_issue` (Modelo) | Scorecard de calidad, tablas afectadas y tickets propuestos.<br>Worklog y auditoría en VirtuAI<br>Sin efectos en sistemas (solo lectura) |

## 5. Capas de identidad

1. **Gemini Enterprise** — licencia + rol IAM sobre la app del área.
2. **A2A OAuth** — el usuario consiente `a2a:invoke` en VirtuAI (Authorization Code + PKCE).
3. **Conectores** — OAuth individual por MCP; IAM de servicio para Cloud Run con autorización de negocio en backend.
4. **Datos/acciones** — ACL de origen, RBAC, filas y aprobación humana.
