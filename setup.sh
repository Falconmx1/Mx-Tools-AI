#!/bin/bash
echo "🔧 Configurando Mx-Tools AI..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Entorno listo. Ejecuta: source venv/bin/activate && uvicorn main:app --reload"
