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
            signal_strength = random.randint(-100, -90)
        else:
            signal_strength = random.randint(-80, -50)
        malfunction = 1 if (power < 3) or (signal_strength < -80) else 0
        data.append((sensor_id, power, signal_strength, malfunction))
    df = pd.DataFrame(data, columns=['sensor_ID', 'power', 'signal_strength', 'malfunction'])
    return df

try:
    num_entries = int(input("请输入需要生成的数据个数: "))
    if num_entries <= 0:
        print("请输入一个正整数。")
    else:
        output_file_name = "train_data.csv"
        generated_data = generate_data(num_entries)
        print(generated_data)
        generated_data.to_csv(output_file_name, index=False)
        print(f"生成的数据已保存到 {output_file_name}")

except ValueError:
    print("请输入一个有效的整数。")