import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sensor_data(num_records):
    """生成传感器数据"""
    sensor_IDs = np.arange(1, num_records + 1)
    # 生成时间戳，从当前时间开始
    start_time = datetime.now()
    timestamps = [start_time + timedelta(minutes=i) for i in range(num_records)]
    # 生成 power 和 signal_strength 数据，保留两位小数
    power = np.random.uniform(3, 5, num_records)
    power = np.round(power, 2)
    signal_strength = np.random.uniform(-80, -50, num_records)
    signal_strength = np.round(signal_strength, 2)
    # 创建 DataFrame
    data = pd.DataFrame({
        'sensor_ID': sensor_IDs,
        'timestamp': timestamps,
        'power': power,
        'signal_strength': signal_strength
    })
    return data

def save_to_csv(data, file_name):
    """将数据保存为 CSV 文件"""
    data.to_csv(file_name, index=False, float_format='%.2f')
    print(f"数据已保存到 {file_name}")

def main():
    num_records = 100  # 生成 100 条记录
    sensor_data = generate_sensor_data(num_records)
    save_to_csv(sensor_data, 'sensor_data.csv')

if __name__ == "__main__":
    main()
