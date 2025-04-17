# backend/app/services/coingecko.py
import requests
from datetime import datetime, timedelta
from typing import Dict, Optional

class CoinGeckoService:
    BASE_URL = "https://api.coingecko.com/api/v3"
    
    # Mapeo solo para las criptomonedas que usas
    CRYPTO_MAPPING = {
        'BTC': 'bitcoin',
        'ETH': 'ethereum',
        'XRP': 'ripple',
        'SOL': 'solana',
        'ADA': 'cardano'
    }
    
    def __init__(self):
        self.cache = {}
        self.cache_duration = timedelta(minutes=5)  # Actualización cada 5 minutos
    
    def _is_cache_valid(self, key: str) -> bool:
        cached_data = self.cache.get(key)
        if cached_data:
            if datetime.now() < cached_data["expiration"]:
                print(f"[CoinGecko Cache] Datos válidos en caché para {key}")
                return True
            print(f"[CoinGecko Cache] Datos expirados en caché para {key}")
        return False
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        try:
            print(f"[CoinGecko API] Haciendo request a: {endpoint}")
            response = requests.get(
                f"{self.BASE_URL}/{endpoint}",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            print(f"[CoinGecko API] Request exitoso a: {endpoint}")
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"[CoinGecko API] Error en la request: {str(e)}")
            return None
    
    def is_crypto(self, symbol: str) -> bool:
        """Determina si un símbolo es una criptomoneda soportada"""
        is_supported = symbol.upper() in self.CRYPTO_MAPPING
        print(f"[CoinGecko] Símbolo {symbol} {'es cripto soportada' if is_supported else 'no es cripto soportada'}") 
        return is_supported
    
    def get_crypto_data(self, symbol: str) -> Optional[Dict]:
        """Obtiene datos para una criptomoneda específica"""
        if not self.is_crypto(symbol):
            print(f"[CoinGecko] {symbol} no es cripto soportada, saltando...")
            return None
            
        coin_id = self.CRYPTO_MAPPING[symbol.upper()]
        cache_key = f"crypto_{symbol}"
        
        if self._is_cache_valid(cache_key):
            print(f"[CoinGecko Cache] Usando datos de caché para {symbol}")
            return self.cache[cache_key]["data"]
        
        print(f"[CoinGecko API] Solicitando datos para {symbol} (ID: {coin_id})")
        data = self._make_request(
            f"coins/{coin_id}",
            params={
                "localization": "false",
                "tickers": "false",
                "market_data": "true",
                "community_data": "false",
                "developer_data": "false"
            }
        )
        
        if not data:
            print(f"[CoinGecko API] No se obtuvieron datos para {symbol}")
            return None
            
        market_data = data.get("market_data", {})
        result = {
            "symbol": symbol,
            "name": data.get("name", ""),
            "price": market_data.get("current_price", {}).get("usd"),
            "change_24h": market_data.get("price_change_24h"),
            "change_percent_24h": market_data.get("price_change_percentage_24h"),
            "high_24h": market_data.get("high_24h", {}).get("usd"),
            "low_24h": market_data.get("low_24h", {}).get("usd"),
            "market_cap": market_data.get("market_cap", {}).get("usd"),
            "total_volume": market_data.get("total_volume", {}).get("usd"),
            "last_updated": data.get("last_updated"),
            "source": "CoinGecko"
        }
        
        print(f"[CoinGecko Cache] Almacenando en caché datos para {symbol}")
        self.cache[cache_key] = {
            "data": result,
            "expiration": datetime.now() + self.cache_duration
        }
        
        return result
    
def get_historical_data(self, symbol: str, days: int = 30) -> Optional[Dict]:
    if not self.is_crypto(symbol):
        return None
        
    coin_id = self.CRYPTO_MAPPING[symbol.upper()]
    cache_key = f"history_{symbol}_{days}"
    
    if self._is_cache_valid(cache_key):
        return self.cache[cache_key]["data"]
    
    print(f"[CoinGecko API] Solicitando datos históricos para {symbol}")
    data = self._make_request(
        f"coins/{coin_id}/market_chart",
        params={
            "vs_currency": "usd",
            "days": days,
            "interval": "daily"  # Añadimos intervalo diario
        }
    )
    
    if not data:
        return None
        
    # Procesamos para obtener apertura, cierre, máximo y mínimo diario
    prices = data.get("prices", [])
    daily_data = []
    
    # Agrupar por día (la API devuelve múltiples puntos por día)
    daily_groups = {}
    for point in prices:
        date = datetime.fromtimestamp(point[0]/1000).strftime('%Y-%m-%d')
        if date not in daily_groups:
            daily_groups[date] = []
        daily_groups[date].append(point[1])
    
    # Calcular valores para cada día
    for date, values in daily_groups.items():
        if values:
            daily_data.append({
                "date": date,
                "open": values[0],  # Primer precio del día
                "close": values[-1],  # Último precio del día
                "high": max(values),
                "low": min(values),
                "price": values[-1]  # Usamos el cierre como precio representativo
            })
    
    historical_data = {
        "daily": daily_data,
        "source": "CoinGecko"
    }
    
    self.cache[cache_key] = {
        "data": historical_data,
        "expiration": datetime.now() + self.cache_duration
    }
    
    return historical_data