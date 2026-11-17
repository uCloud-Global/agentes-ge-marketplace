# Calificación de agentes: complejidad e impacto

Ambas dimensiones usan una escala de **1 a 5**. La calificación considera el contexto de implementación en VirtuAI (integraciones a construir, escrituras, sensibilidad de datos) y el valor de negocio esperado.

## Complejidad

Factores evaluados:

- Integraciones por construir (Custom Tools, Workstation) vs. MCP predefinidos
- Escrituras en sistemas y flujos de aprobación
- Sensibilidad y regulación de los datos (PII, financieros, legales, seguridad)
- Lógica determinística o cálculo requerido (scoring, matching, proyecciones)
- Número de fuentes y pasos del workflow (Classic vs. Deep)

| Score | Nivel | Criterio |
|---|---|---|
| 1 | Muy baja | Agente Classic, 1-2 fuentes en solo lectura (KB o MCP predefinido), sin backend propio ni datos sensibles. |
| 2 | Baja | Solo lectura sobre 2-3 MCP predefinidos o SQL acotado; sin Custom Tools por construir; flujo corto. |
| 3 | Media | Deep multi-paso con 3-4 conectores, o 1 Custom Tool / Workstation, o escrituras simples con aprobación (HITL). |
| 4 | Alta | Varias Custom Tools a construir o escrituras en sistemas transaccionales, datos sensibles, lógica determinística o correlación en tiempo real. |
| 5 | Muy alta | Varios backends a construir + Workstation/extracción documental + datos altamente sensibles o regulados + controles de fraude o sesgo. |

## Impacto

Factores evaluados:

- Volumen y frecuencia de uso
- Alcance (número de usuarios o áreas)
- Efecto directo en ingresos, costos o riesgo
- Tiempo ahorrado por ejecución

| Score | Nivel | Criterio |
|---|---|---|
| 1 | Muy bajo | Uso esporádico, pocos usuarios y ahorro marginal. |
| 2 | Bajo | Mejora de conveniencia para un equipo pequeño; sin efecto medible en ingresos, costos o riesgo. |
| 3 | Medio | Ahorro de tiempo relevante en un proceso de un área, frecuencia semanal/mensual o valor indirecto. |
| 4 | Alto | Proceso frecuente o decisiones de alto valor; efecto medible en ingresos, costos o riesgo de un área. |
| 5 | Muy alto | Alto volumen y amplio alcance (muchos usuarios o transacciones) con efecto directo en ingresos, costos o riesgo crítico. |

## Matriz de priorización

Prioridad sugerida = impacto alto con complejidad baja primero (quick wins), luego apuestas estratégicas.

