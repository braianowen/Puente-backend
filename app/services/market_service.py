# backend/app/services/market_service.py
from typing import Dict, Optional
from app.services.alpha_vantage import AlphaVantageService
from app.services.coingecko import CoinGeckoService

class MarketDataService:
    def __init__(self):
        self.alpha_vantage = AlphaVantageService()
        self.coingecko = CoinGeckoService()
        print("[MarketService] Servicio inicializado")
    
    def get_instrument_data(self, symbol: str) -> Optional[Dict]:
        print(f"\n[MarketService] Buscando datos para {symbol}")
        
        # Primero verificar si es una criptomoneda
        if self.coingecko.is_crypto(symbol):
            print(f"[MarketService] {symbol} es cripto, intentando con CoinGecko")
            crypto_data = self.coingecko.get_crypto_data(symbol)
            if crypto_data:
                print(f"[MarketService] Datos obtenidos de CoinGecko para {symbol}")
                return self._format_coingecko_data(crypto_data)
            print(f"[MarketService] CoinGecko no devolvió datos para {symbol}")
        
        # Si no es cripto o CoinGecko falla, usar AlphaVantage
        print(f"[MarketService] Intentando con AlphaVantage para {symbol}")
        alpha_data = self.alpha_vantage.get_global_quote(symbol)
        
        # Verificar si AlphaVantage devolvió un error de límite
        if isinstance(alpha_data, dict) and "Information" in alpha_data:
            print(f"[MarketService] ERROR: Límite de AlphaVantage alcanzado - {alpha_data['Information']}")
            return None
        
        if alpha_data:
            print(f"[MarketService] Datos obtenidos de AlphaVantage para {symbol}")
            return self._format_alpha_vantage_data(alpha_data, symbol)
        
        print(f"[MarketService] No se pudieron obtener datos para {symbol}")
        return None
    
    def _format_alpha_vantage_data(self, data: Dict, symbol: str) -> Dict:
        formatted = {
            "symbol": symbol,
            "name": data.get("name", ""),
            "price": data.get("05. price"),
            "change": data.get("09. change"),
            "change_percent": data.get("10. change percent"),
            "open": data.get("02. open"),
            "high": data.get("03. high"),
            "low": data.get("04. low"),
            "volume": data.get("06. volume"),
            "latest_trading_day": data.get("07. latest trading day"),
            "previous_close": data.get("08. previous close"),
            "source": "AlphaVantage"
        }
        print(f"[MarketService] Datos formateados de AlphaVantage: {formatted}")
        return formatted
    
    def _format_coingecko_data(self, data: Dict) -> Dict:
        formatted = {
            "symbol": data["symbol"],
            "name": data["name"],
            "price": str(data["price"]),
            "change": str(data["change_24h"]),
            "change_percent": f"{data['change_percent_24h']}%",
            "high_24h": str(data["high_24h"]),
            "low_24h": str(data["low_24h"]),
            "market_cap": str(data["market_cap"]),
            "volume": str(data["total_volume"]),
            "last_updated": data["last_updated"],
            "source": "CoinGecko"
        }
        print(f"[MarketService] Datos formateados de CoinGecko: {formatted}")
        return formatted