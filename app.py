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

    # collect (ratio, row) tuples
    data_list = []
    for sym in holder:
        try:
            ratio = holder[sym].hacim_degisim()
            row = satirYaz(holder[sym])  # returns four-column list
            data_list.append((ratio, row))
        except:
            # Create a dummy row for errors
            data_list.append((0, [sym, "-", "-", "-", "-", "-"]))

    # sort by ratio decending
    data_list.sort(key=lambda x: x[0], reverse=True)

    # split into left and right columns
    half_size = len(data_list) // 2
    left_data = [item[1] for item in data_list[:half_size]]
    right_data = [item[1] for item in data_list[half_size:]]

    # build final rows for tabulate
    rows = []
    max_len = max(len(left_data), len(right_data))
    for i in range(max_len):
        left_cols = left_data[i] if i < len(left_data) else ["", "", "", "", "", ""]
        right_cols = right_data[i] if i < len(right_data) else ["", "", "", "", "", ""]
        rows.append(left_cols + right_cols)

    print(
        tabulate(
            rows,
            headers=[
                "MARKET", "VOLUME", "BVR", "↓↑", "LAST500", "TREND",
                "MARKET", "VOLUME", "BVR", "↓↑", "LAST500", "TREND", 
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
