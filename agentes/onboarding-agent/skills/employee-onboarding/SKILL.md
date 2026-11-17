---
name: employee-onboarding
description: El usuario pide preparar la incorporación de una persona nueva.
---

# employee-onboarding

Skill de **Employee Onboarding Navigator** (Talento). Skill principal del agente.

## When to use
El usuario pide preparar la incorporación de una persona nueva.

## Instructions
1. Confirmar área, rol, fecha de ingreso y manager.
2. Generar checklist por área con get_onboarding_plan.
3. Proponer agenda de bienvenida y pedir aprobación antes de schedule_welcome.
4. Preparar borrador de bienvenida con draft_welcome_mail.
5. Preparar solicitudes de acceso mínimas por rol y pedir aprobación antes de request_access.

## Tools que utiliza
`get_onboarding_plan`, `schedule_welcome`, `draft_welcome_mail`, `request_access`

## Output
Checklist por área - eventos propuestos - borradores - solicitudes de acceso pendientes

## Guardrails
- No comunicar información contractual fuera de RR. HH.
- Datos personales mínimos; no conceder accesos sin visto bueno de TI.
- Ante falta de datos o permisos, decláralo; no inventes.
- Escrituras solo tras vista previa y aprobación explícita.

## Ejemplo
> Prepara el onboarding de una persona que ingresa el próximo lunes al equipo de datos.

Resultado esperado: Checklist por áreas, eventos propuestos, borradores y tareas de acceso.
