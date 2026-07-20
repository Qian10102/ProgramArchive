import random
import pandas as pd
from datetime import datetime, timedelta

def generate_sensor_data(timestamp):
    """生成单条模拟传感器数据"""
    power = round(random.uniform(3, 5), 6)
    signal_strength = round(random.uniform(-80, 50), 6)
    return [timestamp, power, signal_strength]

def generate_data_to_csv(file_name, num_entries):
    """生成多条数据并存入 CSV 文件"""
    data = []
    start_time = datetime.now()
    for i in range(num_entries):
        timestamp = start_time + timedelta(hours=i)  # 确保时间戳不重复
        entry = generate_sensor_data(timestamp.strftime("%Y-%m-%d %H:%M:%S"))
        data.append(entry)
    df = pd.DataFrame(data, columns=["timestamp", "power", "signal_strength"])
    df.to_csv(file_name, index=False)

if __name__ == "__main__":
    generate_data_to_csv("sensor_data.csv", num_entries=500)