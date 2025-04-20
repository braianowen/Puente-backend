# backend/app/services/market_service.py
from typing import Dict, List, Optional
from app.services.alpha_vantage import AlphaVantageService
from app.services.coingecko import CoinGeckoService

class MarketDataService:
    def __init__(self):
        self.alpha_vantage = AlphaVantageService()
        self.coingecko = CoinGeckoService()
        print("[MarketService] Servicio inicializado")
    
    def get_instrument_data(self, symbol: str) -> Optional[Dict]:
        print(f"\n[MarketService] Buscando datos para {symbol}")
        
        # Primero intentar con AlphaVantage para acciones
        print(f"[MarketService] Intentando con AlphaVantage para {symbol}")
        alpha_data = self.alpha_vantage.get_global_quote(symbol)
        
        # Verificar si AlphaVantage devolvió datos válidos
        if alpha_data and not alpha_data.get("error"):
            print(f"[MarketService] Datos obtenidos de AlphaVantage para {symbol}")
            formatted_data = self._format_alpha_vantage_data(alpha_data)
            
            # Añadir datos históricos básicos
            historical = self.alpha_vantage.get_time_series_daily(symbol, outputsize='compact')
            if historical:
                formatted_data["historicalData"] = historical
            
            return formatted_data
        
        # Si no es una acción válida, probar con criptomonedas
        if self.coingecko.is_crypto(symbol):
            print(f"[MarketService] {symbol} es cripto, intentando con CoinGecko")
            crypto_data = self.coingecko.get_crypto_data(symbol)
            if crypto_data:
                print(f"[MarketService] Datos obtenidos de CoinGecko para {symbol}")
                return self._format_coingecko_data(crypto_data)
        
        print(f"[MarketService] No se pudieron obtener datos para {symbol}")
        return None

    
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
    
    def _format_alpha_vantage_data(self, data: Dict, symbol: str = None) -> Dict:
        """Formatea los datos de AlphaVantage para el frontend"""
        if not symbol:
            symbol = data.get("symbol")
        
        return {
            "symbol": symbol,
            "name": symbol,  # AlphaVantage no provee nombre, usamos el símbolo
            "price": data.get("price"),
            "change": data.get("change"),
            "change_percent": data.get("change_percent"),
            "open": data.get("open"),
            "high": data.get("high"),
            "low": data.get("low"),
            "volume": data.get("volume"),
            "latest_trading_day": data.get("latest_trading_day"),
            "previous_close": data.get("previous_close"),
            "source": "AlphaVantage",
            # Campos adicionales para compatibilidad
            "close": data.get("price"),  # Mismo que price
            "high_24h": data.get("high"),
            "low_24h": data.get("low"),
            "total_volume": data.get("volume"),
            "historicalData": data.get("historicalData", {"daily": []})
        }

    def _generate_daily_data_for_alpha(self, quote_data: Dict) -> List[Dict]:
        """Genera datos diarios mínimos para compatibilidad con el frontend"""
        if not quote_data:
            return []
        
        return [{
            "date": quote_data.get("07. latest trading day", ""),
            "open": quote_data.get("02. open"),
            "high": quote_data.get("03. high"),
            "low": quote_data.get("04. low"),
            "close": quote_data.get("05. price"),
            "price": quote_data.get("05. price"),
            "volume": quote_data.get("06. volume")
        }]