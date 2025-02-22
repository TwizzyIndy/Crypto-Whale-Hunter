import time
from binanceClass import BinanceAnaliz as BiAn
from binanceClass import BinanceInfo
from style import satirYaz
import numpy as np

np.seterr(divide='ignore', invalid='ignore')

print("The app is working. Please wait a moment for the initial data to be received. Please ignore any error messages for the initial few data points.")

favourite_pairs = [
    'XRPUSDT', 'ADAUSDT',
]

# get top pairs
top_pairs = BinanceInfo().get_top_pairs(n=20)
top_symbols = [pair['symbol'] for pair in top_pairs]

# extends the list of favourite pairs with the top pairs
# it can be duplicated, so we need to remove duplicates
favourite_pairs.extend(top_symbols)
favourite_pairs = list(set(favourite_pairs))

holder = {symbol: BiAn(symbol) for symbol in favourite_pairs}  # Create objects in the dictionary


def sonuclariYaz():
    print("#############################################")
    print(f"{'MARKET':<12}{'VOLUME':<12}{'↓↑':<2}{'LAST500':<10}")
    for key in holder:
        try:
            satirYaz(holder[key])
        except Exception as e:
            print(f"Error processing market {key}: {e}")

def main():
    # Initial data retrieval
    for key in holder:
        try:
            holder[key].refresh()
        except Exception as e:
            print(f"Error initializing market {key}: {e}")

    while True:
        sonuclariYaz()
        time.sleep(5)  # Wait before refreshing data
        for key in holder:
            try:
                holder[key].refresh()
                print('\033c', end='')  # Clear the screen
            except Exception as e:
                print(f"Error refreshing market {key}: {e}")

if __name__ == "__main__":
    main()
