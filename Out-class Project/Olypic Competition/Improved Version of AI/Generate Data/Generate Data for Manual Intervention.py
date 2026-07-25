import numpy as np
import pandas as pd
import random

def generate_data(num_entries):
    data = []
    for i in range(num_entries):
        sensor_id = i + 1
        if random.random() < 0.05:
            power = round(random.uniform(0, 3), 2)
        else:
            power = round(random.uniform(3, 5), 2)
        if random.random() < 0.05:
            signal_strength = random.randint(-100, -80)
        else:
            signal_strength = random.randint(-80, -50)
        malfunction = 1 if (power < 2.5) or (signal_strength < -85) else 0
        data.append((sensor_id, power, signal_strength, malfunction))
    df = pd.DataFrame(data, columns=['sensor_ID', 'power', 'signal_strength', 'malfunction'])
    return df

def save_to_csv(data, file_name):
    """将数据保存为 CSV 文件"""
    data.to_csv(file_name, index=False, float_format='%.2f')
    print(f"数据已保存到 {file_name}")

if __name__ == '__main__':
    name = input()
    num_samples = 1000
    data = generate_data(num_samples)
    save_to_csv(data=data, file_name=name)