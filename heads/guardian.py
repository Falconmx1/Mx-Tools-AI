class Guardian:
    def generate_firewall_rules(self, attack_log):
        rules = []
        if "port_scan" in attack_log:
            rules.append("iptables -A INPUT -p tcp --dport 1:1024 -m recent --update --seconds 60 -j DROP")
        return rules
    
    def propose_patches(self, vulnerabilities):
        patches = []
        for vuln in vulnerabilities:
            if "eval" in vuln["desc"]:
                patches.append("Reemplazar eval() por alternativas seguras como ast.literal_eval()")
        return patches
    
    def incident_response_plan(self, threat_type):
        plans = {
            "ransomware": "Aislar equipo, desconectar red, restaurar backups offline",
            "ddos": "Activar cloudflare, limitar tasa, filtrar tráfico malicioso"
        }
        return plans.get(threat_type, "Revisar logs y aplicar parches de seguridad")
