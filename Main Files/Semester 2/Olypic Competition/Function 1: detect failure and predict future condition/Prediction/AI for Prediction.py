import pandas as pd
from prophet import Prophet

def forecast_trends(file_name, periods=24):
    """预测电压趋势"""
    data = pd.read_csv(file_name)
    if not isinstance(data, pd.DataFrame) or 'Timestamp' not in data.columns or 'Voltage' not in data.columns:
        raise ValueError("输入数据必须是一个包含 'Timestamp' 和 'Voltage' 列的 pandas DataFrame")
    df = pd.DataFrame({"ds": pd.to_datetime(data["Timestamp"]), "y": data["Voltage"]})
    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(periods=periods, freq='h', include_history=False)
    forecast_voltage = round(model.predict(future), 6)
    return forecast_voltage[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

def main_forecast():
    # 预测趋势
    forecast = forecast_trends("../Malfunction Detection/sensor_data.csv", periods=24)
    forecast.to_csv("forecast_data.csv", index=False)
    print("未来24小时电压预测已经存储进'forecast_data.csv'")

if __name__ == "__main__":
    main_forecast()
