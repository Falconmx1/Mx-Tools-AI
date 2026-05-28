# heads/watcher.py
from core.ml_models import vuln_detector
import re
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class Watcher:
    """Cabeza de análisis con capacidades reales de ML"""
    
    def __init__(self):
        self.ml_engine = vuln_detector
        logger.info("Watcher inicializado con motor de ML")
    
    async def analyze_code_full(self, code: str, language: str = "python") -> Dict:
        """Análisis completo de código con IA"""
        # Análisis profundo con transformers
        ml_results = self.ml_engine.analyze_code_deep(code)
        
        # Análisis estático complementario
        static_analysis = self._static_analysis(code, language)
        
        return {
            "ml_analysis": ml_results,
            "static_analysis": static_analysis,
            "overall_risk": ml_results["risk_score"],
            "recommended_actions": ml_results["suggestions"]
        }
    
    def _static_analysis(self, code: str, language: str) -> Dict:
        """Análisis estático complementario"""
        findings = []
        
        # Reglas específicas por lenguaje
        if language == "python":
            dangerous_funcs = ["eval", "exec", "__import__", "compile"]
            for func in dangerous_funcs:
                if func in code:
                    findings.append(f"Función peligrosa: {func}")
        
        elif language == "javascript":
            if "document.write" in code:
                findings.append("Uso de document.write puede causar XSS")
        
        return {"findings": findings, "language": language}
    
    async def analyze_network(self, target: str) -> Dict:
        """Análisis de red con ML (placeholder para integración real)"""
        # Aquí puedes integrar nmap, shodan, etc.
        return {
            "target": target,
            "ml_prediction": "Análisis de red requeriría integración con nmap/shodan",
            "risk_assessment": "PENDIENTE"
        }
    
    async def analyze_log_stream(self, logs: List[str]) -> Dict:
        """Análisis de logs con transformers"""
        results = []
        for log_line in logs[:10]:  # Limitar a 10 líneas por rendimiento
            analysis = self.ml_engine.analyze_logs(log_line)
            results.append(analysis)
        
        return {
            "logs_analyzed": len(results),
            "anomalies_found": sum(1 for r in results if r["anomalies"]),
            "detailed_analysis": results
        }
