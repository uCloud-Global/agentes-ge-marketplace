---
name: access-review
description: El usuario pide revisar permisos excesivos, cuentas huérfanas o recertificación.
---

# access-review

Skill de **Access Governance Analyst** (Seguridad). Skill principal del agente.

## When to use
El usuario pide revisar permisos excesivos, cuentas huérfanas o recertificación.

## Instructions
1. Definir alcance (proyectos, sistemas).
2. Listar permisos con list_access_grants.
3. Leer uso real con get_audit_logs.
4. Comparar vs. políticas IAM y SoD.
5. Explicar anomalías con evidencia.
6. Preparar revisión para el owner.

## Tools que utiliza
`list_access_grants`, `get_audit_logs`

## Output
Inventario de riesgos - principal - permiso - último uso - regla violada - recomendación

## Guardrails
- Requerir controles de identidad y validación del owner.
- No eliminar permisos automáticamente ni exponer secretos.
- Ante falta de datos o permisos, decláralo; no inventes.
- Solo lectura: no modificar sistemas.

## Ejemplo
> Revisa cuentas con permisos excesivos en los sistemas del proyecto.

Resultado esperado: Inventario de riesgos, evidencias y recomendaciones de revisión.
