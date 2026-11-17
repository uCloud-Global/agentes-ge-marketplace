# Arquitectura - Cashflow Forecast Analyst

**Área:** Finanzas - **Harness:** Deep - **Acceso:** Lectura - **Complejidad:** 4/5 (alta) - **Impacto:** 4/5 (alto)

## 1. Arquitectura (inputs → configuración → tools → outputs)

```mermaid
flowchart LR
  subgraph IN["Inputs"]
    direction TB
    U(["Usuario corporativo autenticado"])
    Q["Solicitud: Proyecta el flujo de caja de las próximas 12 semanas con escenarios."]
    DOCS[/"Documentos: Políticas financieras, Plan presupuestal, Supuestos de forecasting"/]
  end
  subgraph GE["Gemini Enterprise"]
    direction TB
    APP["App ge-finanzas - Custom agent via A2A"]
  end
  subgraph VA["VirtuAI - Cashflow Forecast Analyst"]
    direction TB
    GOV{"Governance check: permisos, budget, guardrails"}
    LOOP(("Agentic loop Deep"))
    subgraph CFG["Configuración"]
      direction TB
      H["Harness: Deep - Gemini Pro - T=0.1 - max 8000 tok"]
      SP["System prompt: AGENTS.md"]
      SK["Skills: forecast-model, liquidity-alert, forecast-backtest"]
      KB[("KB kb-cashflow-analyst")]
      MEM["Memoria 16 KB - sin PII"]
      GR["Guardrails: prompt_injection, off_topic, sql_risk, shell_risk"]
      SEC["Security: Read-only"]
    end
  end
  subgraph TL["Tools"]
    direction TB
    T_mcp_bigquery["MCP predefinido - BigQuery<br/>read_cashflow<br/>get_ar_ap"]
    T_workstation["Deep Agent - Workstation / sandbox (Python)<br/>calculate_scenarios"]
  end
  subgraph SYS["Sistemas externos"]
    direction TB
    S_mcp_bigquery[("BigQuery")]
    S_workstation[("Entorno aislado")]
  end
  subgraph OUT["Outputs"]
    direction TB
    O1["Pronóstico por semana, rango de incertidumbre y principales riesgos."]
    O3["Worklog - auditoría - métricas de uso"]
    O4["KPI: Tiempo de forecast, error de proyección."]
  end
  U --> Q --> APP
  APP -->|"A2A JSON-RPC + OAuth a2a:invoke"| GOV --> LOOP
  CFG -.-> LOOP
  DOCS -.->|"indexación"| KB
  LOOP --> T_mcp_bigquery
  T_mcp_bigquery -->|OAuth por usuario| S_mcp_bigquery
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
  class T_mcp_bigquery,T_workstation tool
```

## 2. Secuencia de una ejecución (Gemini Enterprise → A2A → VirtuAI)

```mermaid
sequenceDiagram
  autonumber
  actor U as Usuario
  participant GE as Gemini Enterprise
  participant V as VirtuAI - agente
  participant P_mcp_bigquery as BigQuery
  participant P_workstation as Workstation
  U->>GE: Proyecta el flujo de caja de las próximas 12 semanas con escenarios.
  GE->>V: A2A message/stream (Bearer, scope a2a:invoke)
  V->>V: Governance check y carga de skill forecast-model
  loop Workflow: Leer históricos → Unificar cuentas → Proyectar escenarios
    V->>P_mcp_bigquery: read_cashflow
    P_mcp_bigquery-->>V: datos (permisos del usuario)
    V->>P_mcp_bigquery: get_ar_ap
    P_mcp_bigquery-->>V: datos (permisos del usuario)
    V->>P_workstation: calculate_scenarios
    P_workstation-->>V: datos (permisos del usuario)
  end
  V->>V: draft_forecast (modelo)
  V-->>GE: Pronóstico por semana, rango de incertidumbre y principales riesgos.
  GE-->>U: Respuesta con fuentes y limitaciones
```

## 3. Workflow de la skill principal `forecast-model`

```mermaid
flowchart TD
  S0["1. Leer históricos con read_cashflow y conciliar saldos iniciales"]
  S0 -.-> X0_read_cashflow[["read_cashflow<br/>BigQuery"]]
  S1["2. Leer AR/AP con get_ar_ap y aplicar patrones de cobro/pago"]
  S0 --> S1
  S1 -.-> X1_get_ar_ap[["get_ar_ap<br/>BigQuery"]]
  S2["3. Calcular escenarios con calculate_scenarios"]
  S1 --> S2
  S2 -.-> X2_calculate_scenarios[["calculate_scenarios<br/>Workstation"]]
  S3["4. Explicar supuestos y rango de incertidumbre"]
  S2 --> S3
  S4["5. Redactar pronóstico con draft_forecast"]
  S3 --> S4
  S4 -.-> X4_draft_forecast[["draft_forecast<br/>Modelo"]]
  S4 --> R(["Tabla semanal (12 semanas) por escenario - supuestos - riesgos - semanas críticas"])
```

## 4. Matriz de inputs, configuración, tools y outputs

| Inputs | Configuración | Tools | Outputs |
|---|---|---|---|
| Solicitud en lenguaje natural vía Gemini Enterprise<br>Identidad del usuario (OAuth A2A)<br>Tokens OAuth por conector<br>Doc: Políticas financieras<br>Doc: Plan presupuestal<br>Doc: Supuestos de forecasting | Harness **Deep**<br>Modelo Gemini Pro - T=0.1<br>System prompt `AGENTS.md`<br>Skills: `forecast-model`, `liquidity-alert`, `forecast-backtest`<br>KB `kb-cashflow-analyst`<br>Guardrails: prompt_injection, off_topic, sql_risk, shell_risk<br>Memoria sin PII | `read_cashflow` (BigQuery)<br>`get_ar_ap` (BigQuery)<br>`calculate_scenarios` (Workstation, Ask)<br>`draft_forecast` (Modelo) | Pronóstico por semana, rango de incertidumbre y principales riesgos.<br>Worklog y auditoría en VirtuAI<br>Sin efectos en sistemas (solo lectura) |

## 5. Capas de identidad

1. **Gemini Enterprise** — licencia + rol IAM sobre la app del área.
2. **A2A OAuth** — el usuario consiente `a2a:invoke` en VirtuAI (Authorization Code + PKCE).
3. **Conectores** — OAuth individual por MCP; IAM de servicio para Cloud Run con autorización de negocio en backend.
4. **Datos/acciones** — ACL de origen, RBAC, filas y aprobación humana.
