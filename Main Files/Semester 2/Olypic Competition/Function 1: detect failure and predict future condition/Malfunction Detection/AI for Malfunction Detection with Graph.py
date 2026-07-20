import random
import pandas as pd
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt

# 设定数据范围（正常范围）
VOLTAGE_RANGE = (2.75, 3.25)  # 伏特
CURRENT_RANGE = (3e-4, 4e-4)  # 安培
SIGNAL_STRENGTH_RANGE = (-80, -50)  # dB
SIGNAL_FREQUENCY_RANGE = (2.14e13, 3.75e13)  # Hz
SENSOR_IDS = ["S01"]  # 监测器ID

def generate_sensor_data(timestamp):
    """生成单条模拟传感器数据"""
    sensor_id = random.choice(SENSOR_IDS)
    voltage = round(random.uniform(*VOLTAGE_RANGE), 6)
    current = round(random.uniform(*CURRENT_RANGE), 6)
    signal_strength = round(random.uniform(*SIGNAL_STRENGTH_RANGE), 6)
    signal_frequency = round(random.uniform(*SIGNAL_STRENGTH_RANGE), 6)
    # 10% 概率生成异常数据
    if random.random() <= 0.10:
        voltage = round(random.uniform(2.0, 2.5), 6)  # 电压突降
        current = round(random.uniform(0.1, 0.3), 6)  # 电流异常降低
        signal_strength = round(random.uniform(-100, -90), 6)  # 信号变差
        signal_frequency = round(random.uniform(3.0, 4.0), 6)  # 频率异常
    return [timestamp, sensor_id, voltage, current, signal_strength, signal_frequency]

def generate_data_to_csv(file_name, num_entries):
    """生成多条数据并存入 CSV 文件"""
    data = []
    start_time = datetime.now()
    for i in range(num_entries):
        timestamp = start_time + timedelta(hours=i)  # 确保时间戳不重复
        entry = generate_sensor_data(timestamp.strftime("%Y-%m-%d %H:%M:%S"))
        data.append(entry)
    df = pd.DataFrame(data, columns=["Timestamp", "Sensor_ID", "Voltage", "Current", "Signal_Strength", "Response_Frequency"])
    df.to_csv(file_name, index=False)
    contamination = (df["Voltage"] < 2.5).mean()  # 假设电压小于2.5为异常
    print(f"已生成 {num_entries} 条模拟数据，存储于 {file_name}。错误数据的比例为 {contamination:.2%}")
    return contamination

def preprocess_data(file_name, columns_to_normalize):
    """从 CSV 文件读取数据并进行预处理"""
    try:
        data = pd.read_csv(file_name).dropna()  # 读取并去掉空数据
        if data.empty:
            raise ValueError("数据为空，无法进行预处理。")
    except FileNotFoundError:
        print("错误：文件未找到，请检查文件名和路径。")
        return None, None
    except ValueError as ve:
        print(ve)
        return None, None
    # 归一化指定列，并保留 Timestamp 列
    scaler = MinMaxScaler()
    normalized_data = scaler.fit_transform(data[columns_to_normalize])
    normalized_df = pd.DataFrame(normalized_data, columns=columns_to_normalize)
    normalized_df['Timestamp'] = data['Timestamp'].values  # 添加 Timestamp 列
    print("已完成数据处理")
    return normalized_df, data

