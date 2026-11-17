# Arquitectura - Executive Intelligence

**Área:** Dirección - **Harness:** Deep - **Acceso:** Lectura - **Complejidad:** 2/5 (baja) - **Impacto:** 4/5 (alto)

## 1. Arquitectura (inputs → configuración → tools → outputs)

```mermaid
flowchart LR
  subgraph IN["Inputs"]
    direction TB
    U(["Usuario corporativo autenticado"])
    Q["Solicitud: Resume resultados de esta semana, riesgos y decisiones pendientes para comité."]
    DOCS[/"Documentos: OKR y KPIs, Actas ejecutivas, Reportes de dirección"/]
  end
  subgraph GE["Gemini Enterprise"]
    direction TB
    APP["App ge-dirección - Custom agent via A2A"]
  end
  subgraph VA["VirtuAI - Executive Intelligence"]
    direction TB
    GOV{"Governance check: permisos, budget, guardrails"}
    LOOP(("Agentic loop Deep"))
    subgraph CFG["Configuración"]
      direction TB
      H["Harness: Deep - Gemini Pro - T=0.2 - max 8000 tok"]
      SP["System prompt: AGENTS.md"]
      SK["Skills: executive-report, kpi-variance-explainer, decision-log-tracker"]
      KB[("KB kb-executive-brief")]
      MEM["Memoria 16 KB - sin PII"]
      GR["Guardrails: prompt_injection, off_topic, sql_risk"]
      SEC["Security: Read-only"]
    end
  end
  subgraph TL["Tools"]
    direction TB
    T_mcp_bigquery["MCP predefinido - BigQuery<br/>get_kpis"]
    T_mcp_drive["MCP predefinido - Google Drive<br/>search_drive"]
    T_mcp_gmail["MCP predefinido - Gmail<br/>search_mail"]
  end
  subgraph SYS["Sistemas externos"]
    direction TB
    S_mcp_bigquery[("BigQuery")]
    S_mcp_drive[("Google Drive")]
    S_mcp_gmail[("Gmail")]
  end
  subgraph OUT["Outputs"]
    direction TB
    O1["Resumen ejecutivo con KPIs, tendencias, riesgos, decisiones y links a fuentes."]
    O3["Worklog - auditoría - métricas de uso"]
    O4["KPI: Tiempo ahorrado por reporte, % afirmaciones con fuente."]
  end
  U --> Q --> APP
  APP -->|"A2A JSON-RPC + OAuth a2a:invoke"| GOV --> LOOP
  CFG -.-> LOOP
  DOCS -.->|"indexación"| KB
  LOOP --> T_mcp_bigquery
  T_mcp_bigquery -->|OAuth por usuario| S_mcp_bigquery
  LOOP --> T_mcp_drive
  T_mcp_drive -->|OAuth por usuario| S_mcp_drive
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
  class T_mcp_bigquery,T_mcp_drive,T_mcp_gmail tool
```

## 2. Secuencia de una ejecución (Gemini Enterprise → A2A → VirtuAI)

```mermaid
sequenceDiagram
  autonumber
  actor U as Usuario
  participant GE as Gemini Enterprise
  participant V as VirtuAI - agente
  participant P_mcp_bigquery as BigQuery
  participant P_mcp_drive as Google Drive
  participant P_mcp_gmail as Gmail
  U->>GE: Resume resultados de esta semana, riesgos y decisiones pendientes para comité.
  GE->>V: A2A message/stream (Bearer, scope a2a:invoke)
  V->>V: Governance check y carga de skill executive-report
  loop Workflow: Solicitar panorama → Consultar métricas → Cruzar decisiones
    V->>P_mcp_bigquery: get_kpis
    P_mcp_bigquery-->>V: datos (permisos del usuario)
    V->>P_mcp_drive: search_drive
    P_mcp_drive-->>V: datos (permisos del usuario)
    V->>P_mcp_gmail: search_mail
    P_mcp_gmail-->>V: datos (permisos del usuario)
  end
  V->>V: draft_executive_brief (modelo)
  V-->>GE: Resumen ejecutivo con KPIs, tendencias, riesgos, decisiones y links a fuentes.
  GE-->>U: Respuesta con fuentes y limitaciones
```

## 3. Workflow de la skill principal `executive-report`

```mermaid
flowchart TD
  S0["1. Confirmar periodo, unidad de negocio y audiencia del briefing"]
  S1["2. Consultar KPIs con get_kpis y registrar fecha de corte de cada métrica"]
  S0 --> S1
  S1 -.-> X1_get_kpis[["get_kpis<br/>BigQuery"]]
  S2["3. Buscar actas y reportes del periodo con search_drive, extraer decisiones y comp…"]
  S1 --> S2
  S2 -.-> X2_search_drive[["search_drive<br/>Google Drive"]]
  S3["4. Cruzar variaciones de KPIs con decisiones y riesgos documentados"]
  S2 --> S3
  S4["5. Redactar el briefing con draft_executive_brief citando fuente por cada cifra"]
  S3 --> S4
  S4 -.-> X4_draft_executive_brief[["draft_executive_brief<br/>Modelo"]]
  S5["6. Revisar que ninguna cifra quede sin fuente, marcar las faltantes como 'sin dato'"]
  S4 --> S5
  S5 --> R(["Resumen (5 bullets) - Tabla KPI (valor, meta, variación, corte, fuente) - Riesgos - Decis…"])
```

## 4. Matriz de inputs, configuración, tools y outputs

| Inputs | Configuración | Tools | Outputs |
|---|---|---|---|
| Solicitud en lenguaje natural vía Gemini Enterprise<br>Identidad del usuario (OAuth A2A)<br>Tokens OAuth por conector<br>Doc: OKR y KPIs<br>Doc: Actas ejecutivas<br>Doc: Reportes de dirección | Harness **Deep**<br>Modelo Gemini Pro - T=0.2<br>System prompt `AGENTS.md`<br>Skills: `executive-report`, `kpi-variance-explainer`, `decision-log-tracker`<br>KB `kb-executive-brief`<br>Guardrails: prompt_injection, off_topic, sql_risk<br>Memoria sin PII | `get_kpis` (BigQuery)<br>`search_drive` (Google Drive)<br>`search_mail` (Gmail)<br>`draft_executive_brief` (Modelo) | Resumen ejecutivo con KPIs, tendencias, riesgos, decisiones y links a fuentes.<br>Worklog y auditoría en VirtuAI<br>Sin efectos en sistemas (solo lectura) |

## 5. Capas de identidad

1. **Gemini Enterprise** — licencia + rol IAM sobre la app del área.
2. **A2A OAuth** — el usuario consiente `a2a:invoke` en VirtuAI (Authorization Code + PKCE).
3. **Conectores** — OAuth individual por MCP; IAM de servicio para Cloud Run con autorización de negocio en backend.
4. **Datos/acciones** — ACL de origen, RBAC, filas y aprobación humana.
