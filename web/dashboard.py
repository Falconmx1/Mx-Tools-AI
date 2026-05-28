# web/dashboard.py
import gradio as gr
import requests
import json
from typing import Dict
import sys
sys.path.append('..')

from heads.watcher import Watcher
from heads.attacker import Attacker
from modules.code_patcher import CodePatcher

# Inicializar componentes
watcher = Watcher()
attacker = Attacker()
patcher = CodePatcher()

def analyze_code_interface(code: str, language: str) -> Dict:
    """Interfaz para análisis de código"""
    result = watcher.analyze_code_full(code, language)
    return {
        "Risk Score": result['overall_risk'],
        "Vulnerabilities": len(result['ml_analysis']['vulnerabilities']),
        "Details": json.dumps(result['ml_analysis']['vulnerabilities'], indent=2),
        "Recommendations": "\n".join(result['recommended_actions'])
    }

def simulate_attack_interface(target: str, attack_type: str) -> str:
    """Interfaz para simulación de ataques"""
    result = attacker.smart_attack_simulation(target, attack_type)
    return json.dumps(result, indent=2)

def generate_patch_interface(code: str, vuln_type: str) -> str:
    """Interfaz para generación de parches"""
    result = patcher.generate_patch(code, vuln_type)
    return f"""## Original Code:
```python
{result['original_code']}
