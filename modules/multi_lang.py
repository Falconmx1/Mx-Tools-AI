# modules/multi_lang.py
from typing import Dict, List
import re

class MultiLanguageAnalyzer:
    """Analizador de vulnerabilidades multi-lenguaje"""
    
    def __init__(self):
        self.language_patterns = {
            "python": {
                "dangerous_funcs": ["eval", "exec", "__import__", "compile", "os.system"],
                "sql_pattern": r'(?i)(cursor\.execute\(f?["\'].*\{.*\}.*["\'])',
                "command_injection": r'(?i)(os\.system|subprocess\.call|subprocess\.Popen)'
            },
            "java": {
                "dangerous_funcs": ["Runtime.exec", "ProcessBuilder", "Class.forName"],
                "sql_pattern": r'(?i)(Statement\.executeQuery|PreparedStatement.*\+=)',
                "command_injection": r'(?i)(Runtime\.exec|ProcessBuilder)'
            },
            "go": {
                "dangerous_funcs": ["syscall.Exec", "os.StartProcess", "exec.Command"],
                "sql_pattern": r'(?i)(db\.Query\(fmt\.Sprintf|db\.Exec\(fmt\.Sprintf)',
                "command_injection": r'(?i)(exec\.Command.*\+)'
            },
            "rust": {
                "dangerous_funcs": ["std::process::Command", "unsafe", "std::mem::transmute"],
                "sql_pattern": r'(?i)(sql_query\(format!)',
                "command_injection": r'(?i)(Command::new\(.*\.arg\(variable\))'
            }
        }
    
    def analyze(self, code: str, language: str) -> Dict:
        """Analiza código en lenguaje específico"""
        if language not in self.language_patterns:
            return {"error": f"Lenguaje {language} no soportado"}
        
        patterns = self.language_patterns[language]
        findings = []
        
        # Buscar funciones peligrosas
        for func in patterns["dangerous_funcs"]:
            if func in code:
                findings.append({
                    "type": "dangerous_function",
                    "function": func,
                    "risk": "HIGH"
                })
        
        # Buscar SQL injection
        if re.search(patterns["sql_pattern"], code):
            findings.append({
                "type": "sql_injection_risk",
                "risk": "CRITICAL"
            })
        
        # Buscar command injection
        if re.search(patterns["command_injection"], code):
            findings.append({
                "type": "command_injection_risk",
                "risk": "CRITICAL"
            })
        
        return {
            "language": language,
            "vulnerabilities_found": len(findings),
            "findings": findings,
            "risk_score": self._calculate_risk(findings)
        }
    
    def _calculate_risk(self, findings: List[Dict]) -> str:
        """Calcula riesgo total"""
        risks = [f["risk"] for f in findings]
        if "CRITICAL" in risks:
            return "CRITICAL"
        elif "HIGH" in risks:
            return "HIGH"
        elif "MEDIUM" in risks:
            return "MEDIUM"
        return "LOW"
