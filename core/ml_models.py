# core/ml_models.py
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VulnerabilityDetector:
    """Detector de vulnerabilidades basado en CodeBERTa"""
    
    def __init__(self):
        logger.info("🔄 Cargando modelos de IA para detección de vulnerabilidades...")
        # Modelo especializado para análisis de código
        self.code_model = AutoModelForSequenceClassification.from_pretrained(
            "microsoft/codebert-base",  # Alternativa: "huggingface/CodeBERTa"
            num_labels=15  # 15 tipos comunes de vulnerabilidades
        )
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
        
        # Modelo para análisis de logs con BERT
        self.log_analyzer = pipeline(
            "text-classification",
            model="bert-base-uncased",
            return_all_scores=True
        )
        
        # Embeddings para código sospechoso
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Base de conocimiento de vulnerabilidades CWE
        self.cwe_patterns = self._load_cwe_patterns()
        logger.info("✅ Modelos de IA cargados exitosamente")
    
    def _load_cwe_patterns(self):
        """Carga patrones de vulnerabilidades CWE"""
        return {
            "CWE-89": {"pattern": r"(?i)(SELECT.*FROM.*WHERE.*=.*\'.*\'|\".*\")", "risk": "CRITICAL"},
            "CWE-79": {"pattern": r"(?i)(<script>|javascript:|onerror=)", "risk": "HIGH"},
            "CWE-22": {"pattern": r"(?i)(\.\./|\.\.\\)", "risk": "MEDIUM"},
            "CWE-78": {"pattern": r"(?i)(;|\||`|\$\(|system\(|exec\()", "risk": "CRITICAL"},
        }
    
    def analyze_code_deep(self, code: str) -> Dict:
        """Análisis profundo de código con transformers"""
        results = {
            "vulnerabilities": [],
            "risk_score": 0.0,
            "suggestions": []
        }
        
        # Tokenizar y obtener predicciones
        inputs = self.tokenizer(code, return_tensors="pt", truncation=True, max_length=512)
        
        with torch.no_grad():
            outputs = self.code_model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        
        # Detectar patrones CWE conocidos
        for cwe_id, cwe_info in self.cwe_patterns.items():
            import re
            if re.search(cwe_info["pattern"], code):
                results["vulnerabilities"].append({
                    "type": cwe_id,
                    "risk": cwe_info["risk"],
                    "description": f"Patrón sospechoso detectado: {cwe_id}"
                })
        
        # Calcular score de riesgo (0-1)
        if results["vulnerabilities"]:
            risk_scores = {"LOW": 0.2, "MEDIUM": 0.5, "HIGH": 0.8, "CRITICAL": 1.0}
            results["risk_score"] = max(risk_scores[v["risk"]] for v in results["vulnerabilities"])
        
        # Generar sugerencias basadas en ML
        results["suggestions"] = self._generate_suggestions(results["vulnerabilities"])
        
        return results
    
    def _generate_suggestions(self, vulnerabilities: List[Dict]) -> List[str]:
        """Genera sugerencias usando NLP"""
        suggestions = []
        for vuln in vulnerabilities:
            if "CWE-89" in vuln["type"]:
                suggestions.append("Usar consultas parametrizadas o Prepared Statements")
            elif "CWE-79" in vuln["type"]:
                suggestions.append("Sanitizar entradas con HTML escaping")
            elif "CWE-22" in vuln["type"]:
                suggestions.append("Validar rutas con path sanitization")
            elif "CWE-78" in vuln["type"]:
                suggestions.append("Evitar system() y comandos shell. Usar subprocess con listas")
        return suggestions
    
    def analyze_logs(self, log_text: str) -> Dict:
        """Análisis de logs con transformers"""
        results = self.log_analyzer(log_text[:512])  # Limitar longitud
        
        # Identificar patrones anómalos
        anomalies = []
        if "failed password" in log_text.lower():
            anomalies.append("Múltiples intentos fallidos de autenticación")
        if "error" in log_text.lower() and "sql" in log_text.lower():
            anomalies.append("Posible SQL injection detectado en logs")
        
        return {
            "classification": results[0] if results else [],
            "anomalies": anomalies,
            "risk_level": "HIGH" if anomalies else "LOW"
        }

# Instancia global
vuln_detector = VulnerabilityDetector()
