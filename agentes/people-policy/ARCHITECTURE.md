# Arquitectura - People Policy Advisor

**Área:** Talento - **Harness:** Classic - **Acceso:** Lectura - **Complejidad:** 1/5 (muy baja) - **Impacto:** 4/5 (alto)

## 1. Arquitectura (inputs → configuración → tools → outputs)

```mermaid
flowchart LR
  subgraph IN["Inputs"]
    direction TB
    U(["Usuario corporativo autenticado"])
    Q["Solicitud: ¿Cuál es la política de viáticos cuando viajo de Colombia a Chile?"]
    DOCS[/"Documentos: Reglamento interno, Vacaciones, Viáticos, Beneficios, Políticas por país"/]
  end
  subgraph GE["Gemini Enterprise"]
    direction TB
    APP["App ge-talento - Custom agent via A2A"]
  end
  subgraph VA["VirtuAI - People Policy Advisor"]
    direction TB
    GOV{"Governance check: permisos, budget, guardrails"}
    LOOP(("Agentic loop Classic"))
    subgraph CFG["Configuración"]
      direction TB
      H["Harness: Classic - Gemini Flash - T=0.1 - max 3000 tok"]
      SP["System prompt: AGENTS.md"]
      SK["Procedimientos: policy-answer, policy-gap-escalation"]
      KB[("KB kb-people-policy")]
      GR["Guardrails: prompt_injection, off_topic"]
      SEC["Security: Read-only"]
    end
  end
  subgraph TL["Tools"]
    direction TB
    T_kb["Knowledge Base de VirtuAI (RAG)<br/>search_approved_policy"]
    T_mcp_drive["MCP predefinido - Google Drive<br/>get_policy_version"]
  end
  subgraph SYS["Sistemas externos"]
    direction TB
    S_mcp_drive[("Google Drive")]
  end
  subgraph OUT["Outputs"]
    direction TB
    O1["Respuesta documentada con política, fecha y ruta de escalamiento."]
    O3["Worklog - auditoría - métricas de uso"]
    O4["KPI: Reducción de preguntas repetidas, precisión normativa."]
  end
  U --> Q --> APP
  APP -->|"A2A JSON-RPC + OAuth a2a:invoke"| GOV --> LOOP
  CFG -.-> LOOP
  DOCS -.->|"indexación"| KB
  LOOP --> T_kb
  LOOP --> T_mcp_drive
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
  class T_kb,T_mcp_drive tool
```

## 2. Secuencia de una ejecución (Gemini Enterprise → A2A → VirtuAI)

```mermaid
sequenceDiagram
  autonumber
  actor U as Usuario
  participant GE as Gemini Enterprise
  participant V as VirtuAI - agente
  participant P_kb as Knowledge Base
  participant P_mcp_drive as Google Drive
  U->>GE: ¿Cuál es la política de viáticos cuando viajo de Colombia a Chile?
  GE->>V: A2A message/stream (Bearer, scope a2a:invoke)
  V->>V: Governance check y carga de skill policy-answer
  loop Workflow: Entender consulta → Identificar país → Buscar política
    V->>P_kb: search_approved_policy
    P_kb-->>V: datos (permisos del usuario)
    V->>P_mcp_drive: get_policy_version
    P_mcp_drive-->>V: datos (permisos del usuario)
  end
  V-->>GE: Respuesta documentada con política, fecha y ruta de escalamiento.
  GE-->>U: Respuesta con fuentes y limitaciones
```

## 3. Workflow de la skill principal `policy-answer`

```mermaid
flowchart TD
  S0["1. Identificar país y tipo de política"]
  S1["2. Buscar fragmento con search_approved_policy"]
  S0 --> S1
  S1 -.-> X1_search_approved_policy[["search_approved_policy<br/>Knowledge Base"]]
  S2["3. Verificar vigencia con get_policy_version"]
  S1 --> S2
  S2 -.-> X2_get_policy_version[["get_policy_version<br/>Google Drive"]]
  S3["4. Responder citando documento, sección y fecha"]
  S2 --> S3
  S4["5. Indicar ruta de escalamiento a RR. HH."]
  S3 --> S4
  S4 --> R(["Respuesta corta - cita textual - documento y fecha - escalamiento"])
```

## 4. Matriz de inputs, configuración, tools y outputs

| Inputs | Configuración | Tools | Outputs |
|---|---|---|---|
| Solicitud en lenguaje natural vía Gemini Enterprise<br>Identidad del usuario (OAuth A2A)<br>Tokens OAuth por conector<br>Doc: Reglamento interno<br>Doc: Vacaciones<br>Doc: Viáticos<br>Doc: Beneficios<br>Doc: Políticas por país | Harness **Classic**<br>Modelo Gemini Flash - T=0.1<br>System prompt `AGENTS.md`<br>Procedimientos: `policy-answer`, `policy-gap-escalation`<br>KB `kb-people-policy`<br>Guardrails: prompt_injection, off_topic | `search_approved_policy` (Knowledge Base)<br>`get_policy_version` (Google Drive) | Respuesta documentada con política, fecha y ruta de escalamiento.<br>Worklog y auditoría en VirtuAI<br>Sin efectos en sistemas (solo lectura) |

## 5. Capas de identidad

1. **Gemini Enterprise** — licencia + rol IAM sobre la app del área.
2. **A2A OAuth** — el usuario consiente `a2a:invoke` en VirtuAI (Authorization Code + PKCE).
3. **Conectores** — OAuth individual por MCP; IAM de servicio para Cloud Run con autorización de negocio en backend.
4. **Datos/acciones** — ACL de origen, RBAC, filas y aprobación humana.
