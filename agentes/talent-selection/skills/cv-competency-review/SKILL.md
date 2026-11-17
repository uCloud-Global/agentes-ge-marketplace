---
name: cv-competency-review
description: RR. HH. pide comparar CVs autorizados contra la rúbrica de una vacante.
---

# cv-competency-review

Skill de **Talent Selection Evidence Analyst** (Talento). Skill principal del agente.

## When to use
RR. HH. pide comparar CVs autorizados contra la rúbrica de una vacante.

## Instructions
1. Leer requisitos con get_job_profile y rúbrica con standardize_role_rubric.
2. Extraer evidencias con extract_cv_evidence (sin atributos protegidos).
3. Estandarizar habilidades y anotar NO OBSERVADO cuando falte evidencia.
4. Construir matriz con build_evidence_matrix.
5. Generar radar con render_skills_radar.
6. Proponer preguntas de entrevista y remitir a RR. HH.

## Tools que utiliza
`get_job_profile`, `extract_cv_evidence`, `standardize_role_rubric`, `build_evidence_matrix`, `render_skills_radar`

## Output
Matriz explicable por competencia (evidencia citada) - radar PNG - preguntas de entrevista - disclaimer de revisión humana

## Guardrails
- CV confidenciales; aislamiento de acceso, no entrenar con datos personales, minimizar retención; prohibidas decisiones autónomas de contratación o rechazo.
- Excluir edad, sexo, foto, nacionalidad, discapacidad, raza, religión y datos sensibles. La evidencia insuficiente no implica falta de capacidad; revisión humana obligatoria.
- Ante falta de datos o permisos, decláralo; no inventes.
- Escrituras solo tras vista previa y aprobación explícita.

## Ejemplo
> Para la vacante Analista de Datos, compara tres CV ficticios con criterios predefinidos; muestra evidencias, vacíos y un gráfico radar para revisión de RR. HH.

Resultado esperado: Matriz explicable por competencia, radar Python y preguntas de entrevista; no realiza selección ni descarte automático.
