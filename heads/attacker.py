# heads/attacker.py
import random
import hashlib
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class Attacker:
    """Simulador ético de ataques con IA"""
    
    def __init__(self):
        self.payload_generator = self._init_payload_generator()
        logger.info("Attacker inicializado - Modo ético")
    
    def _init_payload_generator(self):
        """Inicializa generador de payloads basado en reglas"""
        return {
            "sql_injection": [
                "' OR '1'='1",
                "'; DROP TABLE users; --",
                "' UNION SELECT null, username, password FROM users--"
            ],
            "xss": [
                "<script>alert('XSS')</script>",
                "<img src=x onerror=alert(1)>",
                "javascript:alert('XSS')"
            ],
            "path_traversal": [
                "../../../etc/passwd",
                "..\\..\\..\\windows\\win.ini",
                "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd"
            ]
        }
    
    async def smart_attack_simulation(self, target: str, attack_type: str) -> Dict:
        """Simula ataques inteligentes con variaciones"""
        if attack_type not in self.payload_generator:
            return {"error": f"Tipo de ataque desconocido: {attack_type}"}
        
        # Seleccionar payload aleatorio
        payload = random.choice(self.payload_generator[attack_type])
        
        # Generar variación basada en IA (simplificado)
        variation = self._generate_variation(payload, attack_type)
        
        return {
            "target": target,
            "attack_type": attack_type,
            "payload": payload,
            "ai_variation": variation,
            "mitigation": self._get_mitigation(attack_type),
            "ethical_warning": "SOLO PARA PRUEBAS AUTORIZADAS"
        }
    
    def _generate_variation(self, original: str, attack_type: str) -> str:
        """Genera variaciones ofuscadas (demostración)"""
        if attack_type == "sql_injection":
            # Ofuscación simple de ejemplo
            return original.replace(" ", "/**/")
        elif attack_type == "xss":
            return original.replace("<", "&lt;").replace(">", "&gt;")
        return original
    
    def _get_mitigation(self, attack_type: str) -> str:
        """Recomendaciones de mitigación"""
        mitigations = {
            "sql_injection": "Usar consultas parametrizadas, ORM, validación de entrada",
            "xss": "Sanitizar salida con HTML escaping, CSP headers",
            "path_traversal": "Validar rutas con whitelist, usar path canonicalization"
        }
        return mitigations.get(attack_type, "Revisar OWASP Top 10 para más información")
