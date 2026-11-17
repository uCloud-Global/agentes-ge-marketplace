# Arquitectura - Contract Review Assistant

**Área:** Legal - **Harness:** Deep - **Acceso:** Lectura - **Complejidad:** 3/5 (media) - **Impacto:** 4/5 (alto)

## 1. Arquitectura (inputs → configuración → tools → outputs)

```mermaid
flowchart LR
  subgraph IN["Inputs"]
    direction TB
    U(["Usuario corporativo autenticado"])
    Q["Solicitud: Revisa este NDA e identifica desviaciones frente a nuestro estándar."]
    DOCS[/"Documentos: Plantillas aprobadas, Playbook de cláusulas, Política de firmas"/]
  end
  subgraph GE["Gemini Enterprise"]
    direction TB
    APP["App ge-legal - Custom agent via A2A"]
  end
  subgraph VA["VirtuAI - Contract Review Assistant"]
    direction TB
    GOV{"Governance check: permisos, budget, guardrails"}
    LOOP(("Agentic loop Deep"))
    subgraph CFG["Configuración"]
      direction TB
      H["Harness: Deep - Gemini Pro - T=0.1 - max 10000 tok"]
      SP["System prompt: AGENTS.md"]
      SK["Skills: contract-review, nda-quick-check, obligation-extractor"]
      KB[("KB kb-contract-reviewer")]
      MEM["Memoria 16 KB - sin PII"]
      GR["Guardrails: prompt_injection, off_topic"]
      SEC["Security: Read-only"]
    end
  end
  subgraph TL["Tools"]
    direction TB
    T_mcp_drive["MCP predefinido - Google Drive<br/>read_contract"]
    T_kb["Knowledge Base de VirtuAI (RAG)<br/>search_playbook"]
  end
  subgraph SYS["Sistemas externos"]
    direction TB
    S_mcp_drive[("Google Drive")]
  end
  subgraph OUT["Outputs"]
    direction TB
    O1["Informe de cláusulas, severidad, citas y texto alternativo sugerido."]
    O3["Worklog - auditoría - métricas de uso"]
    O4["KPI: Tiempo de primera revisión, % hallazgos aceptados."]
  end
  U --> Q --> APP
  APP -->|"A2A JSON-RPC + OAuth a2a:invoke"| GOV --> LOOP
  CFG -.-> LOOP
  DOCS -.->|"indexación"| KB
  LOOP --> T_mcp_drive
  T_mcp_drive -->|OAuth por usuario| S_mcp_drive
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
  class T_mcp_drive,T_kb tool
```

## 2. Secuencia de una ejecución (Gemini Enterprise → A2A → VirtuAI)

```mermaid
sequenceDiagram
  autonumber
  actor U as Usuario
  participant GE as Gemini Enterprise
  participant V as VirtuAI - agente
  participant P_mcp_drive as Google Drive
  participant P_kb as Knowledge Base
  U->>GE: Revisa este NDA e identifica desviaciones frente a nuestro estándar.
  GE->>V: A2A message/stream (Bearer, scope a2a:invoke)
  V->>V: Governance check y carga de skill contract-review
  loop Workflow: Localizar contrato → Extraer cláusulas → Comparar estándar
    V->>P_mcp_drive: read_contract
    P_mcp_drive-->>V: datos (permisos del usuario)
    V->>P_kb: search_playbook
    P_kb-->>V: datos (permisos del usuario)
  end
  V->>V: compare_clauses, draft_redlines (modelo)
  V-->>GE: Informe de cláusulas, severidad, citas y texto alternativo sugerido.
  GE-->>U: Respuesta con fuentes y limitaciones
```

## 3. Workflow de la skill principal `contract-review`

```mermaid
flowchart TD
  S0["1. Leer contrato con read_contract"]
  S0 -.-> X0_read_contract[["read_contract<br/>Google Drive"]]
  S1["2. Extraer cláusulas clave (objeto, plazo, responsabilidad, indemnidad, confidenci…"]
  S0 --> S1
  S2["3. Comparar con playbook usando search_playbook y compare_clauses"]
  S1 --> S2
  S2 -.-> X2_compare_clauses[["compare_clauses<br/>Modelo"]]
  S2 -.-> X2_search_playbook[["search_playbook<br/>Knowledge Base"]]
  S3["4. Asignar severidad (alta/media/baja) por desviación"]
  S2 --> S3
  S4["5. Proponer redlines con draft_redlines"]
  S3 --> S4
  S4 -.-> X4_draft_redlines[["draft_redlines<br/>Modelo"]]
  S4 --> R(["Tabla cláusula - texto actual (cita) - estándar - desviación - severidad - redline sugeri…"])
```

## 4. Matriz de inputs, configuración, tools y outputs

| Inputs | Configuración | Tools | Outputs |
|---|---|---|---|
| Solicitud en lenguaje natural vía Gemini Enterprise<br>Identidad del usuario (OAuth A2A)<br>Tokens OAuth por conector<br>Doc: Plantillas aprobadas<br>Doc: Playbook de cláusulas<br>Doc: Política de firmas | Harness **Deep**<br>Modelo Gemini Pro - T=0.1<br>System prompt `AGENTS.md`<br>Skills: `contract-review`, `nda-quick-check`, `obligation-extractor`<br>KB `kb-contract-reviewer`<br>Guardrails: prompt_injection, off_topic<br>Memoria sin PII | `read_contract` (Google Drive)<br>`compare_clauses` (Modelo)<br>`search_playbook` (Knowledge Base)<br>`draft_redlines` (Modelo) | Informe de cláusulas, severidad, citas y texto alternativo sugerido.<br>Worklog y auditoría en VirtuAI<br>Sin efectos en sistemas (solo lectura) |

## 5. Capas de identidad

1. **Gemini Enterprise** — licencia + rol IAM sobre la app del área.
2. **A2A OAuth** — el usuario consiente `a2a:invoke` en VirtuAI (Authorization Code + PKCE).
3. **Conectores** — OAuth individual por MCP; IAM de servicio para Cloud Run con autorización de negocio en backend.
4. **Datos/acciones** — ACL de origen, RBAC, filas y aprobación humana.
