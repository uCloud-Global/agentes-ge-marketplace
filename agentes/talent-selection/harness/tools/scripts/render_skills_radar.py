#!/usr/bin/env python3
"""Gráfico polar de evidencias de competencias para revisión humana.

Uso: python talento_radar_demo.py --output radar_talento.png
Dependencias: pip install matplotlib numpy
Datos 100% ficticios; no utiliza atributos protegidos, no toma decisiones laborales.

En producción, reemplace DEMO_DATA con una rúbrica validada por RR. HH.,
compartida para todas las personas candidatas al mismo rol. Las puntuaciones
representan EVIDENCIA documentada para cada habilidad, no una conclusión
sobre la capacidad de la persona.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

DEMO_DATA = {
    'role': 'Analista de Datos - Demo ficticia',
    'scale': 5,
    'competencies': [
        {'name': 'SQL', 'weight': 0.24, 'target': 4.5},
        {'name': 'Python', 'weight': 0.21, 'target': 4.0},
        {'name': 'Estadística', 'weight': 0.16, 'target': 4.0},
        {'name': 'Modelado', 'weight': 0.16, 'target': 3.5},
        {'name': 'Comunicación', 'weight': 0.13, 'target': 4.0},
        {'name': 'Gobierno de datos', 'weight': 0.10, 'target': 3.5},
    ],
    'candidates': [
        {'alias':'Perfil A', 'scores':[4.8,4.4,3.9,4.0,3.6,3.8]},
        {'alias':'Perfil B', 'scores':[4.0,3.8,4.4,3.8,4.5,4.1]},
        {'alias':'Perfil C', 'scores':[3.5,4.6,3.3,3.6,4.0,3.4]},
    ]
}


def validate(data):
    comp = data['competencies']
    n = len(comp)
    assert 3 <= n <= 12, 'Se requieren entre 3 y 12 habilidades'
    assert abs(sum(float(c['weight']) for c in comp) - 1.0) < 1e-6, 'Los pesos deben sumar 1'
    scale = float(data.get('scale', 5))
    for c in comp:
        assert 0 <= float(c['target']) <= scale
    for person in data['candidates']:
        assert len(person['scores']) == n
        assert all(v is None or 0 <= float(v) <= scale for v in person['scores'])
    return scale


def build_chart(data, output_path):
    scale = validate(data)
    competencies = data['competencies']
    n = len(competencies)
    theta = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    wrap = lambda values: values + values[:1]
    fig, ax = plt.subplots(figsize=(10, 8.2), subplot_kw={'polar':True}, dpi=175)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#f8faff')
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.degrees(theta), [f"{c['name']}\n{round(c['weight']*100)}%" for c in competencies], fontsize=10.5)
    ax.set_ylim(0, scale)
    ax.set_yticks([1,2,3,4,5])
    ax.set_yticklabels(['1','2','3','4','5'], color='#76819a', fontsize=9)
    ax.grid(color='#dbe4f3', linewidth=0.9)
    ax.spines['polar'].set_color('#b6c8e8')
    targets = [float(c['target']) for c in competencies]
    ax.plot(wrap(theta), wrap(targets), '--', color='#344767', linewidth=2, label='Objetivo del rol')
    colors = ['#1a73e8','#34a853','#ea4335','#fbbc04']
    for i, person in enumerate(data['candidates']):
        scores = [float(v) if v is not None else np.nan for v in person['scores']]
        color = colors[i % len(colors)]
        ax.plot(wrap(theta), wrap(scores), marker='o', markersize=5, lw=2, color=color, label=person['alias'])
        ax.fill(wrap(theta), wrap(scores), alpha=0.07, color=color)
    fig.suptitle('Matriz comparativa de competencias', fontsize=19, fontweight='bold', y=.97, color='#192a47')
    fig.text(.5, .925, data['role'], ha='center', color='#52617c', fontsize=11)
    fig.legend(loc='lower center', ncol=min(4, len(data['candidates'])+1), bbox_to_anchor=(.5,.035), frameon=False)
    fig.text(.5, .005, 'Datos simulados - Evidencias revisables - No determina contratación', ha='center', color='#71819a', fontsize=9)
    fig.subplots_adjust(top=.84,bottom=.15,left=.12,right=.88)
    out = Path(output_path)
    out.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(out,bbox_inches='tight',facecolor='white')
    plt.close(fig)
    return out

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--input', help='Archivo JSON con el esquema de rol/competencias/personas candidatas')
    parser.add_argument('--output',default='radar_talento.png')
    args=parser.parse_args()
    data=json.loads(Path(args.input).read_text(encoding='utf-8')) if args.input else DEMO_DATA
    result=build_chart(data,args.output)
    print(result)
