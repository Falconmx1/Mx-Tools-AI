import asyncio
from heads.watcher import Watcher
from heads.attacker import Attacker

async def test_watcher():
    watcher = Watcher()
    
    # Código vulnerable de prueba
    vulnerable_code = """
    def login(username, password):
        query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
        return execute_query(query)
    
    def process_input(data):
        eval(data)
    """
    
    result = await watcher.analyze_code_full(vulnerable_code, "python")
    print("=== ANÁLISIS DE CÓDIGO ===")
    print(f"Riesgo total: {result['overall_risk']}")
    print(f"Vulnerabilidades encontradas: {len(result['ml_analysis']['vulnerabilities'])}")
    print(f"Sugerencias: {result['recommended_actions']}")

async def test_attacker():
    attacker = Attacker()
    result = await attacker.smart_attack_simulation("test-site.com", "sql_injection")
    print("\n=== SIMULACIÓN DE ATAQUE ===")
    print(f"Payload: {result['payload']}")
    print(f"Mitigación: {result['mitigation']}")

if __name__ == "__main__":
    asyncio.run(test_watcher())
    asyncio.run(test_attacker())
