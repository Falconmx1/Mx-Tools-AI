# modules/cwe_finetuner.py
from transformers import AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset
import pandas as pd
import torch
from typing import Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CWEFinetuner:
    """Fine-tuning de modelos con dataset CWE"""
    
    def __init__(self, model_name: str = "microsoft/codebert-base"):
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        logger.info("Preparando fine-tuning con CWE dataset")
    
    def prepare_cwe_dataset(self, cwe_data_path: str = "./data/cwe_data") -> Dataset:
        """Prepara dataset CWE para fine-tuning"""
        # Dataset simulado de vulnerabilidades CWE
        # En producción, cargar de fuentes reales como CWE CAPEC
        data = {
            "code": [
                "SELECT * FROM users WHERE id = '" + input + "'",
                "<script>alert(document.cookie)</script>",
                "system('ping ' + host)",
                # Más ejemplos...
            ],
            "cwe_id": [
                "CWE-89",  # SQL Injection
                "CWE-79",  # XSS
                "CWE-78",  # Command Injection
            ]
        }
        
        df = pd.DataFrame(data)
        dataset = Dataset.from_pandas(df)
        
        # Tokenizar
        from transformers import AutoTokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        
        def tokenize_function(examples):
            return self.tokenizer(examples["code"], padding="max_length", truncation=True)
        
        tokenized_dataset = dataset.map(tokenize_function, batched=True)
        return tokenized_dataset
    
    def fine_tune(self, dataset: Dataset, output_dir: str = "./models/cwe_finetuned"):
        """Ejecuta fine-tuning"""
        logger.info("Iniciando fine-tuning con CWE dataset...")
        
        # Configurar modelo
        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.model_name,
            num_labels=15  # 15 categorías CWE principales
        )
        
        # Configurar entrenamiento
        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=3,
            per_device_train_batch_size=8,
            per_device_eval_batch_size=8,
            warmup_steps=500,
            weight_decay=0.01,
            logging_dir='./logs',
            logging_steps=10,
            save_strategy="epoch"
        )
        
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=dataset,
        )
        
        trainer.train()
        trainer.save_model(output_dir)
        logger.info(f"✅ Fine-tuning completado. Modelo guardado en {output_dir}")
        
        return trainer.model
    
    def load_finetuned_model(self, model_path: str = "./models/cwe_finetuned"):
        """Carga modelo fine-tuned"""
        from transformers import AutoModelForSequenceClassification
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        logger.info("Modelo fine-tuned cargado")
        return self.model
