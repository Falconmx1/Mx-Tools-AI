import random

class Attacker:
    def __init__(self, scope_file="./data/authorized_targets.txt"):
        self.scope = self._load_scope(scope_file)
    
    def _load_scope(self, file):
        # Carga dominios/IPs autorizados
        return ["example.com"]  # demo
    
    def simulate_phishing(self, target_domain):
        if target_domain not in self.scope:
            return {"error": "Dominio no autorizado"}
        templates = [
            "Urgent: Your password expires today. Click here: http://fake-login.com",
            "Invoice #{} attached (malicious macro)".format(random.randint(1000,9999))
        ]
        return {"payload": random.choice(templates), "type": "phishing"}
    
    def sql_injection_sim(self, url):
        payloads = ["' OR '1'='1", "'; DROP TABLE users; --"]
        return {"payloads": payloads, "mitigation": "Use parametrized queries"}
