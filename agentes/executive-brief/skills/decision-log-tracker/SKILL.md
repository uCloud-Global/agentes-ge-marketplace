---
name: decision-log-tracker
description: El usuario pide el estado de decisiones o compromisos de comité.
---

# decision-log-tracker

Skill de **Executive Intelligence** (Dirección).

## When to use
El usuario pide el estado de decisiones o compromisos de comité.

## Instructions
1. Buscar actas recientes y extraer decisiones con responsable y fecha.
2. Buscar en correo evidencia de avance de cada compromiso.
3. Clasificar estado: cumplido, en curso, vencido, sin evidencia.
4. Listar decisiones pendientes para el próximo comité.

## Output
Tabla decisión - responsable - fecha - estado - evidencia

## Guardrails
- No revelar indicadores fuera del rol del solicitante.
- Cuando no haya datos actualizados debe indicarlo; validar que ninguna cifra se invente.
- Ante falta de datos o permisos, decláralo; no inventes.
- Solo lectura: no modificar sistemas.
