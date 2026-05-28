import os
from fastapi import FastAPI
from dotenv import load_dotenv
from banner import show_banner
from core.config import settings
from web.endpoints import analysis, attack, defense

load_dotenv()

# Mostrar banner al iniciar
show_banner()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Guardián de 3 cabezas para ciberseguridad ética ofensiva/defensiva"
)

# Incluir routers de cada cabeza
app.include_router(analysis.router, prefix="/api/v1/analysis", tags=["Watcher"])
app.include_router(attack.router, prefix="/api/v1/attack", tags=["Attacker"])
app.include_router(defense.router, prefix="/api/v1/defense", tags=["Guardian"])

@app.get("/")
def root():
    return {
        "message": "Mx-Tools AI - El guardián de tres cabezas está vigilando",
        "heads": ["Watcher (Análisis)", "Attacker (Simulación)", "Guardian (Defensa)"],
        "ethics": "Solo usar en entornos autorizados"
    }