| Agente | Área | Complejidad | Impacto | Cuadrante |
|---|---|---|---|---|
| [Enterprise Data Analyst](agentes/sql-analyst/README.md) | Datos | 3 | 5 | Quick win |
| [IT Helpdesk Concierge](agentes/it-helpdesk/README.md) | Tecnología | 3 | 5 | Quick win |
| [Sales CRM Copilot](agentes/sales-copilot/README.md) | Ventas | 3 | 5 | Quick win |
| [Customer Support Resolver](agentes/support-resolver/README.md) | Clientes | 4 | 5 | Apuesta estratégica |
| [Accounts Payable Reviewer](agentes/invoice-review/README.md) | Finanzas | 5 | 5 | Apuesta estratégica |
| [People Policy Advisor](agentes/people-policy/README.md) | Talento | 1 | 4 | Quick win |
| [Executive Intelligence](agentes/executive-brief/README.md) | Dirección | 2 | 4 | Quick win |
| [Compliance Control Monitor](agentes/compliance-monitor/README.md) | Legal | 3 | 4 | Quick win |
| [Contract Review Assistant](agentes/contract-reviewer/README.md) | Legal | 3 | 4 | Quick win |
| [Customer Success Health](agentes/customer-health/README.md) | Clientes | 3 | 4 | Quick win |
| [Lead Qualification Agent](agentes/lead-qualification/README.md) | Ventas | 3 | 4 | Quick win |
| [Access Governance Analyst](agentes/access-auditor/README.md) | Seguridad | 4 | 4 | Apuesta estratégica |
| [Cashflow Forecast Analyst](agentes/cashflow-analyst/README.md) | Finanzas | 4 | 4 | Apuesta estratégica |
| [Commercial Proposal Studio](agentes/proposal-builder/README.md) | Ventas | 4 | 4 | Apuesta estratégica |
| [Incident Response Coordinator](agentes/incident-command/README.md) | Tecnología | 4 | 4 | Apuesta estratégica |
| [Expense Policy Auditor](agentes/expense-auditor/README.md) | Finanzas | 2 | 3 | Mejora incremental |
| [Marketing Performance Analyst](agentes/marketing-analytics/README.md) | Marketing | 2 | 3 | Mejora incremental |
| [Data Quality Sentinel](agentes/data-quality/README.md) | Datos | 3 | 3 | Mejora incremental |
| [Process Improvement Scout](agentes/process-optimizer/README.md) | Operaciones | 3 | 3 | Mejora incremental |
| [Project PMO Copilot](agentes/pmo-copilot/README.md) | Operaciones | 3 | 3 | Mejora incremental |
| [Strategic Opportunity Radar](agentes/strategy-radar/README.md) | Dirección | 3 | 3 | Mejora incremental |
| [Supplier Risk Analyst](agentes/supplier-risk/README.md) | Compras | 3 | 3 | Mejora incremental |
| [Campaign Launch Copilot](agentes/campaign-copilot/README.md) | Marketing | 4 | 3 | Evaluar caso de negocio |
| [Employee Onboarding Navigator](agentes/onboarding-agent/README.md) | Talento | 4 | 3 | Evaluar caso de negocio |
| [Purchase Request Assistant](agentes/procurement-assistant/README.md) | Compras | 4 | 3 | Evaluar caso de negocio |
| [Talent Selection Evidence Analyst](agentes/talent-selection/README.md) | Talento | 5 | 3 | Evaluar caso de negocio |

## Justificación por agente

