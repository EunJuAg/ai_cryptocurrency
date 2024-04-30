#ETC orderbook 수집코드
import time
import requests
import pandas as pd
from datetime import datetime
import pytz

from google.colab import drive

drive.mount('/content/drive')

data_list = []

kst = pytz.timezone('Asia/Seoul')

while True:
    response = requests.get('https://api.bithumb.com/public/orderbook/ETC_KRW/?count=10')
    book = response.json()
    data = book['data']

    bids = pd.DataFrame(data['bids']).apply(pd.to_numeric, errors='ignore')
    bids.sort_values('price', ascending=False, inplace=True)
    bids.reset_index(drop=True, inplace=True)
    bids['type'] = 0

    asks = pd.DataFrame(data['asks']).apply(pd.to_numeric, errors='ignore')
    asks.sort_values('price', ascending=True, inplace=True)
    asks.reset_index(drop=True, inplace=True)
    asks['type'] = 1

    df = pd.concat([bids, asks])

    current_time_kst = datetime.now(kst)
    current_time_str = current_time_kst.strftime('%Y-%m-%d %H:%M:%S')
    df['timestamp'] = f"{current_time_str}.{current_time_kst.microsecond:06d}"

    data_list.append(df)

    if len(data_list) == 17280:

        current_time = datetime.now(kst).strftime('%Y-%m-%d-%H-%M-%S')
        filename = f"/content/drive/My Drive/ETC_Orderbook_{current_time}.csv"

        combined_df = pd.concat(data_list)
        combined_df.to_csv(filename, index=False)

        data_list = []

    time.sleep(5)
