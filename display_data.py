import json
from datetime import datetime

class MockNiceHashData:
    def get_mining_data(self):
        return {
            "miningRigs": [
                {
                    "minerStatus": "MINING",
                    "stats": {
                        "speedAccepted": 95450000  # 95.45 MH/s
                    }
                },
                {
                    "minerStatus": "MINING",
                    "stats": {
                        "speedAccepted": 85320000  # 85.32 MH/s
                    }
                }
            ]
        }

    def get_wallet_balance(self):
        return {
            "currencies": [
                {
                    "currency": "BTC",
                    "available": "0.00123456"
                },
                {
                    "currency": "ETH",
                    "available": "0.05432100"
                }
            ]
        }

def format_hashrate(hashrate):
    if hashrate > 1e9:
        return f"{hashrate/1e9:.2f} GH/s"
    elif hashrate > 1e6:
        return f"{hashrate/1e6:.2f} MH/s"
    elif hashrate > 1e3:
        return f"{hashrate/1e3:.2f} KH/s"
    return f"{hashrate:.2f} H/s"

def display_stats():
    api = MockNiceHashData()
    
    try:
        # Get mock data
        mining_data = api.get_mining_data()
        wallet_data = api.get_wallet_balance()
        
        # Print timestamp
        print(f"\n=== NiceHash Stats ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ===\n")
        
        # Process mining rigs data
        if 'miningRigs' in mining_data:
            total_hashrate = 0
            active_rigs = 0
            
            for rig in mining_data['miningRigs']:
                if rig['minerStatus'] == 'MINING':
                    active_rigs += 1
                    if 'stats' in rig and rig['stats']:
                        total_hashrate += float(rig['stats'].get('speedAccepted', 0))
            
            print(f"Active Rigs: {active_rigs}")
            print(f"Total Hashrate: {format_hashrate(total_hashrate)}")
        
        # Process wallet data
        if 'currencies' in wallet_data:
            print("\nWallet Balances:")
            for currency in wallet_data['currencies']:
                if float(currency['available']) > 0:
                    print(f"{currency['currency']}: {float(currency['available']):.8f}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    display_stats()