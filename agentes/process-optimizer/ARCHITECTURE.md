# Arquitectura - Process Improvement Scout

**Área:** Operaciones - **Harness:** Deep - **Acceso:** Lectura - **Complejidad:** 3/5 (media) - **Impacto:** 3/5 (medio)

## 1. Arquitectura (inputs → configuración → tools → outputs)

```mermaid
flowchart LR
  subgraph IN["Inputs"]
    direction TB
    U(["Usuario corporativo autenticado"])
    Q["Solicitud: Analiza el proceso de aprobación de compras y dónde se pierde tiempo."]
    DOCS[/"Documentos: SOP actuales, Métricas operativas, Flujogramas"/]
  end
  subgraph GE["Gemini Enterprise"]
    direction TB
    APP["App ge-operaciones - Custom agent via A2A"]
  end
  subgraph VA["VirtuAI - Process Improvement Scout"]
    direction TB
    GOV{"Governance check: permisos, budget, guardrails"}
    LOOP(("Agentic loop Deep"))
    subgraph CFG["Configuración"]
      direction TB
      H["Harness: Deep - Gemini Pro - T=0.3 - max 8000 tok"]
      SP["System prompt: AGENTS.md"]
      SK["Skills: process-improvement, process-mining-lite, automation-business-case"]
      KB[("KB kb-process-optimizer")]
      MEM["Memoria 16 KB - sin PII"]
      GR["Guardrails: prompt_injection, off_topic, sql_risk, shell_risk"]
      SEC["Security: Read-only"]
    end
  end
  subgraph TL["Tools"]
    direction TB
    T_kb["Knowledge Base de VirtuAI (RAG)<br/>search_sop"]
    T_mcp_bigquery["MCP predefinido - BigQuery<br/>query_cycle_time"]
  end
  subgraph SYS["Sistemas externos"]
    direction TB
    S_mcp_bigquery[("BigQuery")]
  end
  subgraph OUT["Outputs"]
    direction TB
    O1["Mapa AS-IS / TO-BE, cuellos de botella y backlog de automatización."]
    O3["Worklog - auditoría - métricas de uso"]
    O4["KPI: Tiempo de ciclo, cantidad de retrabajos."]
  end
  U --> Q --> APP
  APP -->|"A2A JSON-RPC + OAuth a2a:invoke"| GOV --> LOOP
  CFG -.-> LOOP
  DOCS -.->|"indexación"| KB
  LOOP --> T_kb
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
  class MEM cfg
  class T_kb,T_mcp_bigquery tool
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
  U->>GE: Analiza el proceso de aprobación de compras y dónde se pierde tiempo.
  GE->>V: A2A message/stream (Bearer, scope a2a:invoke)
  V->>V: Governance check y carga de skill process-improvement
  loop Workflow: Seleccionar proceso → Leer SOP → Medir fricciones
    V->>P_kb: search_sop
    P_kb-->>V: datos (permisos del usuario)
    V->>P_mcp_bigquery: query_cycle_time
    P_mcp_bigquery-->>V: datos (permisos del usuario)
  end
  V->>V: draft_automation_map (modelo)
  V-->>GE: Mapa AS-IS / TO-BE, cuellos de botella y backlog de automatización.
  GE-->>U: Respuesta con fuentes y limitaciones
```

## 3. Workflow de la skill principal `process-improvement`

```mermaid
flowchart TD
  S0["1. Seleccionar proceso y alcance"]
  S1["2. Leer SOP con search_sop"]
  S0 --> S1
  S1 -.-> X1_search_sop[["search_sop<br/>Knowledge Base"]]
  S2["3. Medir tiempos por etapa con query_cycle_time"]
  S1 --> S2
  S2 -.-> X2_query_cycle_time[["query_cycle_time<br/>BigQuery"]]
  S3["4. Identificar cuellos de botella y retrabajos"]
  S2 --> S3
  S4["5. Diseñar TO-BE y backlog priorizado"]
  S3 --> S4
  S5["6. Estimar impacto con supuestos"]
  S4 --> S5
  S5 --> R(["Mapa AS-IS/TO-BE (mermaid) - cuellos de botella con evidencia - backlog priorizado - impa…"])
```

## 4. Matriz de inputs, configuración, tools y outputs

| Inputs | Configuración | Tools | Outputs |
|---|---|---|---|
| Solicitud en lenguaje natural vía Gemini Enterprise<br>Identidad del usuario (OAuth A2A)<br>Tokens OAuth por conector<br>Doc: SOP actuales<br>Doc: Métricas operativas<br>Doc: Flujogramas | Harness **Deep**<br>Modelo Gemini Pro - T=0.3<br>System prompt `AGENTS.md`<br>Skills: `process-improvement`, `process-mining-lite`, `automation-business-case`<br>KB `kb-process-optimizer`<br>Guardrails: prompt_injection, off_topic, sql_risk, shell_risk<br>Memoria sin PII | `search_sop` (Knowledge Base)<br>`query_cycle_time` (BigQuery)<br>`draft_automation_map` (Modelo) | Mapa AS-IS / TO-BE, cuellos de botella y backlog de automatización.<br>Worklog y auditoría en VirtuAI<br>Sin efectos en sistemas (solo lectura) |

## 5. Capas de identidad

1. **Gemini Enterprise** — licencia + rol IAM sobre la app del área.
2. **A2A OAuth** — el usuario consiente `a2a:invoke` en VirtuAI (Authorization Code + PKCE).
3. **Conectores** — OAuth individual por MCP; IAM de servicio para Cloud Run con autorización de negocio en backend.
4. **Datos/acciones** — ACL de origen, RBAC, filas y aprobación humana.
