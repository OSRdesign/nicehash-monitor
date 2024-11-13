from nicehash_api import NiceHashAPI
from display_manager import DisplayManager
from data_formatter import DataFormatter
import time
import sys

def main():
    api = NiceHashAPI()
    display = DisplayManager()
    formatter = DataFormatter()
    
    while True:
        try:
            # Fetch data
            mining_data = api.get_mining_data()
            wallet_data = api.get_wallet_balance()
            
            # Format data
            stats = formatter.format_stats(mining_data, wallet_data)
            
            # Update display
            display.update_display(stats)
            
            # Wait for refresh interval (5 minutes)
            time.sleep(300)
            
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)
        except Exception as e:
            print(f"Error: {str(e)}")
            time.sleep(60)  # Wait 1 minute before retrying

if __name__ == "__main__":
    main()