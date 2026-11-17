---
name: supplier-assessment
description: El usuario pide evaluar riesgo o desempeño de proveedores.
---

# supplier-assessment

Skill de **Supplier Risk Analyst** (Compras). Skill principal del agente.

## When to use
El usuario pide evaluar riesgo o desempeño de proveedores.

## Instructions
1. Consultar KPIs con get_supplier_kpis.
2. Verificar obligaciones con search_contract.
3. Calcular score con score_risk.
4. Explicar riesgo por dimensión.
5. Recomendar acción para aprobación.

## Tools que utiliza
`get_supplier_kpis`, `search_contract`, `score_risk`

## Output
Ranking - score por dimensión - evidencia - acción recomendada

## Guardrails
- Aprobar decisiones de bloqueo o suspensión.
- Evitar puntuaciones opacas y sesgos no justificados.
- Ante falta de datos o permisos, decláralo; no inventes.
- Solo lectura: no modificar sistemas.

## Ejemplo
> ¿Cuáles proveedores muestran incumplimientos recurrentes este trimestre?

Resultado esperado: Ranking de riesgo, evidencia y plan de revisión.
