# Arquitectura - Access Governance Analyst

**Área:** Seguridad - **Harness:** Deep - **Acceso:** Lectura - **Complejidad:** 4/5 (alta) - **Impacto:** 4/5 (alto)

## 1. Arquitectura (inputs → configuración → tools → outputs)

```mermaid
flowchart LR
  subgraph IN["Inputs"]
    direction TB
    U(["Usuario corporativo autenticado"])
    Q["Solicitud: Revisa cuentas con permisos excesivos en los sistemas del proyecto."]
    DOCS[/"Documentos: Políticas IAM, Matriz de accesos, Criterios SoD"/]
  end
  subgraph GE["Gemini Enterprise"]
    direction TB
    APP["App ge-seguridad - Custom agent via A2A"]
  end
  subgraph VA["VirtuAI - Access Governance Analyst"]
    direction TB
    GOV{"Governance check: permisos, budget, guardrails"}
    LOOP(("Agentic loop Deep"))
    subgraph CFG["Configuración"]
      direction TB
      H["Harness: Deep - Gemini Pro - T=0.1 - max 8000 tok"]
      SP["System prompt: AGENTS.md"]
      SK["Skills: access-review, orphan-account-check, sod-conflict-check"]
      KB[("KB kb-access-auditor")]
      MEM["Memoria 16 KB - sin PII"]
      GR["Guardrails: prompt_injection, off_topic, sql_risk"]
      SEC["Security: Read-only"]
    end
  end
  subgraph TL["Tools"]
    direction TB
    T_custom["Custom Tool HTTP - Cloud Run (IAM)<br/>list_access_grants"]
    T_mcp_cloud_logging["MCP predefinido - Cloud Logging<br/>get_audit_logs"]
    T_mcp_bigquery["MCP predefinido - BigQuery<br/>query_access_inventory"]
    T_mcp_drive["MCP predefinido - Google Drive<br/>draft_review (Ask)"]
  end
  subgraph SYS["Sistemas externos"]
    direction TB
    S_custom[("API privada / Cloud Run")]
    S_mcp_cloud_logging[("Cloud Logging")]
    S_mcp_bigquery[("BigQuery")]
    S_mcp_drive[("Google Drive")]
  end
  subgraph OUT["Outputs"]
    direction TB
    O1["Inventario de riesgos, evidencias y recomendaciones de revisión."]
    O3["Worklog - auditoría - métricas de uso"]
    O4["KPI: Permisos excesivos detectados, tiempo de recertificación."]
  end
  U --> Q --> APP
  APP -->|"A2A JSON-RPC + OAuth a2a:invoke"| GOV --> LOOP
  CFG -.-> LOOP
  DOCS -.->|"indexación"| KB
  LOOP --> T_custom
  T_custom -->|IAM run.invoker| S_custom
  LOOP --> T_mcp_cloud_logging
  T_mcp_cloud_logging -->|OAuth por usuario| S_mcp_cloud_logging
  LOOP --> T_mcp_bigquery
  T_mcp_bigquery -->|OAuth por usuario| S_mcp_bigquery
  LOOP -->|Ask / aprobación| T_mcp_drive
  T_mcp_drive -->|OAuth por usuario| S_mcp_drive
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
  class T_custom,T_mcp_cloud_logging,T_mcp_bigquery,T_mcp_drive tool
```

## 2. Secuencia de una ejecución (Gemini Enterprise → A2A → VirtuAI)

```mermaid
sequenceDiagram
  autonumber
  actor U as Usuario
  participant GE as Gemini Enterprise
  participant V as VirtuAI - agente
  participant P_custom as Custom Tool
  participant P_mcp_cloud_logging as Cloud Logging
  participant P_mcp_bigquery as BigQuery
  participant P_mcp_drive as Google Drive
  U->>GE: Revisa cuentas con permisos excesivos en los sistemas del proyecto.
  GE->>V: A2A message/stream (Bearer, scope a2a:invoke)
  V->>V: Governance check y carga de skill access-review
  loop Workflow: Definir alcance → Leer permisos → Comparar políticas
    V->>P_custom: list_access_grants
    P_custom-->>V: datos (permisos del usuario)
    V->>P_mcp_cloud_logging: get_audit_logs
    P_mcp_cloud_logging-->>V: datos (permisos del usuario)
    V->>P_mcp_bigquery: query_access_inventory
    P_mcp_bigquery-->>V: datos (permisos del usuario)
  end
  V->>V: flag_excess_privilege (modelo)
  V-->>GE: task input-required (vista previa + approval_requests)
  GE-->>U: Solicitud de aprobación
  alt Aprobado
    U->>GE: Aprobar
    GE->>V: respuesta de aprobación
    V->>P_mcp_drive: draft_review (request_id)
    P_mcp_drive-->>V: OK + ID
  else Denegado o expira
    V->>V: acción queda pendiente, sin reintento
  end
  V-->>GE: Inventario de riesgos, evidencias y recomendaciones de revisión.
  GE-->>U: Respuesta con fuentes y limitaciones
```

## 3. Workflow de la skill principal `access-review`

```mermaid
flowchart TD
  S0["1. Definir alcance (proyectos, sistemas)"]
  S1["2. Listar permisos con list_access_grants"]
  S0 --> S1
  S1 -.-> X1_list_access_grants[["list_access_grants<br/>Custom Tool"]]
  S2["3. Leer uso real con get_audit_logs"]
  S1 --> S2
  S2 -.-> X2_get_audit_logs[["get_audit_logs<br/>Cloud Logging"]]
  S3["4. Comparar vs. políticas IAM y SoD"]
  S2 --> S3
  S4["5. Explicar anomalías con evidencia"]
  S3 --> S4
  S5["6. Preparar revisión para el owner"]
  S4 --> S5
  S5 --> R(["Inventario de riesgos - principal - permiso - último uso - regla violada - recomendación"])
```

## 4. Matriz de inputs, configuración, tools y outputs

| Inputs | Configuración | Tools | Outputs |
|---|---|---|---|
| Solicitud en lenguaje natural vía Gemini Enterprise<br>Identidad del usuario (OAuth A2A)<br>Tokens OAuth por conector<br>Doc: Políticas IAM<br>Doc: Matriz de accesos<br>Doc: Criterios SoD | Harness **Deep**<br>Modelo Gemini Pro - T=0.1<br>System prompt `AGENTS.md`<br>Skills: `access-review`, `orphan-account-check`, `sod-conflict-check`<br>KB `kb-access-auditor`<br>Guardrails: prompt_injection, off_topic, sql_risk<br>Memoria sin PII | `list_access_grants` (Custom Tool)<br>`get_audit_logs` (Cloud Logging)<br>`query_access_inventory` (BigQuery)<br>`flag_excess_privilege` (Modelo)<br>`draft_review` (Google Drive, Ask) | Inventario de riesgos, evidencias y recomendaciones de revisión.<br>Worklog y auditoría en VirtuAI<br>Sin efectos en sistemas (solo lectura) |

## 5. Capas de identidad

1. **Gemini Enterprise** — licencia + rol IAM sobre la app del área.
2. **A2A OAuth** — el usuario consiente `a2a:invoke` en VirtuAI (Authorization Code + PKCE).
3. **Conectores** — OAuth individual por MCP; IAM de servicio para Cloud Run con autorización de negocio en backend.
4. **Datos/acciones** — ACL de origen, RBAC, filas y aprobación humana.
