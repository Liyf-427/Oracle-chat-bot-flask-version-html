import pandas as pd
import numpy as np
import joblib
from datetime import datetime, timedelta
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import MeanSquaredError
from sklearn.preprocessing import StandardScaler
import random

# **改进的 S&P 500 预测函数**
def pred_c(query_date):
    # **加载模型和Scaler**
    model = load_model('models/Oracle_model_S&P500_prediction.h5', custom_objects={'mse': MeanSquaredError()})
    scaler = joblib.load('models/S&P500_scaler.joblib')

    # **读取历史数据**
    path = 'data/S&P 500 Historical Data.csv'
    df = pd.read_csv(path, parse_dates=['Date'], dayfirst=True)  # 确保日期格式正确
    df = df.sort_values(by='Date')  # 确保按时间顺序排列
    df['Price'] = df['Price'].str.replace(',', '').astype(float)  # 处理价格数据

    # **用户输入目标日期**
    ##query_date = datetime.strptime(query_date, "%Y-%m-%d")

    # **计算需要预测的天数**
    query_date = pd.to_datetime(query_date).normalize()
    last_date = df['Date'].max()  # 获取数据集中最新的日期
    days_to_predict = (query_date - last_date).days  # 计算预测间隔
    if days_to_predict <= 0:
        print("Error: The date must be in the future!")
        return

    print(f"Predicting for {days_to_predict} days from {last_date.date()} to {query_date.date()}.")

    # **获取最新 10 天的数据**
    seq_length = 10
    last_10_days = df['Price'].values[-seq_length:]  # 获取最新10天的价格数据
    last_10_days_scaled = scaler.fit_transform(last_10_days.reshape(-1, 1))  # 归一化
    last_10_days_scaled = last_10_days_scaled.reshape(1, seq_length, 1).astype('float32')

    # **预测未来价格**
    predicted_prices = []
    for _ in range(days_to_predict):
        predicted_price = model.predict(last_10_days_scaled, verbose=0)  # 预测一天
        real_price = scaler.inverse_transform(predicted_price)[0][0]  # 逆归一化
        predicted_prices.append(real_price)

        # **更新输入数据**

        last_10_days_scaled = np.append(last_10_days_scaled[:, 1:, :], predicted_price.reshape(1, 1, 1)/seq_length, axis=1)

    # **输出结果**
    for i, price in enumerate(predicted_prices, 1):
        print(f"Predicted S&P 500 price for {last_date.date() + timedelta(days=i)}: {price:.2f}")
    # **获取最后一天的预测结果**
    final_price = predicted_prices[-1]
    prev_day_price = predicted_prices[-2] if len(predicted_prices) > 1 else df['Price'].values[-1]
    change_percentage = ((final_price - prev_day_price) / prev_day_price) * 100

    return final_price, change_percentage

