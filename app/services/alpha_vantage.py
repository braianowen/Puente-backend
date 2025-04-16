# backend/app/services/alpha_vantage.py
import requests
from datetime import datetime, timedelta

class AlphaVantageService:
    def __init__(self, api_key="9GB194M168WJYBUD"):
        self.base_url = "https://www.alphavantage.co/query"
        self.api_key = api_key
        self.cache = {}
        self.cache_duration = timedelta(minutes=160) 

    def _is_cache_valid(self, symbol):
        cached_data = self.cache.get(symbol)
        if not cached_data:
            return False
        return datetime.now() < cached_data["expiration"]

    def get_global_quote(self, symbol: str):
        if self._is_cache_valid(symbol):
            print(f"✅ [CACHE] Datos de {symbol} obtenidos desde el caché")
            return self.cache[symbol]["data"]
        
        print(f"🌐 [API] Solicitando datos de {symbol} desde Alpha Vantage")
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": self.api_key
        }
        response = requests.get(self.base_url, params=params)
        data = response.json().get("Global Quote", {})
        
        # Almacenar en caché
        self.cache[symbol] = {
            "data": data,
            "expiration": datetime.now() + self.cache_duration
        }
        
        return data