| Agente | Complejidad | Justificación | Impacto | Justificación |
|---|---|---|---|---|
| Executive Intelligence | 2 | Solo lectura sobre 3 MCP predefinidos (BigQuery, Drive, Gmail); sin backend propio. La dificultad está en la trazabilidad de cifras, no en la integración. | 4 | Pocos usuarios (comité directivo) pero decisiones de alto valor y ahorro semanal de consolidación de reportes. |
| Strategic Opportunity Radar | 3 | Deep con razonamiento alto, web search/fetch y validación de fuentes externas no confiables; sin escrituras ni backend. | 3 | Uso trimestral en planeación; valor estratégico alto pero indirecto y difícil de medir. |
| Sales CRM Copilot | 3 | Tres MCP predefinidos sin backend propio, pero con escrituras en CRM y borradores de correo bajo aprobación. | 5 | Uso diario por toda la fuerza comercial; efecto directo en pipeline y cobertura de seguimientos. |
| Lead Qualification Agent | 3 | Requiere Custom Tool de scoring determinístico y versionado, controles anti-sesgo y creación de tareas con aprobación. | 4 | Reduce el tiempo a primer contacto y mejora la conversión de leads; efecto en ingresos del área comercial. |
| Commercial Proposal Studio | 4 | Generación de documentos vía Docs API (Custom Tool), gobierno de tarifas y descuentos y plantillas; contenido largo. | 4 | Ahorra horas de preventa por propuesta y reduce errores de precio; frecuencia media. |
| Campaign Launch Copilot | 4 | Dos Custom Tools (métricas y programación en plataforma), cumplimiento de consentimiento/opt-out y revisión de claims. | 3 | Acelera la preparación de campañas de un equipo acotado; efecto indirecto en respuesta y conversión. |
| Marketing Performance Analyst | 2 | Classic de solo lectura con HubSpot y SQL acotado en BigQuery; sin backend. | 3 | Reduce tiempo de reporting de marketing; valor analítico para un equipo. |
| Customer Support Resolver | 4 | Cara al cliente: verificación de identidad, PII, escrituras en tickets, políticas de reembolso y escalamiento. | 5 | Alto volumen de casos; efecto directo en tiempo de atención, resolución en primer contacto y costo de soporte. |
| Customer Success Health | 3 | Workstation (Enterprise) para la fórmula de health score más dos MCP de lectura; sin escrituras. | 4 | Anticipa churn en la cartera; efecto directo en retención e ingresos recurrentes. |
| Employee Onboarding Navigator | 4 | Coordina varias áreas: solicitud de accesos vía ITSM (Custom Tool), eventos de calendario y datos de RR. HH., todo con aprobación. | 3 | Mejora la experiencia de ingreso; volumen ligado a contrataciones, ahorro moderado por caso. |
| People Policy Advisor | 1 | Classic con KB y verificación de versión en Drive; solo lectura y sin backend. | 4 | Alcance a todos los colaboradores y alto volumen de preguntas repetidas; bajo riesgo y adopción rápida. |
| Accounts Payable Reviewer | 5 | Extracción documental (Document AI) + 3-way match con ERP + validación de proveedor: tres Custom Tools, datos bancarios y control de fraude. | 5 | Alto volumen de facturas, ahorro por factura y prevención de pagos erróneos o fraudulentos; ROI directo. |
| Cashflow Forecast Analyst | 4 | Modelado de escenarios en Workstation con conciliación de saldos, aislamiento por entidad y exigencia alta de exactitud. | 4 | Decisiones de liquidez de alto valor para Finanzas; frecuencia semanal y pocos usuarios. |
| Expense Policy Auditor | 2 | Classic de solo lectura con BigQuery y política en KB; complejidad en reglas de moneda, país y excepciones. | 3 | Reduce tiempo de auditoría de gastos; impacto acotado al área. |
| Supplier Risk Analyst | 3 | Una Custom Tool de scoring versionado más lectura de KPIs y contratos; sin escrituras. | 3 | Mejora la homologación y gestión de proveedores; frecuencia periódica. |
| Purchase Request Assistant | 4 | Tres Custom Tools sobre ERP (catálogo, presupuesto, envío a aprobación) con segregación de funciones. | 3 | Reduce rechazos por requisiciones incompletas y tiempo de solicitud; efecto operativo moderado. |
| Contract Review Assistant | 3 | Solo lectura (Drive + KB) sin backend, pero exige razonamiento jurídico preciso, citas y playbook de cláusulas. | 4 | Ahorra tiempo de primera revisión legal y reduce riesgo contractual en acuerdos de alto valor. |
| Compliance Control Monitor | 3 | Una Custom Tool (matriz de controles) más búsqueda de evidencias y alertas en borrador. | 4 | Reduce riesgo regulatorio y esfuerzo de auditoría; alto valor en industrias reguladas. |
| IT Helpdesk Concierge | 3 | Dos Custom Tools (CMDB e ITSM) con creación de tickets bajo aprobación; runbooks en KB. | 5 | Alcance a todos los colaboradores y alto volumen de consultas repetidas; deflexión directa de tickets. |
| Incident Response Coordinator | 4 | Correlación en tiempo real de logs, métricas y despliegues; enmascaramiento de PII; sin acciones sobre infraestructura. | 4 | Reduce MTTR en incidentes con impacto en ingresos; uso por equipos técnicos de guardia. |
| Enterprise Data Analyst | 3 | BigQuery gobernado con dry-run, topes de costo y catálogo de métricas; la exactitud semántica es el reto principal. | 5 | Analítica de autoservicio para muchas áreas; reduce la dependencia del equipo de datos. |
| Data Quality Sentinel | 3 | Reglas de calidad como SQL de lectura más correlación con logs de pipelines; sin remediación automática. | 3 | Detecta problemas antes del consumo; valor transversal pero indirecto. |
| Project PMO Copilot | 3 | Una Custom Tool (hoja maestra de hitos) más Drive, Calendar y borradores; flujo de redacción. | 3 | Ahorra horas semanales de reporting a PMO y líderes de proyecto. |
| Process Improvement Scout | 3 | Workstation para análisis de tiempos de ciclo más SOP en KB; solo lectura. | 3 | Identifica oportunidades de automatización; valor indirecto y de mediano plazo. |
| Talent Selection Evidence Analyst | 5 | Tres Custom Tools (ATS, extracción de CV, rúbrica) + Workstation para el radar, PII de candidatos, controles de sesgo y workspace aislado. | 3 | Reduce el tiempo de pre-revisión de CVs; el impacto se limita por diseño: la decisión siempre es humana. |
| Access Governance Analyst | 4 | Inventario de accesos vía Cloud Asset Inventory (Custom Tool), audit logs y matriz SoD sobre datos de seguridad. | 4 | Reduce riesgo de accesos excesivos y el tiempo de recertificación; alto valor para seguridad y auditoría. |
