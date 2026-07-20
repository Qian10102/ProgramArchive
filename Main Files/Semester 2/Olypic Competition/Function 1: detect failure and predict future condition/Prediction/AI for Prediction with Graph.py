import pandas as pd
import matplotlib.pyplot as plt
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

def visualize_forecast(forecast_data, title="Voltage Forecast"):
    """可视化预测结果"""
    plt.figure(figsize=(12, 6))
    plt.plot(forecast_data['ds'], forecast_data['yhat'], label='Predicted Voltage', color='blue')
    plt.fill_between(forecast_data['ds'], forecast_data['yhat_lower'], forecast_data['yhat_upper'], alpha=0.2, color='blue', label='Confidence Interval')
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel('Time', fontsize=12)
    plt.ylabel('Voltage', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(loc='best')
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.savefig('voltage_forecast.png', dpi=300, bbox_inches='tight')
    plt.close()

def main_forecast():
    # 预测趋势
    forecast = forecast_trends("../Malfunction Detection/sensor_data.csv", periods=24)
    forecast.to_csv("forecast_data.csv", index=False)
    print("未来24小时电压预测已经存储进'forecast_data.csv'")
    # 可视化预测结果
    visualize_forecast(forecast, title="Voltage Forecast for Next 24 Hours")
    print("已生成预测趋势图，存储为 'voltage_forecast.png'")

if __name__ == "__main__":
    main_forecast()