# Arquitectura - Marketing Performance Analyst

**Área:** Marketing - **Harness:** Classic - **Acceso:** Lectura - **Complejidad:** 2/5 (baja) - **Impacto:** 3/5 (medio)

## 1. Arquitectura (inputs → configuración → tools → outputs)

```mermaid
flowchart LR
  subgraph IN["Inputs"]
    direction TB
    U(["Usuario corporativo autenticado"])
    Q["Solicitud: ¿Qué campañas generaron más oportunidades calificadas el último mes?"]
    DOCS[/"Documentos: Definición de métricas, UTM standards, Objetivos de campañas"/]
  end
  subgraph GE["Gemini Enterprise"]
    direction TB
    APP["App ge-marketing - Custom agent via A2A"]
  end
  subgraph VA["VirtuAI - Marketing Performance Analyst"]
    direction TB
    GOV{"Governance check: permisos, budget, guardrails"}
    LOOP(("Agentic loop Classic"))
    subgraph CFG["Configuración"]
      direction TB
      H["Harness: Classic - Gemini Flash - T=0.2 - max 5000 tok"]
      SP["System prompt: AGENTS.md"]
      SK["Procedimientos: campaign-attribution, metric-variance"]
      KB[("KB kb-marketing-analytics")]
      GR["Guardrails: prompt_injection, off_topic, sql_risk"]
      SEC["Security: Read-only"]
    end
  end
  subgraph TL["Tools"]
    direction TB
    T_mcp_hubspot["MCP predefinido - HubSpot<br/>get_campaigns"]
    T_mcp_bigquery["MCP predefinido - BigQuery<br/>run_readonly_query"]
  end
  subgraph SYS["Sistemas externos"]
    direction TB
    S_mcp_hubspot[("HubSpot CRM")]
    S_mcp_bigquery[("BigQuery")]
  end
  subgraph OUT["Outputs"]
    direction TB
    O1["Tabla comparativa con conversiones, costos si están disponibles y fuentes."]
    O3["Worklog - auditoría - métricas de uso"]
    O4["KPI: Tiempo de reporting, adopción de insights."]
  end
  U --> Q --> APP
  APP -->|"A2A JSON-RPC + OAuth a2a:invoke"| GOV --> LOOP
  CFG -.-> LOOP
  DOCS -.->|"indexación"| KB
  LOOP --> T_mcp_hubspot
  T_mcp_hubspot -->|OAuth por usuario| S_mcp_hubspot
  LOOP --> T_mcp_bigquery
  T_mcp_bigquery -->|OAuth por usuario| S_mcp_bigquery
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
  class T_mcp_hubspot,T_mcp_bigquery tool
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
  U->>GE: ¿Qué campañas generaron más oportunidades calificadas el último mes?
  GE->>V: A2A message/stream (Bearer, scope a2a:invoke)
  V->>V: Governance check y carga de skill campaign-attribution
  loop Workflow: Leer campañas → Unir métricas → Detectar variaciones
    V->>P_mcp_hubspot: get_campaigns
    P_mcp_hubspot-->>V: datos (permisos del usuario)
    V->>P_mcp_bigquery: run_readonly_query
    P_mcp_bigquery-->>V: datos (permisos del usuario)
  end
  V->>V: draft_insights (modelo)
  V-->>GE: Tabla comparativa con conversiones, costos si están disponibles y fuentes.
  GE-->>U: Respuesta con fuentes y limitaciones
```

## 3. Workflow de la skill principal `campaign-attribution`

```mermaid
flowchart TD
  S0["1. Leer campañas del periodo"]
  S1["2. Unir métricas por UTM con run_readonly_query"]
  S0 --> S1
  S1 -.-> X1_run_readonly_query[["run_readonly_query<br/>BigQuery"]]
  S2["3. Calcular conversiones y costo por resultado si existe"]
  S1 --> S2
  S3["4. Explicar con fuentes y límites del modelo de atribución"]
  S2 --> S3
  S3 --> R(["Tabla comparativa + modelo de atribución usado + limitaciones"])
```

## 4. Matriz de inputs, configuración, tools y outputs

| Inputs | Configuración | Tools | Outputs |
|---|---|---|---|
| Solicitud en lenguaje natural vía Gemini Enterprise<br>Identidad del usuario (OAuth A2A)<br>Tokens OAuth por conector<br>Doc: Definición de métricas<br>Doc: UTM standards<br>Doc: Objetivos de campañas | Harness **Classic**<br>Modelo Gemini Flash - T=0.2<br>System prompt `AGENTS.md`<br>Procedimientos: `campaign-attribution`, `metric-variance`<br>KB `kb-marketing-analytics`<br>Guardrails: prompt_injection, off_topic, sql_risk | `get_campaigns` (HubSpot)<br>`run_readonly_query` (BigQuery)<br>`draft_insights` (Modelo) | Tabla comparativa con conversiones, costos si están disponibles y fuentes.<br>Worklog y auditoría en VirtuAI<br>Sin efectos en sistemas (solo lectura) |

## 5. Capas de identidad

1. **Gemini Enterprise** — licencia + rol IAM sobre la app del área.
2. **A2A OAuth** — el usuario consiente `a2a:invoke` en VirtuAI (Authorization Code + PKCE).
3. **Conectores** — OAuth individual por MCP; IAM de servicio para Cloud Run con autorización de negocio en backend.
4. **Datos/acciones** — ACL de origen, RBAC, filas y aprobación humana.
