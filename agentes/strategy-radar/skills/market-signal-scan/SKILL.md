---
name: market-signal-scan
description: El usuario pide revisar tendencias, competidores o regulación externa.
---

# market-signal-scan

Skill de **Strategic Opportunity Radar** (Dirección).

## When to use
El usuario pide revisar tendencias, competidores o regulación externa.

## Instructions
1. Definir alcance (sector, país, horizonte).
2. Buscar y abrir fuentes externas con web fetch; priorizar fuentes primarias.
3. Registrar fecha y URL de cada señal.
4. Clasificar señal: oportunidad, amenaza, regulación, tecnología.

## Output
Lista de señales con fecha, fuente, tipo y relevancia

## Guardrails
- Fuentes externas deben validarse; no prometer resultados.
- Debe separar hechos, hipótesis y estimaciones; comprobar trazabilidad.
- Ante falta de datos o permisos, decláralo; no inventes.
- Solo lectura: no modificar sistemas.
