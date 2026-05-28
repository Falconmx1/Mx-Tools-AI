# core/redis_cache.py
import redis
import pickle
import hashlib
import json
from typing import Any, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelCache:
    """Caché de modelos y resultados usando Redis"""
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        try:
            self.redis_client = redis.from_url(redis_url, decode_responses=False)
            self.redis_client.ping()
            self.enabled = True
            logger.info("✅ Redis cache conectado")
        except Exception as e:
            logger.warning(f"⚠️ Redis no disponible: {e}. Cache deshabilitado.")
            self.enabled = False
    
    def _get_key(self, prefix: str, data: Any) -> str:
        """Genera hash único para cachear"""
        data_str = json.dumps(data) if isinstance(data, (dict, list)) else str(data)
        hash_key = hashlib.md5(data_str.encode()).hexdigest()
        return f"mx_tools:{prefix}:{hash_key}"
    
    def cache_model_output(self, model_name: str, input_data: Any, output: Any, ttl: int = 3600):
        """Cachea output de modelos"""
        if not self.enabled:
            return
        
        key = self._get_key(model_name, input_data)
        try:
            self.redis_client.setex(key, ttl, pickle.dumps(output))
            logger.debug(f"Output cacheado para {model_name}")
        except Exception as e:
            logger.error(f"Error cacheando: {e}")
    
    def get_cached_output(self, model_name: str, input_data: Any) -> Optional[Any]:
        """Recupera output cacheado"""
        if not self.enabled:
            return None
        
        key = self._get_key(model_name, input_data)
        try:
            cached = self.redis_client.get(key)
            if cached:
                logger.debug(f"Cache hit para {model_name}")
                return pickle.loads(cached)
        except Exception as e:
            logger.error(f"Error recuperando cache: {e}")
        return None
    
    def clear_model_cache(self, model_name: str):
        """Limpia cache de un modelo específico"""
        if not self.enabled:
            return
        
        pattern = f"mx_tools:{model_name}:*"
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                self.redis_client.delete(*keys)
                logger.info(f"Cache limpiado para {model_name}")
        except Exception as e:
            logger.error(f"Error limpiando cache: {e}")
