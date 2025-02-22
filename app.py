import time
from binanceClass import BinanceAnaliz as BiAn
from binanceClass import BinanceInfo
from style import satirYaz
import numpy as np
from tabulate import tabulate

np.seterr(divide='ignore', invalid='ignore')

print("The app is working. Please wait a moment for the initial data to be received. Please ignore any error messages for the initial few data points.")

favourite_pairs = [
    'XRPUSDT', 'ADAUSDT',
]

holder = {symbol: BiAn(symbol) for symbol in favourite_pairs}  # Create objects in the dictionary


def sonuclariYaz():
    # get top pairs
    top_pairs = BinanceInfo().get_top_pairs(n=20)
    top_symbols = [pair['symbol'] for pair in top_pairs]
    favourite_pairs.extend(top_symbols)

    # remove duplicates
    unique_symbols = list(set(favourite_pairs))

    # update holder
    new_holder = {symbol: BiAn(symbol) for symbol in unique_symbols}
    holder.update(new_holder)

    half_size = len(holder) // 2
    left_symbols = list(holder.keys())[:half_size]
    right_symbols = list(holder.keys())[half_size:]
    
    left_data = []
    for k in left_symbols:
        try:
            left_data.append(satirYaz(holder[k]))
        except:
            left_data.append("Error")

    right_data = []
    for k in right_symbols:
        try:
            right_data.append(satirYaz(holder[k]))
        except:
            right_data.append("Error")

    rows = []
    max_len = max(len(left_data), len(right_data))
    for i in range(max_len):
        left_cols = left_data[i] if i < len(left_data) else ["", "", "", ""]
        right_cols = right_data[i] if i < len(right_data) else ["", "", "", ""]
        rows.append(left_cols + right_cols)

    print(
        tabulate(
            rows,
            headers=[
                "MARKET", "VOLUME", "↓↑", "LAST500",
                "MARKET", "VOLUME", "↓↑", "LAST500"
            ],
            tablefmt="fancy_grid"
        )
    )

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
