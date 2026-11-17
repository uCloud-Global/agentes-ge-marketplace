# Arquitectura - IT Helpdesk Concierge

**Área:** Tecnología - **Harness:** Deep - **Acceso:** Escritura con aprobación - **Complejidad:** 3/5 (media) - **Impacto:** 5/5 (muy alto)

## 1. Arquitectura (inputs → configuración → tools → outputs)

```mermaid
flowchart LR
  subgraph IN["Inputs"]
    direction TB
    U(["Usuario corporativo autenticado"])
    Q["Solicitud: No puedo ingresar a la VPN. ¿Qué debo probar y puedes crear un ticket?"]
    DOCS[/"Documentos: Runbooks de soporte, FAQ TI, Catálogo de servicios"/]
  end
  subgraph GE["Gemini Enterprise"]
    direction TB
    APP["App ge-tecnología - Custom agent via A2A"]
  end
  subgraph VA["VirtuAI - IT Helpdesk Concierge"]
    direction TB
    GOV{"Governance check: permisos, budget, guardrails"}
    LOOP(("Agentic loop Deep"))
    subgraph CFG["Configuración"]
      direction TB
      H["Harness: Deep - Gemini Flash - T=0.2 - max 4000 tok"]
      SP["System prompt: AGENTS.md"]
      SK["Skills: helpdesk-triage, password-reset-guidance, service-catalog-request"]
      KB[("KB kb-it-helpdesk")]
      MEM["Memoria 16 KB - sin PII"]
      GR["Guardrails: prompt_injection, off_topic, urgency, sentiment"]
      SEC["Security: Ask before each call - HITL"]
    end
  end
  subgraph TL["Tools"]
    direction TB
    T_kb["Knowledge Base de VirtuAI (RAG)<br/>search_runbook"]
    T_custom["Custom Tool HTTP - Cloud Run (IAM)<br/>lookup_asset<br/>create_ticket (Ask)"]
  end
  subgraph SYS["Sistemas externos"]
    direction TB
    S_custom[("API privada / Cloud Run")]
  end
  subgraph OUT["Outputs"]
    direction TB
    O1["Pasos de diagnóstico y ticket prellenado sujeto a aprobación."]
    O2["Aprobaciones input-required"]
    O3["Worklog - auditoría - métricas de uso"]
    O4["KPI: Resolución automática, tiempo de atención."]
  end
  U --> Q --> APP
  APP -->|"A2A JSON-RPC + OAuth a2a:invoke"| GOV --> LOOP
  CFG -.-> LOOP
  DOCS -.->|"indexación"| KB
  LOOP --> T_kb
  LOOP -->|Ask / aprobación| T_custom
  T_custom -->|IAM run.invoker| S_custom
  LOOP --> O1
  LOOP --> O3
  LOOP --> O2
  O1 -->|"respuesta A2A streaming"| APP
  classDef inp fill:#e8f0fe,stroke:#1a73e8,color:#15213d
  classDef out fill:#e6f4ea,stroke:#34a853,color:#15213d
  classDef cfg fill:#fff8e1,stroke:#fbbc04,color:#15213d
  classDef tool fill:#fce8e6,stroke:#ea4335,color:#15213d
  class U,Q,DOCS inp
  class O1,O3,O4 out
  class H,SP,SK,KB,GR,SEC cfg
  class MEM cfg
  class O2 out
  class T_kb,T_custom tool
```

## 2. Secuencia de una ejecución (Gemini Enterprise → A2A → VirtuAI)

```mermaid
sequenceDiagram
  autonumber
  actor U as Usuario
  participant GE as Gemini Enterprise
  participant V as VirtuAI - agente
  participant P_kb as Knowledge Base
  participant P_custom as Custom Tool
  U->>GE: No puedo ingresar a la VPN. ¿Qué debo probar y puedes crear un ticket?
  GE->>V: A2A message/stream (Bearer, scope a2a:invoke)
  V->>V: Governance check y carga de skill helpdesk-triage
  loop Workflow: Clasificar solicitud → Consultar runbook → Orientar solución
    V->>P_kb: search_runbook
    P_kb-->>V: datos (permisos del usuario)
    V->>P_custom: lookup_asset
    P_custom-->>V: datos (permisos del usuario)
  end
  V->>V: draft_ticket (modelo)
  V-->>GE: task input-required (vista previa + approval_requests)
  GE-->>U: Solicitud de aprobación
  alt Aprobado
    U->>GE: Aprobar
    GE->>V: respuesta de aprobación
    V->>P_custom: create_ticket (request_id)
    P_custom-->>V: OK + ID
  else Denegado o expira
    V->>V: acción queda pendiente, sin reintento
  end
  V-->>GE: Pasos de diagnóstico y ticket prellenado sujeto a aprobación.
  GE-->>U: Respuesta con fuentes y limitaciones
```

## 3. Workflow de la skill principal `helpdesk-triage`

```mermaid
flowchart TD
  S0["1. Clasificar solicitud (acceso, hardware, software, red, cuenta)"]
  S1["2. Buscar runbook con search_runbook"]
  S0 --> S1
  S1 -.-> X1_search_runbook[["search_runbook<br/>Knowledge Base"]]
  S2["3. Guiar diagnóstico paso a paso, sin pedir contraseñas"]
  S1 --> S2
  S3["4. Si no se resuelve, consultar activo con lookup_asset y prellenar con draft_tick…"]
  S2 --> S3
  S3 -.-> X3_lookup_asset[["lookup_asset<br/>Custom Tool"]]
  S3 -.-> X3_draft_ticket[["draft_ticket<br/>Modelo"]]
  S4["5. Pedir aprobación antes de create_ticket"]
  S3 --> S4
  S4 -.-> X4_create_ticket[["create_ticket<br/>Custom Tool"]]
  style X4_create_ticket fill:#fce8e6,stroke:#ea4335
  S4 --> R(["Pasos realizados - resultado - ticket propuesto (categoría, prioridad, descripción)"])
```

## 4. Matriz de inputs, configuración, tools y outputs

| Inputs | Configuración | Tools | Outputs |
|---|---|---|---|
| Solicitud en lenguaje natural vía Gemini Enterprise<br>Identidad del usuario (OAuth A2A)<br>Tokens OAuth por conector<br>Doc: Runbooks de soporte<br>Doc: FAQ TI<br>Doc: Catálogo de servicios | Harness **Deep**<br>Modelo Gemini Flash - T=0.2<br>System prompt `AGENTS.md`<br>Skills: `helpdesk-triage`, `password-reset-guidance`, `service-catalog-request`<br>KB `kb-it-helpdesk`<br>Guardrails: prompt_injection, off_topic, urgency, sentiment<br>Memoria sin PII | `search_runbook` (Knowledge Base)<br>`lookup_asset` (Custom Tool)<br>`draft_ticket` (Modelo)<br>`create_ticket` (Custom Tool, Ask) | Pasos de diagnóstico y ticket prellenado sujeto a aprobación.<br>Worklog y auditoría en VirtuAI<br>Acciones pendientes de aprobación |

## 5. Capas de identidad

1. **Gemini Enterprise** — licencia + rol IAM sobre la app del área.
2. **A2A OAuth** — el usuario consiente `a2a:invoke` en VirtuAI (Authorization Code + PKCE).
3. **Conectores** — OAuth individual por MCP; IAM de servicio para Cloud Run con autorización de negocio en backend.
4. **Datos/acciones** — ACL de origen, RBAC, filas y aprobación humana.
