import pandas as pd
import numpy as np
from google.colab import files

uploaded = files.upload() #사용자로부터 데이터파일(csv)를 업로드 받음

#업로드된 파일 읽기
file_name = list(uploaded.keys())[0]
data = pd.read_csv(file_name)
print(data.head())

data['timestamp'] = pd.to_datetime(data['timestamp']) #timestamp를 datetime 형식으로 변환
data['direction'] = np.where(data['side'] == 1, 1, -1) #side에 따라 각 거래의 방향을 결정 (0=매도, 1=매수)

data['pnl'] = data['amount'] - (data['quantity'] * data['price']) - data['fee'] #모든 거래에 대한 PnL 각각 계산
data['cumulative_pnl'] = data['pnl'].cumsum() #누적 PnL 계산
print("Cumulative PnL: ") #누적 PnL 출력
print(data[['timestamp', 'cumulative_pnl']])

#누적 PnL 그래프로 나타내기
import matplotlib.pyplot as plt
plt.figure(figsize=(12, 6))
plt.plot(data['timestamp'], data['cumulative_pnl'], marker='o')
plt.xlabel('Timestamp')
plt.ylabel('Cumulative PnL')
plt.title('Cumulative PnL over Time')
plt.grid(True)
plt.show()
