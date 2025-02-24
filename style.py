def satirYaz(market):
    # Calculate the volume change ratio. If greater than 1, there is an increase; if less than 1, a decrease.
    hacim_deg= market.hacim_degisim()
    if hacim_deg > 1.5:
        color = '\x1b[6;30;42m' # Green
    elif hacim_deg > 1:
        color = '\x1b[5;30;43m' # Yellow
    elif hacim_deg > 0.6:
        color = '\x1b[6;30;47m' # White
    else:
        color = '\x1b[6;31;47m' # Red

    # Calculate the price change ratio. If greater than 3, there is an increase; if less than 3, a decrease.
    artis_deg= market.fiyat_artis_azalis()
    if artis_deg >= 3:
        color_artis = '\x1b[6;30;42m'
        if artis_deg == 4:
            icerik = '↑↑'
        else:
            icerik = '  '
    else:
        color_artis = '\x1b[6;30;41m'
        if artis_deg == 1:
            icerik = '↓↓'
        else:
            icerik = '  '

    # get 5m trend
    trend_5m = market.detect_trend_sma(interval="5m", limit=5)
    
    buy_ratio = market.buy_volume_ratio()
    
    return [
        market.df24['symbol'],
        color + f"{hacim_deg:.4f}" + '\x1b[0m',
        f"{buy_ratio * 100:.2f}%",
        color_artis + icerik + '\x1b[0m',
        f"{int(market.recent_trades_time_interval())}sec",
        trend_5m
    ]