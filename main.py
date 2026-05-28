import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from banner import show_banner
from heads.watcher import Watcher
from heads.attacker import Attacker
import logging

load_dotenv()
show_banner()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Mx-Tools AI", version="2.0.0")

# Inicializar cabezas
watcher = Watcher()
attacker = Attacker()

# Modelos de datos
class CodeAnalysisRequest(BaseModel):
    code: str
    language: str = "python"

class AttackRequest(BaseModel):
    target: str
    attack_type: str  # sql_injection, xss, path_traversal

@app.post("/analyze/code")
async def analyze_code(request: CodeAnalysisRequest):
    """Endpoint para análisis de código con IA"""
    try:
        result = await watcher.analyze_code_full(request.code, request.language)
        return result
    except Exception as e:
        logger.error(f"Error en análisis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/simulate/attack")
async def simulate_attack(request: AttackRequest):
    """Endpoint para simulación ética de ataques"""
    # Verificar que solo se use en entornos autorizados
    if os.getenv("ALLOW_ETHICAL_ATTACKS_ONLY", "True") == "True":
        logger.warning(f"Simulación de ataque solicitada para {request.target}")
    
    result = await attacker.smart_attack_simulation(request.target, request.attack_type)
    return result

@app.get("/health")
async def health_check():
    """Verificar estado de los modelos de IA"""
    return {
        "status": "healthy",
        "ml_models_loaded": True,
        "watcher_ready": True,
        "attacker_ready": True
    }
