# Arquitectura - Supplier Risk Analyst

**Área:** Compras - **Harness:** Deep - **Acceso:** Lectura - **Complejidad:** 3/5 (media) - **Impacto:** 3/5 (medio)

## 1. Arquitectura (inputs → configuración → tools → outputs)

```mermaid
flowchart LR
  subgraph IN["Inputs"]
    direction TB
    U(["Usuario corporativo autenticado"])
    Q["Solicitud: ¿Cuáles proveedores muestran incumplimientos recurrentes este trimestre?"]
    DOCS[/"Documentos: Contratos proveedores, Matriz homologación, SLA, Código de conducta"/]
  end
  subgraph GE["Gemini Enterprise"]
    direction TB
    APP["App ge-compras - Custom agent via A2A"]
  end
  subgraph VA["VirtuAI - Supplier Risk Analyst"]
    direction TB
    GOV{"Governance check: permisos, budget, guardrails"}
    LOOP(("Agentic loop Deep"))
    subgraph CFG["Configuración"]
      direction TB
      H["Harness: Deep - Gemini Pro - T=0.2 - max 6000 tok"]
      SP["System prompt: AGENTS.md"]
      SK["Skills: supplier-assessment, sla-breach-review, supplier-scorecard"]
      KB[("KB kb-supplier-risk")]
      MEM["Memoria 16 KB - sin PII"]
      GR["Guardrails: prompt_injection, off_topic, sql_risk"]
      SEC["Security: Read-only"]
    end
  end
  subgraph TL["Tools"]
    direction TB
    T_mcp_bigquery["MCP predefinido - BigQuery<br/>get_supplier_kpis"]
    T_mcp_drive["MCP predefinido - Google Drive<br/>search_contract"]
    T_custom["Custom Tool HTTP - Cloud Run (IAM)<br/>score_risk"]
  end
  subgraph SYS["Sistemas externos"]
    direction TB
    S_mcp_bigquery[("BigQuery")]
    S_mcp_drive[("Google Drive")]
    S_custom[("API privada / Cloud Run")]
  end
  subgraph OUT["Outputs"]
    direction TB
    O1["Ranking de riesgo, evidencia y plan de revisión."]
    O3["Worklog - auditoría - métricas de uso"]
    O4["KPI: Tiempo de homologación, incidencias detectadas."]
  end
  U --> Q --> APP
  APP -->|"A2A JSON-RPC + OAuth a2a:invoke"| GOV --> LOOP
  CFG -.-> LOOP
  DOCS -.->|"indexación"| KB
  LOOP --> T_mcp_bigquery
  T_mcp_bigquery -->|OAuth por usuario| S_mcp_bigquery
  LOOP --> T_mcp_drive
  T_mcp_drive -->|OAuth por usuario| S_mcp_drive
  LOOP --> T_custom
  T_custom -->|IAM run.invoker| S_custom
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
  class T_mcp_bigquery,T_mcp_drive,T_custom tool
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
  participant P_custom as Custom Tool
  U->>GE: ¿Cuáles proveedores muestran incumplimientos recurrentes este trimestre?
  GE->>V: A2A message/stream (Bearer, scope a2a:invoke)
  V->>V: Governance check y carga de skill supplier-assessment
  loop Workflow: Consultar proveedor → Cruzar entregas → Verificar contrato
    V->>P_mcp_bigquery: get_supplier_kpis
    P_mcp_bigquery-->>V: datos (permisos del usuario)
    V->>P_mcp_drive: search_contract
    P_mcp_drive-->>V: datos (permisos del usuario)
    V->>P_custom: score_risk
    P_custom-->>V: datos (permisos del usuario)
  end
  V->>V: prepare_review (modelo)
  V-->>GE: Ranking de riesgo, evidencia y plan de revisión.
  GE-->>U: Respuesta con fuentes y limitaciones
```

## 3. Workflow de la skill principal `supplier-assessment`

```mermaid
flowchart TD
  S0["1. Consultar KPIs con get_supplier_kpis"]
  S0 -.-> X0_get_supplier_kpis[["get_supplier_kpis<br/>BigQuery"]]
  S1["2. Verificar obligaciones con search_contract"]
  S0 --> S1
  S1 -.-> X1_search_contract[["search_contract<br/>Google Drive"]]
  S2["3. Calcular score con score_risk"]
  S1 --> S2
  S2 -.-> X2_score_risk[["score_risk<br/>Custom Tool"]]
  S3["4. Explicar riesgo por dimensión"]
  S2 --> S3
  S4["5. Recomendar acción para aprobación"]
  S3 --> S4
  S4 --> R(["Ranking - score por dimensión - evidencia - acción recomendada"])
```

## 4. Matriz de inputs, configuración, tools y outputs

| Inputs | Configuración | Tools | Outputs |
|---|---|---|---|
| Solicitud en lenguaje natural vía Gemini Enterprise<br>Identidad del usuario (OAuth A2A)<br>Tokens OAuth por conector<br>Doc: Contratos proveedores<br>Doc: Matriz homologación<br>Doc: SLA<br>Doc: Código de conducta | Harness **Deep**<br>Modelo Gemini Pro - T=0.2<br>System prompt `AGENTS.md`<br>Skills: `supplier-assessment`, `sla-breach-review`, `supplier-scorecard`<br>KB `kb-supplier-risk`<br>Guardrails: prompt_injection, off_topic, sql_risk<br>Memoria sin PII | `get_supplier_kpis` (BigQuery)<br>`search_contract` (Google Drive)<br>`score_risk` (Custom Tool)<br>`prepare_review` (Modelo) | Ranking de riesgo, evidencia y plan de revisión.<br>Worklog y auditoría en VirtuAI<br>Sin efectos en sistemas (solo lectura) |

## 5. Capas de identidad

1. **Gemini Enterprise** — licencia + rol IAM sobre la app del área.
2. **A2A OAuth** — el usuario consiente `a2a:invoke` en VirtuAI (Authorization Code + PKCE).
3. **Conectores** — OAuth individual por MCP; IAM de servicio para Cloud Run con autorización de negocio en backend.
4. **Datos/acciones** — ACL de origen, RBAC, filas y aprobación humana.
