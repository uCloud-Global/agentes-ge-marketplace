# Arquitectura - Customer Support Resolver

**Área:** Clientes - **Harness:** Deep - **Acceso:** Escritura con aprobación - **Complejidad:** 4/5 (alta) - **Impacto:** 5/5 (muy alto)

## 1. Arquitectura (inputs → configuración → tools → outputs)

```mermaid
flowchart LR
  subgraph IN["Inputs"]
    direction TB
    U(["Usuario corporativo autenticado"])
    Q["Solicitud: Un cliente reclama por un cobro duplicado: revisa antecedentes y prepara respuesta."]
    DOCS[/"Documentos: FAQs, SLA, Políticas de devolución, Base de soluciones"/]
  end
  subgraph GE["Gemini Enterprise"]
    direction TB
    APP["App ge-clientes - Custom agent via A2A"]
  end
  subgraph VA["VirtuAI - Customer Support Resolver"]
    direction TB
    GOV{"Governance check: permisos, budget, guardrails"}
    LOOP(("Agentic loop Deep"))
    subgraph CFG["Configuración"]
      direction TB
      H["Harness: Deep - Gemini Pro - T=0.3 - max 5000 tok"]
      SP["System prompt: AGENTS.md"]
      SK["Skills: support-resolution, escalation-triage, refund-policy-check"]
      KB[("KB kb-support-resolver")]
      MEM["Memoria 16 KB - sin PII"]
      GR["Guardrails: prompt_injection, off_topic, sentiment, urgency"]
      SEC["Security: Ask before each call - HITL"]
    end
  end
  subgraph TL["Tools"]
    direction TB
    T_mcp_hubspot["MCP predefinido - HubSpot<br/>lookup_customer<br/>get_ticket<br/>update_ticket (Ask)"]
    T_kb["Knowledge Base de VirtuAI (RAG)<br/>search_kb"]
    T_mcp_gmail["MCP predefinido - Gmail<br/>draft_reply (Ask)"]
  end
  subgraph SYS["Sistemas externos"]
    direction TB
    S_mcp_hubspot[("HubSpot CRM")]
    S_mcp_gmail[("Gmail")]
  end
  subgraph OUT["Outputs"]
    direction TB
    O1["Diagnóstico, solución fundamentada, borrador de respuesta y escalamiento."]
    O2["Aprobaciones input-required"]
    O3["Worklog - auditoría - métricas de uso"]
    O4["KPI: Resolución en primer contacto, tiempo medio de atención."]
  end
  U --> Q --> APP
  APP -->|"A2A JSON-RPC + OAuth a2a:invoke"| GOV --> LOOP
  CFG -.-> LOOP
  DOCS -.->|"indexación"| KB
  LOOP -->|Ask / aprobación| T_mcp_hubspot
  T_mcp_hubspot -->|OAuth por usuario| S_mcp_hubspot
  LOOP --> T_kb
  LOOP -->|Ask / aprobación| T_mcp_gmail
  T_mcp_gmail -->|OAuth por usuario| S_mcp_gmail
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
  class T_mcp_hubspot,T_kb,T_mcp_gmail tool
```

## 2. Secuencia de una ejecución (Gemini Enterprise → A2A → VirtuAI)

