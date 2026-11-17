# Arquitectura - Expense Policy Auditor

**Área:** Finanzas - **Harness:** Classic - **Acceso:** Lectura - **Complejidad:** 2/5 (baja) - **Impacto:** 3/5 (medio)

## 1. Arquitectura (inputs → configuración → tools → outputs)

```mermaid
flowchart LR
  subgraph IN["Inputs"]
    direction TB
    U(["Usuario corporativo autenticado"])
    Q["Solicitud: Audita los gastos del último viaje y marca los que exceden política."]
    DOCS[/"Documentos: Política de viáticos, Tabla de topes, Procedimiento de reembolso"/]
  end
  subgraph GE["Gemini Enterprise"]
    direction TB
    APP["App ge-finanzas - Custom agent via A2A"]
  end
  subgraph VA["VirtuAI - Expense Policy Auditor"]
    direction TB
    GOV{"Governance check: permisos, budget, guardrails"}
    LOOP(("Agentic loop Classic"))
    subgraph CFG["Configuración"]
      direction TB
      H["Harness: Classic - Gemini Flash - T=0.1 - max 4000 tok"]
      SP["System prompt: AGENTS.md"]
      SK["Procedimientos: expense-audit, fx-normalization"]
      KB[("KB kb-expense-auditor")]
      GR["Guardrails: prompt_injection, off_topic, sql_risk"]
      SEC["Security: Read-only"]
    end
  end
  subgraph TL["Tools"]
    direction TB
    T_mcp_bigquery["MCP predefinido - BigQuery<br/>get_expenses"]
    T_kb["Knowledge Base de VirtuAI (RAG)<br/>read_policy"]
  end
  subgraph SYS["Sistemas externos"]
    direction TB
    S_mcp_bigquery[("BigQuery")]
  end
  subgraph OUT["Outputs"]
    direction TB
    O1["Tabla de excepciones y evidencia, sin rechazos automáticos."]
    O3["Worklog - auditoría - métricas de uso"]
    O4["KPI: Tiempo de auditoría, precisión de alertas."]
  end
  U --> Q --> APP
  APP -->|"A2A JSON-RPC + OAuth a2a:invoke"| GOV --> LOOP
  CFG -.-> LOOP
  DOCS -.->|"indexación"| KB
  LOOP --> T_mcp_bigquery
  T_mcp_bigquery -->|OAuth por usuario| S_mcp_bigquery
  LOOP --> T_kb
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
  class T_mcp_bigquery,T_kb tool
```

## 2. Secuencia de una ejecución (Gemini Enterprise → A2A → VirtuAI)

```mermaid
sequenceDiagram
  autonumber
  actor U as Usuario
  participant GE as Gemini Enterprise
  participant V as VirtuAI - agente
  participant P_mcp_bigquery as BigQuery
  participant P_kb as Knowledge Base
  U->>GE: Audita los gastos del último viaje y marca los que exceden política.
  GE->>V: A2A message/stream (Bearer, scope a2a:invoke)
  V->>V: Governance check y carga de skill expense-audit
  loop Workflow: Leer gastos → Identificar política → Comparar topes
    V->>P_mcp_bigquery: get_expenses
    P_mcp_bigquery-->>V: datos (permisos del usuario)
    V->>P_kb: read_policy
    P_kb-->>V: datos (permisos del usuario)
  end
  V->>V: flag_exceptions (modelo)
  V-->>GE: Tabla de excepciones y evidencia, sin rechazos automáticos.
  GE-->>U: Respuesta con fuentes y limitaciones
```

## 3. Workflow de la skill principal `expense-audit`

```mermaid
flowchart TD
  S0["1. Leer gastos con get_expenses"]
  S0 -.-> X0_get_expenses[["get_expenses<br/>BigQuery"]]
  S1["2. Identificar política aplicable (país, fecha, moneda) con read_policy"]
  S0 --> S1
  S1 -.-> X1_read_policy[["read_policy<br/>Knowledge Base"]]
  S2["3. Comparar contra topes y excepciones aprobadas"]
  S1 --> S2
  S3["4. Listar excepciones con evidencia"]
  S2 --> S3
  S3 --> R(["Tabla gasto - tope - diferencia - evidencia - excepción aprobada sí/no"])
```

## 4. Matriz de inputs, configuración, tools y outputs

| Inputs | Configuración | Tools | Outputs |
|---|---|---|---|
| Solicitud en lenguaje natural vía Gemini Enterprise<br>Identidad del usuario (OAuth A2A)<br>Tokens OAuth por conector<br>Doc: Política de viáticos<br>Doc: Tabla de topes<br>Doc: Procedimiento de reembolso | Harness **Classic**<br>Modelo Gemini Flash - T=0.1<br>System prompt `AGENTS.md`<br>Procedimientos: `expense-audit`, `fx-normalization`<br>KB `kb-expense-auditor`<br>Guardrails: prompt_injection, off_topic, sql_risk | `get_expenses` (BigQuery)<br>`read_policy` (Knowledge Base)<br>`flag_exceptions` (Modelo) | Tabla de excepciones y evidencia, sin rechazos automáticos.<br>Worklog y auditoría en VirtuAI<br>Sin efectos en sistemas (solo lectura) |

## 5. Capas de identidad

1. **Gemini Enterprise** — licencia + rol IAM sobre la app del área.
2. **A2A OAuth** — el usuario consiente `a2a:invoke` en VirtuAI (Authorization Code + PKCE).
3. **Conectores** — OAuth individual por MCP; IAM de servicio para Cloud Run con autorización de negocio en backend.
4. **Datos/acciones** — ACL de origen, RBAC, filas y aprobación humana.
