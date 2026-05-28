# modules/code_patcher.py
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import logging
from typing import Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CodePatcher:
    """Generador automático de parches usando CodeT5"""
    
    def __init__(self):
        logger.info("🔄 Cargando CodeT5 para generación de parches...")
        self.model_name = "Salesforce/codet5-base"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        logger.info(f"✅ CodeT5 cargado en {self.device}")
    
    def generate_patch(self, vulnerable_code: str, vulnerability_type: str) -> Dict:
        """Genera un parche de seguridad para código vulnerable"""
        
        # Crear prompt específico para el modelo
        prompt = self._create_prompt(vulnerable_code, vulnerability_type)
        
        # Tokenizar y generar
        inputs = self.tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = self.model.generate(
                inputs["input_ids"],
                max_length=512,
                num_beams=5,
                temperature=0.7,
                do_sample=True
            )
        
        patched_code = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extraer solo la parte del código (post-procesamiento)
        patched_code = self._extract_code(patched_code)
        
        return {
            "original_code": vulnerable_code,
            "patched_code": patched_code,
            "vulnerability": vulnerability_type,
            "confidence": 0.85  # Por ahora fijo, luego mejorar
        }
    
    def _create_prompt(self, code: str, vuln_type: str) -> str:
        """Crea prompt para CodeT5"""
        prompts = {
            "sql_injection": f"Fix SQL injection vulnerability in this code:\n{code}\n\nSecure version:",
            "xss": f"Fix XSS vulnerability in this JavaScript code:\n{code}\n\nSecure version:",
            "command_injection": f"Fix command injection vulnerability:\n{code}\n\nSecure version:"
        }
        return prompts.get(vuln_type, f"Fix security issue in this code:\n{code}\n\nSecure version:")
    
    def _extract_code(self, generated: str) -> str:
        """Extrae código limpio de la generación"""
        # Simple extraction - puede mejorarse
        lines = generated.split('\n')
        code_lines = []
        in_code = False
        
        for line in lines:
            if 'def ' in line or 'function ' in line or 'class ' in line:
                in_code = True
            if in_code:
                code_lines.append(line)
        
        return '\n'.join(code_lines) if code_lines else generated
