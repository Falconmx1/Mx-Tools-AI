# main.py (versión completa)
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from banner import show_banner
from heads.watcher import Watcher
from heads.attacker import Attacker
from heads.guardian import Guardian
from modules.code_patcher import CodePatcher
from modules.multi_lang import MultiLanguageAnalyzer
from core.redis_cache import ModelCache
import logging

load_dotenv()
show_banner()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Mx-Tools AI", version="3.0.0")

# Inicializar componentes
watcher = Watcher()
attacker = Attacker()
guardian = Guardian()
patcher = CodePatcher()
multi_lang = MultiLanguageAnalyzer()
cache = ModelCache(os.getenv("REDIS_URL", "redis://localhost:6379"))

# Modelos de datos
class CodeAnalysisRequest(BaseModel):
    code: str
    language: str = "python"
    use_cache: bool = True

class PatchRequest(BaseModel):
    code: str
    vulnerability_type: str
    language: str = "python"

@app.post("/analyze/code")
async def analyze_code(request: CodeAnalysisRequest):
    # Verificar cache
    cache_key = f"analysis_{request.language}_{hash(request.code)}"
    if request.use_cache:
        cached = cache.get_cached_output("code_analysis", cache_key)
        if cached:
            return cached
    
    # Análisis multi-lenguaje
    lang_analysis = multi_lang.analyze(request.code, request.language)
    
    # Análisis profundo
    deep_analysis = await watcher.analyze_code_full(request.code, request.language)
    
    result = {
        "language_analysis": lang_analysis,
        "deep_analysis": deep_analysis,
        "overall_risk": max(lang_analysis.get("risk_score", 0), deep_analysis["overall_risk"])
    }
    
    # Cachear resultado
    if request.use_cache:
        cache.cache_model_output("code_analysis", cache_key, result)
    
    return result

@app.post("/generate/patch")
async def generate_patch(request: PatchRequest):
    """Genera parche automático para código vulnerable"""
    result = patcher.generate_patch(request.code, request.vulnerability_type)
    return result

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "3.0.0",
        "components": {
            "watcher": "active",
            "attacker": "active", 
            "guardian": "active",
            "patcher": "active",
            "multi_lang": "active",
            "cache": cache.enabled
        },
        "supported_languages": ["python", "java", "go", "rust", "javascript"]
    }
