# Arquitectura - Strategic Opportunity Radar

**Área:** Dirección - **Harness:** Deep - **Acceso:** Lectura - **Complejidad:** 3/5 (media) - **Impacto:** 3/5 (medio)

## 1. Arquitectura (inputs → configuración → tools → outputs)

```mermaid
flowchart LR
  subgraph IN["Inputs"]
    direction TB
    U(["Usuario corporativo autenticado"])
    Q["Solicitud: ¿Qué oportunidades estratégicas emergieron este trimestre y cuáles priorizamos?"]
    DOCS[/"Documentos: Plan estratégico, Análisis de mercado, Roadmap de iniciativas"/]
  end
  subgraph GE["Gemini Enterprise"]
    direction TB
    APP["App ge-dirección - Custom agent via A2A"]
  end
  subgraph VA["VirtuAI - Strategic Opportunity Radar"]
    direction TB
    GOV{"Governance check: permisos, budget, guardrails"}
    LOOP(("Agentic loop Deep"))
    subgraph CFG["Configuración"]
      direction TB
      H["Harness: Deep - Gemini Pro - T=0.4 - max 8000 tok"]
      SP["System prompt: AGENTS.md"]
      SK["Skills: strategic-radar, market-signal-scan, initiative-prioritization"]
      KB[("KB kb-strategy-radar")]
      MEM["Memoria 16 KB - sin PII"]
      GR["Guardrails: prompt_injection, off_topic, sql_risk"]
      SEC["Security: Read-only"]
    end
  end
  subgraph TL["Tools"]
    direction TB
    T_kb["Knowledge Base de VirtuAI (RAG)<br/>search_knowledge"]
    T_mcp_bigquery["MCP predefinido - BigQuery<br/>get_strategy_metrics"]
    T_mcp_gmail["MCP predefinido - Gmail<br/>search_mail"]
  end
  subgraph SYS["Sistemas externos"]
    direction TB
    S_mcp_bigquery[("BigQuery")]
    S_mcp_gmail[("Gmail")]
  end
  subgraph OUT["Outputs"]
    direction TB
    O1["Matriz oportunidad-impacto-evidencia, dependencias y supuestos."]
    O3["Worklog - auditoría - métricas de uso"]
    O4["KPI: Calidad de oportunidades evaluadas, tiempo de análisis."]
  end
  U --> Q --> APP
  APP -->|"A2A JSON-RPC + OAuth a2a:invoke"| GOV --> LOOP
  CFG -.-> LOOP
  DOCS -.->|"indexación"| KB
  LOOP --> T_kb
  LOOP --> T_mcp_bigquery
  T_mcp_bigquery -->|OAuth por usuario| S_mcp_bigquery
  LOOP --> T_mcp_gmail
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
  class T_kb,T_mcp_bigquery,T_mcp_gmail tool
```

## 2. Secuencia de una ejecución (Gemini Enterprise → A2A → VirtuAI)

```mermaid
sequenceDiagram
  autonumber
  actor U as Usuario
  participant GE as Gemini Enterprise
  participant V as VirtuAI - agente
  participant P_kb as Knowledge Base
  participant P_mcp_bigquery as BigQuery
  participant P_mcp_gmail as Gmail
  U->>GE: ¿Qué oportunidades estratégicas emergieron este trimestre y cuáles priorizamos?
  GE->>V: A2A message/stream (Bearer, scope a2a:invoke)
  V->>V: Governance check y carga de skill strategic-radar
  loop Workflow: Leer prioridades → Consultar señales → Contrastar datos
    V->>P_kb: search_knowledge
    P_kb-->>V: datos (permisos del usuario)
    V->>P_mcp_bigquery: get_strategy_metrics
    P_mcp_bigquery-->>V: datos (permisos del usuario)
    V->>P_mcp_gmail: search_mail
    P_mcp_gmail-->>V: datos (permisos del usuario)
  end
  V->>V: draft_opportunity_map (modelo)
  V-->>GE: Matriz oportunidad-impacto-evidencia, dependencias y supuestos.
  GE-->>U: Respuesta con fuentes y limitaciones
```

## 3. Workflow de la skill principal `strategic-radar`

```mermaid
flowchart TD
  S0["1. Leer prioridades y objetivos vigentes con search_knowledge"]
  S0 -.-> X0_search_knowledge[["search_knowledge<br/>Knowledge Base"]]
  S1["2. Consultar métricas internas con get_strategy_metrics"]
  S0 --> S1
  S1 -.-> X1_get_strategy_metrics[["get_strategy_metrics<br/>BigQuery"]]
  S2["3. Buscar señales externas con web search y validar cada una con al menos una fuen…"]
  S1 --> S2
  S3["4. Contrastar señales vs. prioridades: encaje, impacto, esfuerzo y dependencias"]
  S2 --> S3
  S4["5. Priorizar con matriz impacto/esfuerzo y declarar supuestos"]
  S3 --> S4
  S5["6. Presentar hallazgos separando hechos, hipótesis y estimaciones"]
  S4 --> S5
  S5 --> R(["Matriz oportunidad - impacto - esfuerzo - evidencia - supuestos - dependencias"])
```

## 4. Matriz de inputs, configuración, tools y outputs

| Inputs | Configuración | Tools | Outputs |
|---|---|---|---|
| Solicitud en lenguaje natural vía Gemini Enterprise<br>Identidad del usuario (OAuth A2A)<br>Tokens OAuth por conector<br>Doc: Plan estratégico<br>Doc: Análisis de mercado<br>Doc: Roadmap de iniciativas | Harness **Deep**<br>Modelo Gemini Pro - T=0.4<br>System prompt `AGENTS.md`<br>Skills: `strategic-radar`, `market-signal-scan`, `initiative-prioritization`<br>KB `kb-strategy-radar`<br>Guardrails: prompt_injection, off_topic, sql_risk<br>Memoria sin PII | `search_knowledge` (Knowledge Base)<br>`get_strategy_metrics` (BigQuery)<br>`search_mail` (Gmail)<br>`draft_opportunity_map` (Modelo) | Matriz oportunidad-impacto-evidencia, dependencias y supuestos.<br>Worklog y auditoría en VirtuAI<br>Sin efectos en sistemas (solo lectura) |

## 5. Capas de identidad

1. **Gemini Enterprise** — licencia + rol IAM sobre la app del área.
2. **A2A OAuth** — el usuario consiente `a2a:invoke` en VirtuAI (Authorization Code + PKCE).
3. **Conectores** — OAuth individual por MCP; IAM de servicio para Cloud Run con autorización de negocio en backend.
4. **Datos/acciones** — ACL de origen, RBAC, filas y aprobación humana.
