from datetime import datetime
import json
import requests
from typing import Optional

class DataFormatter:
    COINGECKO_API_URL = "https://api.coingecko.com/api/v3"
    
    @staticmethod
    def get_btc_eur_rate() -> Optional[float]:
        """Obtient le taux de conversion BTC/EUR depuis CoinGecko."""
        try:
            response = requests.get(
                f"{DataFormatter.COINGECKO_API_URL}/simple/price",
                params={
                    "ids": "bitcoin",
                    "vs_currencies": "eur"
                },
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            return float(data['bitcoin']['eur'])
        except (requests.RequestException, KeyError, ValueError) as e:
            print(f"Erreur lors de la récupération du taux BTC/EUR: {e}")
            return None
    
    @staticmethod
    def format_hashrate(hashrate):
        if hashrate > 1e9:
            return f"{hashrate/1e9:.2f} GH/s"
        elif hashrate > 1e6:
            return f"{hashrate/1e6:.2f} MH/s"
        elif hashrate > 1e3:
            return f"{hashrate/1e3:.2f} KH/s"
        return f"{hashrate:.2f} H/s"
    
    @staticmethod
    def format_stats(mining_data, wallet_data):
        stats = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'active_rigs': '0 (total 0)',
            'total_hashrate': '0 MH/s',
            'balances': {},
            'balance_eur': '0.00 €'
        }
        
        # Process mining data
        if 'miningRigs' in mining_data:
            active_rigs = mining_data.get('minerStatuses', {}).get('MINING', 0)
            total_rigs = mining_data.get('totalRigs', 0)
            stats['active_rigs'] = f"{active_rigs} (total {total_rigs})"
            
            total_hashrate = 0
            main_algo = ""
            
            if 'totalSpeedAccepted' in mining_data:
                # Trouver l'algorithme avec la vitesse la plus élevée
                max_speed = 0
                for algo_id, speed in mining_data['totalSpeedAccepted'].items():
                    speed_float = float(speed)
                    total_hashrate += speed_float
                    if speed_float > max_speed:
                        max_speed = speed_float
                        for rig in mining_data.get('miningRigs', []):
                            for stat in rig.get('stats', []):
                                if str(algo_id) == '61':
                                    main_algo = "VRSC"
                                    break
            
            stats['total_hashrate'] = f"{total_hashrate:.2f} MH/s {main_algo}"
        
        # Process wallet data
        if 'currencies' in wallet_data:
            btc_balance = 0
            for currency in wallet_data['currencies']:
                if currency['currency'] == 'BTC':
                    btc_balance = float(currency['available'])
                if float(currency['available']) > 0:
                    stats['balances'][currency['currency']] = f"{float(currency['available']):.8f}"
            
            # Obtenir le taux BTC/EUR et calculer la valeur en EUR
            if btc_balance > 0:
                eur_rate = DataFormatter.get_btc_eur_rate()
                if eur_rate:
                    balance_eur = btc_balance * eur_rate
                    stats['balance_eur'] = f"{balance_eur:.2f} €"
                else:
                    print("Impossible d'obtenir le taux BTC/EUR")
        
        return stats