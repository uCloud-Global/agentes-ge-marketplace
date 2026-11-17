---
name: governed-sql
description: El usuario hace una pregunta de negocio que requiere datos tabulares.
---

# governed-sql

Skill de **Enterprise Data Analyst** (Datos). Skill principal del agente.

## When to use
El usuario hace una pregunta de negocio que requiere datos tabulares.

## Instructions
1. Traducir la pregunta a métricas oficiales con explain_metrics.
2. Descubrir tablas con discover_schema.
3. Escribir SQL solo SELECT con LIMIT.
4. Validar con validate_sql (bytes, tipo de sentencia).
5. Ejecutar con run_readonly_query.
6. Explicar resultados con SQL, fuente, filtros y supuestos.

## Tools que utiliza
`discover_schema`, `validate_sql`, `run_readonly_query`, `explain_metrics`

## Output
Respuesta - tabla - SQL usado - fuente - supuestos - costo estimado

## Guardrails
- Cuenta de solo lectura y datasets permitidos.
- Validar esquema, límites de filas, costos y semántica; no usar DML.
- Ante falta de datos o permisos, decláralo; no inventes.
- Solo lectura: no modificar sistemas.

## Ejemplo
> ¿Cómo varió el revenue por región en los últimos seis meses?

Resultado esperado: Tabla y narrativa con SQL documentado, fuente y supuestos.
