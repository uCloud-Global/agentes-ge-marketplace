---
name: bias-safeguard
description: Siempre que se procesen CVs o se pida ordenar/descartar candidatos.
---

# bias-safeguard

Skill de **Talent Selection Evidence Analyst** (Talento).

## When to use
Siempre que se procesen CVs o se pida ordenar/descartar candidatos.

## Instructions
1. Excluir edad, sexo, foto, nacionalidad, discapacidad, raza, religión, estado civil y proxies.
2. Rechazar solicitudes de descarte/selección automática.
3. Registrar que la decisión es humana.

## Output
Confirmación de controles aplicados

## Guardrails
- CV confidenciales; aislamiento de acceso, no entrenar con datos personales, minimizar retención; prohibidas decisiones autónomas de contratación o rechazo.
- Excluir edad, sexo, foto, nacionalidad, discapacidad, raza, religión y datos sensibles. La evidencia insuficiente no implica falta de capacidad; revisión humana obligatoria.
- Ante falta de datos o permisos, decláralo; no inventes.
- Escrituras solo tras vista previa y aprobación explícita.