```mermaid
sequenceDiagram
  autonumber
  actor U as Usuario
  participant GE as Gemini Enterprise
  participant V as VirtuAI - agente
  participant P_mcp_hubspot as HubSpot
  participant P_kb as Knowledge Base
  participant P_mcp_gmail as Gmail
  U->>GE: Un cliente reclama por un cobro duplicado: revisa antecedentes y prepara respue…
  GE->>V: A2A message/stream (Bearer, scope a2a:invoke)
  V->>V: Governance check y carga de skill support-resolution
  loop Workflow: Identificar caso → Consultar historial → Buscar política
    V->>P_mcp_hubspot: lookup_customer
    P_mcp_hubspot-->>V: datos (permisos del usuario)
    V->>P_kb: search_kb
    P_kb-->>V: datos (permisos del usuario)
    V->>P_mcp_hubspot: get_ticket
    P_mcp_hubspot-->>V: datos (permisos del usuario)
  end
  V-->>GE: task input-required (vista previa + approval_requests)
  GE-->>U: Solicitud de aprobación
  alt Aprobado
    U->>GE: Aprobar
    GE->>V: respuesta de aprobación
    V->>P_mcp_gmail: draft_reply (request_id)
    P_mcp_gmail-->>V: OK + ID
    V->>P_mcp_hubspot: update_ticket (request_id)
    P_mcp_hubspot-->>V: OK + ID
  else Denegado o expira
    V->>V: acción queda pendiente, sin reintento
  end
  V-->>GE: Diagnóstico, solución fundamentada, borrador de respuesta y escalamiento.
  GE-->>U: Respuesta con fuentes y limitaciones
```

## 3. Workflow de la skill principal `support-resolution`

```mermaid
flowchart TD
  S0["1. Identificar cliente y validar identidad con lookup_customer"]
  S0 -.-> X0_lookup_customer[["lookup_customer<br/>HubSpot"]]
  S1["2. Leer historial y ticket con get_ticket"]
  S0 --> S1
  S1 -.-> X1_get_ticket[["get_ticket<br/>HubSpot"]]
  S2["3. Buscar política aplicable con search_kb"]
  S1 --> S2
  S2 -.-> X2_search_kb[["search_kb<br/>Knowledge Base"]]
  S3["4. Diagnosticar y preparar solución fundamentada en política"]
  S2 --> S3
  S4["5. Crear borrador con draft_reply"]
  S3 --> S4
  S4 -.-> X4_draft_reply[["draft_reply<br/>Gmail"]]
  style X4_draft_reply fill:#fce8e6,stroke:#ea4335
  S5["6. Pedir aprobación para update_ticket o escalar"]
  S4 --> S5
  S5 -.-> X5_update_ticket[["update_ticket<br/>HubSpot"]]
  style X5_update_ticket fill:#fce8e6,stroke:#ea4335
  S5 --> R(["Diagnóstico - política aplicada (cita) - solución - borrador - acción propuesta / escalam…"])
```

## 4. Matriz de inputs, configuración, tools y outputs

| Inputs | Configuración | Tools | Outputs |
|---|---|---|---|
| Solicitud en lenguaje natural vía Gemini Enterprise<br>Identidad del usuario (OAuth A2A)<br>Tokens OAuth por conector<br>Doc: FAQs<br>Doc: SLA<br>Doc: Políticas de devolución<br>Doc: Base de soluciones | Harness **Deep**<br>Modelo Gemini Pro - T=0.3<br>System prompt `AGENTS.md`<br>Skills: `support-resolution`, `escalation-triage`, `refund-policy-check`<br>KB `kb-support-resolver`<br>Guardrails: prompt_injection, off_topic, sentiment, urgency<br>Memoria sin PII | `lookup_customer` (HubSpot)<br>`search_kb` (Knowledge Base)<br>`get_ticket` (HubSpot)<br>`draft_reply` (Gmail, Ask)<br>`update_ticket` (HubSpot, Ask) | Diagnóstico, solución fundamentada, borrador de respuesta y escalamiento.<br>Worklog y auditoría en VirtuAI<br>Acciones pendientes de aprobación |

## 5. Capas de identidad

1. **Gemini Enterprise** — licencia + rol IAM sobre la app del área.
2. **A2A OAuth** — el usuario consiente `a2a:invoke` en VirtuAI (Authorization Code + PKCE).
3. **Conectores** — OAuth individual por MCP; IAM de servicio para Cloud Run con autorización de negocio en backend.
4. **Datos/acciones** — ACL de origen, RBAC, filas y aprobación humana.