def detect_anomalies(processed_data, num_trials=100):
    """寻找最佳 contamination 值并检测异常数据，同时记录不同 contamination 值及其异常比例及差值"""
    best_contamination = None
    lowest_anomaly_ratio = float('inf')
    contamination_results = []  # 记录每次尝试的 contamination 值和异常比例
    # 原始数据的错误比例（10%）
    original_error_ratio = 0.15
    for _ in range(num_trials):  # 随机调整num_trials次
        random_contamination = round(random.uniform(0.01, 0.2), 6)
        model = IsolationForest(contamination=random_contamination, random_state=42)
        model.fit(processed_data[["Voltage", "Current", "Signal_Strength", "Response_Frequency"]])
        anomaly_scores = model.predict(processed_data[["Voltage", "Current", "Signal_Strength", "Response_Frequency"]])
        processed_data["Anomaly_Score"] = anomaly_scores
        anomalies = processed_data[processed_data["Anomaly_Score"] == -1]
        current_anomaly_ratio = len(anomalies) / len(processed_data)
        print(f"尝试的 contamination 值: {random_contamination:.2f}, 当前异常比例: {current_anomaly_ratio:.2f}")
        # 计算差值
        difference = abs(current_anomaly_ratio - original_error_ratio)
        print(f"与原始错误比例的差值: {difference:.4f}")
        # 记录 contamination 值、异常比例和差值
        contamination_results.append({
            'contamination': random_contamination,
            'anomaly_ratio': current_anomaly_ratio,
            'difference': difference
        })
        if current_anomaly_ratio < lowest_anomaly_ratio:
            lowest_anomaly_ratio = current_anomaly_ratio
            best_contamination = random_contamination
    # 将 contamination_results 保存为 CSV 文件
    contamination_df = pd.DataFrame(contamination_results)
    contamination_df.to_csv("contamination_analysis.csv", index=False)
    print(f"已将 contamination 分析结果保存至 'contamination_analysis.csv'")
    print(f"最佳 contamination 值：{best_contamination}，最低异常比例：{lowest_anomaly_ratio:.2f}")
    return processed_data, best_contamination

def plot_contamination_analysis():
    """绘制contamination值与异常比例及差值的折线图"""
    try:
        # 读取 contamination 分析结果
        contamination_df = pd.read_csv("contamination_analysis.csv")
        print("加载 contamination 分析结果成功。")
        # 检查必要列是否存在
        if 'contamination' not in contamination_df.columns or 'anomaly_ratio' not in contamination_df.columns or 'difference' not in contamination_df.columns:
            print("错误：contamination_analysis.csv 文件缺少必要列。")
            return
        # 按 contamination 值排序
        contamination_df.sort_values(by='contamination', inplace=True)
        # 绘制异常比例折线图
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.plot(contamination_df['contamination'], contamination_df['anomaly_ratio'], marker='o', markersize=8, linestyle='-', linewidth=2, color='blue', label='Anomaly Ratio')
        plt.title('Contamination Value vs Anomaly Ratio', fontsize=14, fontweight='bold')
        plt.xlabel('Contamination Value', fontsize=12)
        plt.ylabel('Anomaly Ratio', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(loc='best')
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
        # 绘制差值折线图
        plt.subplot(1, 2, 2)
        plt.plot(contamination_df['contamination'], contamination_df['difference'], marker='o', markersize=8, linestyle='-', linewidth=2, color='red', label='Difference')
        plt.title('Contamination Value vs Difference', fontsize=14, fontweight='bold')
        plt.xlabel('Contamination Value', fontsize=12)
        plt.ylabel('Difference', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(loc='best')
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
        # 调整布局
        plt.tight_layout()
        # 保存图表
        plt.savefig('contamination_analysis_plot.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("已生成 contamination 分析折线图，存储为 'contamination_analysis_plot.png'。")
    except FileNotFoundError:
        print("错误：未找到 'contamination_analysis.csv' 文件，无法生成图表。")
    except Exception as e:
        print(f"错误：{str(e)}")

def main():
    # 生成模拟数据
    contamination = generate_data_to_csv("sensor_data.csv", num_entries=500)
    # 预处理数据
    processed_data, original_data = preprocess_data("sensor_data.csv", columns_to_normalize=["Voltage", "Current", "Signal_Strength", "Response_Frequency"])
    # 检测异常
    processed_data, best_contamination = detect_anomalies(processed_data)
    # 输出异常数据
    anomalies = processed_data[processed_data["Anomaly_Score"] == -1]
    if not anomalies.empty:
        anomalies.to_csv("anomalies.csv", index=False)
        print("异常数据已经储存进'anomalies.csv'")
    else:
        print("未检测到异常数据。")
    # 生成 contamination 分析折线图
    plot_contamination_analysis()


if __name__ == "__main__":
    main()