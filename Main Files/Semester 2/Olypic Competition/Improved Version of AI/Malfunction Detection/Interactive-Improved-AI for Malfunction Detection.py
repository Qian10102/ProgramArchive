import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.metrics import accuracy_score


def load_data_from_csv(file_path, load_labels=False):
    df = pd.read_csv(file_path)
    required_columns = ['power', 'signal_strength']
    if not all(col in df.columns for col in required_columns):
        raise ValueError("CSV 文件中必须包含 'power' 和 'signal_strength' 列")
    X = df[['power', 'signal_strength']].values
    sensor_IDs = np.arange(1, len(df) + 1)
    labels = df['malfunction'].values if load_labels and 'malfunction' in df.columns else None
    if load_labels and labels is not None:
        return X, sensor_IDs, labels
    return X, sensor_IDs


def train_isolation_forest(X_train, labels_train, contamination):
    model = IsolationForest(contamination=contamination, random_state=42)
    model.fit(X_train)
    y_train_pred = model.predict(X_train)
    return [1 if x == -1 else 0 for x in y_train_pred], model

def plot_data(X, y_pred, title, sensor_IDs=None):
    # 创建 DataFrame 以用于 plotly 绘图
    data = pd.DataFrame(X, columns=['Power', 'Signal Strength'])
    data['Predicted Malfunction'] = y_pred
    data['Sensor ID'] = sensor_IDs
    # 添加一个新的列来显示状态信息
    data['Status'] = np.where(data['Predicted Malfunction'] == 1, 'Faulty', 'Normal')
    # 创建 plotly 散点图
    fig = px.scatter(data_frame=data,
                     x='Power',
                     y='Signal Strength',
                     color='Predicted Malfunction',
                     hover_name='Sensor ID',  # 传感器 ID
                     hover_data={'Sensor ID': True, 'Status': True},  # 显示传感器 ID 和状态
                     title=title,
                     color_continuous_scale=px.colors.sequential.Viridis)
    # 设置标题的居中对齐
    fig.update_layout(title_text=title, title_x=0.5)
    # 显示图表
    fig.show()

def calculate_accuracy(true_labels, predictions):
    if len(true_labels) == 0:
        return 0
    return np.sum(true_labels == predictions) / len(true_labels)

def main():
    train_file_path = 'train_data.csv'
    test_file_path = 'test_data.csv'
    test_answer_file_path = 'test_data_answer.csv'
    # 加载训练和测试数据
    X_train, sensor_IDs_train, labels_train = load_data_from_csv(train_file_path, load_labels=True)
    X_test, sensor_IDs_test = load_data_from_csv(test_file_path)
    test_answer_df = pd.read_csv(test_answer_file_path)
    # 检查测试答案的格式
    if 'malfunction' not in test_answer_df.columns:
        raise ValueError("测试答案文件中必须包含 'malfunction' 列")
    # 标准化数据
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    # 设置污染值
    contamination_values = np.linspace(0.09, 0.09, 1)
    best_accuracy = 0
    best_model = None
    # 训练模型并选择最佳准确性
    for contamination in contamination_values:
        y_train_pred, model = train_isolation_forest(X_train_scaled, labels_train, contamination)
        masked_labels_train = labels_train[labels_train == 1]
        masked_predictions = [y for y, label in zip(y_train_pred, labels_train) if label == 1]
        # 计算准确率
        accuracy = calculate_accuracy(masked_labels_train, masked_predictions)
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_model = model
    print(f"最佳 contamination 值: {contamination:.2f}, 对应的训练集准确率: {best_accuracy:.4f}")
    # 预测测试集
    y_test_pred = best_model.predict(X_test_scaled)
    y_test_pred = [1 if x == -1 else 0 for x in y_test_pred]
    # 构建结果 DataFrame
    results = pd.DataFrame({'sensor_ID': sensor_IDs_test, 'predicted_malfunction': y_test_pred})
    correct_anomaly_results = results[results['predicted_malfunction'] == 1]
    # 创建全零的真实标签数组以保持与测试数据的长度一致
    true_labels = np.zeros(len(sensor_IDs_test), dtype=int)
    # 将故障标记为1, 确保只有真实故障的ID对应675为1
    true_labels[test_answer_df['malfunction'] == 1] = 1
    # 获取真实的故障 ID 列
    malfunction_ones = test_answer_df[test_answer_df['malfunction'] == 1]['sensor_ID'].values
    print("实际故障的 sensor_ID:", malfunction_ones)
    print("模型预测的异常 sensor_ID:", correct_anomaly_results['sensor_ID'].values)
    # 获取预测异常值的 sensor_ID
    predicted_anomalies = correct_anomaly_results['sensor_ID'].values
    # 使用预测与真实标签构建相应的数组
    predicted_labels = np.zeros(len(sensor_IDs_test))
    predicted_labels[np.isin(sensor_IDs_test, predicted_anomalies)] = 1
    # 计算准确率
    accuracy_of_predictions = accuracy_score(true_labels, predicted_labels)
    print(f"与测试答案中 malfunction 为 1 的数据相比，模型的准确率: {accuracy_of_predictions:.4f}")
    # 保存结果
    output_file_path = 'results.csv'
    correct_anomaly_results.to_csv(output_file_path, index=False)
    print(f"结果已保存到 {output_file_path}")
    # 绘制结果
    plot_data(X_train, y_train_pred, title="Prediction for training data", sensor_IDs=sensor_IDs_train)
    plot_data(X_test, y_test_pred, title="Prediction for testing data", sensor_IDs=sensor_IDs_test)

# 运行主函数
if __name__ == "__main__":
    main()