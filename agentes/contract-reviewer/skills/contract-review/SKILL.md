---
name: contract-review
description: El usuario pide revisar un contrato, NDA o adenda frente al estándar.
---

# contract-review

Skill de **Contract Review Assistant** (Legal). Skill principal del agente.

## When to use
El usuario pide revisar un contrato, NDA o adenda frente al estándar.

## Instructions
1. Leer contrato con read_contract.
2. Extraer cláusulas clave (objeto, plazo, responsabilidad, indemnidad, confidencialidad, ley aplicable, terminación).
3. Comparar con playbook usando search_playbook y compare_clauses.
4. Asignar severidad (alta/media/baja) por desviación.
5. Proponer redlines con draft_redlines.

## Tools que utiliza
`read_contract`, `compare_clauses`, `search_playbook`, `draft_redlines`

## Output
Tabla cláusula - texto actual (cita) - estándar - desviación - severidad - redline sugerido

## Guardrails
- No firmar ni compartir contratos sin validación legal.
- No sustituir revisión de abogado y evitar conclusiones jurídicas definitivas.
- Ante falta de datos o permisos, decláralo; no inventes.
- Solo lectura: no modificar sistemas.

## Ejemplo
> Revisa este NDA e identifica desviaciones frente a nuestro estándar.

Resultado esperado: Informe de cláusulas, severidad, citas y texto alternativo sugerido.
