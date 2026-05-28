from transformers import pipeline
import re

class Watcher:
    def __init__(self):
        self.nlp = pipeline("text-classification", model="bert-base-uncased")
    
    def analyze_code(self, code: str):
        # Simula detección de vulnerabilidades con NLP + reglas
        findings = []
        if "eval(" in code:
            findings.append({"risk": "HIGH", "desc": "Uso de eval() detectado"})
        if re.search(r"password\s*=\s*['\"][^'\"]+['\"]", code):
            findings.append({"risk": "MEDIUM", "desc": "Posible hardcoded password"})
        return findings
    
    def scan_network(self, target: str):
        # Placeholder: integración con nmap, shodan, etc.
        return {"open_ports": [22, 80, 443], "services": ["ssh", "http", "https"]}
