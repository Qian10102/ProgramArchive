import numpy as np
def analyze_temperature(seed):
    np.set_printoptions(linewidth=1000)
    np.random.seed(seed)
    temperatures = np.random.uniform(10.0, 35.0, 7)
    average_temp = np.mean(temperatures)
    max_temp = np.max(temperatures)
    min_temp = np.min(temperatures)
    sorted_temps = np.sort(temperatures)
    temp_diff = temperatures - average_temp
    print(f"随机数种子：{seed}")
    print(f"生成的气温数据：{temperatures}")
    print(f"平均气温：{average_temp:.2f}°C")
    print(f"最高气温：{max_temp:.2f}°C")
    print(f"最低气温：{min_temp:.2f}°C")
    print(f"排序后的气温数据：{sorted_temps}")
    print(f"气温偏差：{temp_diff}")

seed = int(input())
analyze_temperature(seed)
