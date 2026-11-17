# Arquitectura - Enterprise Data Analyst

**Área:** Datos - **Harness:** Deep - **Acceso:** Lectura - **Complejidad:** 3/5 (media) - **Impacto:** 5/5 (muy alto)

## 1. Arquitectura (inputs → configuración → tools → outputs)

```mermaid
flowchart LR
  subgraph IN["Inputs"]
    direction TB
    U(["Usuario corporativo autenticado"])
    Q["Solicitud: ¿Cómo varió el revenue por región en los últimos seis meses?"]
    DOCS[/"Documentos: Diccionario de datos, Catálogo de métricas, Políticas de acceso"/]
  end
  subgraph GE["Gemini Enterprise"]
    direction TB
    APP["App ge-datos - Custom agent via A2A"]
  end
  subgraph VA["VirtuAI - Enterprise Data Analyst"]
    direction TB
    GOV{"Governance check: permisos, budget, guardrails"}
    LOOP(("Agentic loop Deep"))
    subgraph CFG["Configuración"]
      direction TB
      H["Harness: Deep - Gemini Pro - T=0.1 - max 6000 tok"]
      SP["System prompt: AGENTS.md"]
      SK["Skills: governed-sql, metric-definition-check, query-cost-guard"]
      KB[("KB kb-sql-analyst")]
      MEM["Memoria 16 KB - sin PII"]
      GR["Guardrails: prompt_injection, off_topic, sql_risk"]
      SEC["Security: Read-only"]
    end
  end
  subgraph TL["Tools"]
    direction TB
    T_mcp_bigquery["MCP predefinido - BigQuery<br/>discover_schema<br/>validate_sql<br/>run_readonly_query"]
    T_kb["Knowledge Base de VirtuAI (RAG)<br/>explain_metrics"]
  end
  subgraph SYS["Sistemas externos"]
    direction TB
    S_mcp_bigquery[("BigQuery")]
  end
  subgraph OUT["Outputs"]
    direction TB
    O1["Tabla y narrativa con SQL documentado, fuente y supuestos."]
    O3["Worklog - auditoría - métricas de uso"]
    O4["KPI: Tiempo hasta insight, exactitud de consultas."]
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
  class MEM cfg
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
  U->>GE: ¿Cómo varió el revenue por región en los últimos seis meses?
  GE->>V: A2A message/stream (Bearer, scope a2a:invoke)
  V->>V: Governance check y carga de skill governed-sql
  loop Workflow: Entender pregunta → Consultar esquema → Validar SQL
    V->>P_mcp_bigquery: discover_schema
    P_mcp_bigquery-->>V: datos (permisos del usuario)
    V->>P_mcp_bigquery: validate_sql
    P_mcp_bigquery-->>V: datos (permisos del usuario)
    V->>P_mcp_bigquery: run_readonly_query
    P_mcp_bigquery-->>V: datos (permisos del usuario)
    V->>P_kb: explain_metrics
    P_kb-->>V: datos (permisos del usuario)
  end
  V-->>GE: Tabla y narrativa con SQL documentado, fuente y supuestos.
  GE-->>U: Respuesta con fuentes y limitaciones
```

## 3. Workflow de la skill principal `governed-sql`

```mermaid
flowchart TD
  S0["1. Traducir la pregunta a métricas oficiales con explain_metrics"]
  S0 -.-> X0_explain_metrics[["explain_metrics<br/>Knowledge Base"]]
  S1["2. Descubrir tablas con discover_schema"]
  S0 --> S1
  S1 -.-> X1_discover_schema[["discover_schema<br/>BigQuery"]]
  S2["3. Escribir SQL solo SELECT con LIMIT"]
  S1 --> S2
  S3["4. Validar con validate_sql (bytes, tipo de sentencia)"]
  S2 --> S3
  S3 -.-> X3_validate_sql[["validate_sql<br/>BigQuery"]]
  S4["5. Ejecutar con run_readonly_query"]
  S3 --> S4
  S4 -.-> X4_run_readonly_query[["run_readonly_query<br/>BigQuery"]]
  S5["6. Explicar resultados con SQL, fuente, filtros y supuestos"]
  S4 --> S5
  S5 --> R(["Respuesta - tabla - SQL usado - fuente - supuestos - costo estimado"])
```

## 4. Matriz de inputs, configuración, tools y outputs

| Inputs | Configuración | Tools | Outputs |
|---|---|---|---|
| Solicitud en lenguaje natural vía Gemini Enterprise<br>Identidad del usuario (OAuth A2A)<br>Tokens OAuth por conector<br>Doc: Diccionario de datos<br>Doc: Catálogo de métricas<br>Doc: Políticas de acceso | Harness **Deep**<br>Modelo Gemini Pro - T=0.1<br>System prompt `AGENTS.md`<br>Skills: `governed-sql`, `metric-definition-check`, `query-cost-guard`<br>KB `kb-sql-analyst`<br>Guardrails: prompt_injection, off_topic, sql_risk<br>Memoria sin PII | `discover_schema` (BigQuery)<br>`validate_sql` (BigQuery)<br>`run_readonly_query` (BigQuery)<br>`explain_metrics` (Knowledge Base) | Tabla y narrativa con SQL documentado, fuente y supuestos.<br>Worklog y auditoría en VirtuAI<br>Sin efectos en sistemas (solo lectura) |

## 5. Capas de identidad

1. **Gemini Enterprise** — licencia + rol IAM sobre la app del área.
2. **A2A OAuth** — el usuario consiente `a2a:invoke` en VirtuAI (Authorization Code + PKCE).
3. **Conectores** — OAuth individual por MCP; IAM de servicio para Cloud Run con autorización de negocio en backend.
4. **Datos/acciones** — ACL de origen, RBAC, filas y aprobación humana.
