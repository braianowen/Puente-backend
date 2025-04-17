# backend/app/services/alpha_vantage.py
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class AlphaVantageService:
    def __init__(self, api_key="9GB194M168WJYBUD"):
        self.base_url = "https://www.alphavantage.co/query"
        self.api_key = api_key
        self.cache = {}
        self.cache_duration = timedelta(minutes=160)  

    def _is_cache_valid(self, symbol: str, endpoint: str) -> bool:
        cached_data = self.cache.get((symbol, endpoint))
        if not cached_data:
            return False
        return datetime.now() < cached_data["expiration"]

    def _make_request(self, params: Dict) -> Optional[Dict]:
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ [API] Error en la solicitud: {e}")
            return None

    def get_global_quote(self, symbol: str) -> Dict:
        cache_key = (symbol, "GLOBAL_QUOTE")
        if self._is_cache_valid(*cache_key):
            print(f"✅ [CACHE] Datos de {symbol} obtenidos desde el caché (GLOBAL_QUOTE)")
            return self.cache[cache_key]["data"]
        
        print(f"🌐 [API] Solicitando GLOBAL_QUOTE para {symbol}")
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": self.api_key
        }
        
        data = self._make_request(params)
        quote_data = data.get("Global Quote", {}) if data else {}
        
        # Transformar datos a formato consistente
        processed_data = {
            'symbol': symbol,
            'price': quote_data.get('05. price'),
            'change': quote_data.get('09. change'),
            'change_percent': quote_data.get('10. change percent'),
            'open': quote_data.get('02. open'),
            'high': quote_data.get('03. high'),
            'low': quote_data.get('04. low'),
            'volume': quote_data.get('06. volume'),
            'latest_trading_day': quote_data.get('07. latest trading day'),
            'previous_close': quote_data.get('08. previous close')
        }
        
        # Almacenar en caché
        self.cache[cache_key] = {
            "data": processed_data,
            "expiration": datetime.now() + self.cache_duration
        }
        
        return processed_data

    def get_time_series_daily(self, symbol: str, outputsize: str = 'compact') -> Dict:
        cache_key = (symbol, f"TIME_SERIES_DAILY_{outputsize}")
        if self._is_cache_valid(*cache_key):
            print(f"✅ [CACHE] Datos de {symbol} obtenidos desde el caché (TIME_SERIES_DAILY)")
            return self.cache[cache_key]["data"]
        
        print(f"🌐 [API] Solicitando TIME_SERIES_DAILY para {symbol}")
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "outputsize": outputsize,  # 'compact' (100 datos) o 'full' (20+ años)
            "apikey": self.api_key
        }
        
        data = self._make_request(params)
        time_series = data.get("Time Series (Daily)", {}) if data else {}
        
        # Procesar datos históricos
        processed_data = {
            'symbol': symbol,
            'last_refreshed': data.get('Meta Data', {}).get('3. Last Refreshed'),
            'time_series': {
                date: {
                    'open': values['1. open'],
                    'high': values['2. high'],
                    'low': values['3. low'],
                    'close': values['4. close'],
                    'volume': values['5. volume']
                }
                for date, values in time_series.items()
            }
        }
        
        # Almacenar en caché
        self.cache[cache_key] = {
            "data": processed_data,
            "expiration": datetime.now() + self.cache_duration
        }
        
        return processed_data

    def get_instrument_details(self, symbol: str) -> Dict:
        """Obtiene datos completos combinando GLOBAL_QUOTE y TIME_SERIES_DAILY"""
        quote = self.get_global_quote(symbol)
        time_series = self.get_time_series_daily(symbol, outputsize='compact')
        
        return {
            **quote,
            **time_series,
            'historical_data': self._process_historical_data(time_series.get('time_series', {}))
        }

    def _process_historical_data(self, time_series: Dict) -> List:
        """Procesa datos históricos para el frontend"""
        return [
            {
                'date': date,
                'price': float(data['close']),
                'volume': int(data['volume']),
                'variation': self._calculate_variation(data)
            }
            for date, data in sorted(time_series.items(), reverse=True)
        ]

    def _calculate_variation(self, daily_data: Dict) -> float:
        try:
            open_price = float(daily_data['open'])
            close_price = float(daily_data['close'])
            return ((close_price - open_price) / open_price) * 100
        except (ValueError, KeyError):
            return 0.0