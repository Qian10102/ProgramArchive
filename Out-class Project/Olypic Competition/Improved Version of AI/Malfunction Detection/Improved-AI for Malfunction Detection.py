import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.metrics import accuracy_score

def load_data_from_csv(file_path, load_labels=False):
    df = pd.read_csv(file_path)

    if not all(col in df.columns for col in ['power', 'signal_strength']):
        raise ValueError("CSV 文件中必须包含 'power' 和 'signal_strength' 列")

    power = df['power'].values
    signal_strength = df['signal_strength'].values
    X = np.array(list(zip(power, signal_strength)))

    if load_labels and 'malfunction' in df.columns:
        labels = df['malfunction'].values  # 仅当需要标签时加载
        return X, np.arange(1, len(df) + 1), labels  # sensor_ID 从 1 开始

    return X, np.arange(1, len(df) + 1)  # sensor_ID 从 1 开始

# 指定 CSV 文件的路径
train_file_path = '/Users/qian10102/PycharmProjects/PycharmProject/Main Files/Semester 2/Olypic Competition/Improved Version of AI/Generate Data/train_data.csv'
test_file_path = '/Users/qian10102/PycharmProjects/PycharmProject/Main Files/Semester 2/Olypic Competition/Improved Version of AI/Generate Data/test_data.csv'
test_answer_file_path = '/Users/qian10102/PycharmProjects/PycharmProject/Main Files/Semester 2/Olypic Competition/Improved Version of AI/Generate Data/test_data_answer.csv'

# 从 CSV 文件加载训练和测试数据
X_train, sensor_IDs_train, labels_train = load_data_from_csv(train_file_path, load_labels=True)
X_test, sensor_IDs_test = load_data_from_csv(test_file_path)

# 加载测试答案文件
test_answer_df = pd.read_csv(test_answer_file_path)
# 提取malfunction列，确认其存在并有适当的值
if 'malfunction' not in test_answer_df.columns:
    raise ValueError("测试答案文件中必须包含 'malfunction' 列")

# 数据标准化
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 遍历多个 contamination 值以寻找最佳准确率
contamination_values = np.linspace(0.15, 0.15, 1)  # 使用单个选项
best_accuracy = 0
best_contamination = 0

# 存储每个 contamination 对应的准确率用于输出
accuracy_list = []

for contamination in contamination_values:
    # 创建 Isolation Forest 模型
    model = IsolationForest(contamination=contamination, random_state=42)

    # 训练模型
    model.fit(X_train_scaled)

    # 预测结果
    y_train_pred = model.predict(X_train_scaled)

    # 将预测结果转换为0和1（-1表示异常，1表示正常）
    y_train_pred = [1 if x == -1 else 0 for x in y_train_pred]

    # 计算准确率
    accuracy = accuracy_score(labels_train, y_train_pred)
    accuracy_list.append(accuracy)

    print(f"Contamination: {contamination:.4f}, Training Accuracy: {accuracy:.4f}")

    # 找到最佳准确率
    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_contamination = contamination

# 最佳 contamination 值和对应准确率
print(f"最佳 contamination 值: {best_contamination:.2f}, 对应的训练集准确率: {best_accuracy:.4f}")

# 现在对测试集进行预测
# 使用最佳 contamination 重新训练模型
final_model = IsolationForest(contamination=best_contamination, random_state=42)
final_model.fit(X_train_scaled)

# 预测测试集
y_test_pred = final_model.predict(X_test_scaled)

# 将预测结果转换为0和1（-1表示异常，1表示正常）
y_test_pred = [1 if x == -1 else 0 for x in y_test_pred]

# 找出测试集中被标记为异常的 sensor_ID
incorrect_anomalies = sensor_IDs_test[np.array(y_test_pred) == 1]

# 输出被标记为异常的 sensor_ID
print("被标记为异常的 sensor_ID:", incorrect_anomalies)

# 创建一个 DataFrame 用于保存测试结果
results = pd.DataFrame({
    'sensor_ID': sensor_IDs_test,
    'predicted_malfunction': y_test_pred
})

# 只保留异常值和对应的 sensor_ID
incorrect_anomaly_results = results[results['predicted_malfunction'] == 1]

# 计算准确率：与 "malfunction" 为 0 的行进行比较
malfunction_zeros = test_answer_df[test_answer_df['malfunction'] == 0]['sensor_ID'].values
true_positives = set(incorrect_anomalies) & set(malfunction_zeros)

# 计算准确率（即预测正确的异常值占所有实际非异常值的比例）
accuracy_of_predictions = len(true_positives) / len(malfunction_zeros) if len(malfunction_zeros) > 0 else 0

print(f"与测试答案中malfunction为0的数据相比，模型的准确率: {accuracy_of_predictions:.4f}")

# 保存结果到 CSV 文件
output_file_path = '/Users/qian10102/PycharmProjects/PycharmProject/Main Files/Semester 2/Olypic Competition/Improved Version of AI/Malfunction Detection/results.csv'
incorrect_anomaly_results.to_csv(output_file_path, index=False)
print(f"结果已保存到 {output_file_path}")

# 绘制训练集图表并保存
plt.figure(figsize=(10, 6))
plt.scatter(X_train[:, 0], X_train[:, 1], c=y_train_pred, cmap='coolwarm', marker='o', edgecolor='k', s=50)
plt.title('2D Scatter Plot with Anomaly Detection (Train Data)', fontsize=14)
plt.xlabel('Power')
plt.ylabel('Signal Strength')
plt.colorbar(label='Predicted Malfunction (0=Normal, 1=Anomaly)')
plt.grid()
train_output_path = '/Users/qian10102/PycharmProjects/PycharmProject/Main Files/Semester 2/Olypic Competition/Improved Version of AI/Malfunction Detection/train_data_plot.png'
plt.savefig(train_output_path)
plt.close()  # 关闭当前图，以释放内存
print(f"训练集图表已保存到 {train_output_path}")

# 绘制测试集图表并保存
plt.figure(figsize=(10, 6))
plt.scatter(X_test[:, 0], X_test[:, 1], c=y_test_pred, cmap='coolwarm', marker='o', edgecolor='k', s=50)
plt.title('2D Scatter Plot with Anomaly Detection (Test Data)', fontsize=14)
plt.xlabel('Power')
plt.ylabel('Signal Strength')
plt.colorbar(label='Predicted Malfunction (0=Normal, 1=Anomaly)')
plt.grid()
test_output_path = '/Users/qian10102/PycharmProjects/PycharmProject/Main Files/Semester 2/Olypic Competition/Improved Version of AI/Malfunction Detection/test_data_plot.png'
plt.savefig(test_output_path)
plt.close()  # 关闭当前图，以释放内存
print(f"测试集图表已保存到 {test_output_path}")