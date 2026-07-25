import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

def read_sensor_data(csv_file='sensor_data.csv'):
    """从指定的 CSV 文件中读取传感器数据"""
    try:
        data = pd.read_csv(csv_file)
        columns = data.columns.tolist()
        data.columns = columns
        print(f"读取到的列名：{data.columns.tolist()}")

        if 'timestamp' in data.columns:
            data['timestamp'] = pd.to_datetime(data['timestamp'])

        if 'power' in data.columns and 'signal_strength' in data.columns:
            filtered_data = data[['power', 'signal_strength', 'malfunction']]
            return filtered_data
        else:
            print(f"CSV文件 {csv_file} 中缺少 'power' 或 'signal_strength' 列。现有列：{data.columns.tolist()}")
            return None
    except FileNotFoundError:
        print(f"CSV文件 {csv_file} 未找到。请检查文件路径。")
        return None

def train_maintenance_model(training_data):
    """训练维护模型"""
    training_data['needs_maintenance'] = training_data['malfunction'].copy()
    X = training_data[['power', 'signal_strength']]
    y = training_data["needs_maintenance"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"模型在训练集上的准确率: {accuracy:.2f}")
    print("分类报告:")
    print(classification_report(y_test, y_pred))
    # 特征重要性可视化
    plt.figure(figsize=(10, 6))
    feature_importance = model.feature_importances_
    features = X.columns
    sns.barplot(x=feature_importance, y=features)
    plt.title('Feature Importance for Maintenance Prediction')
    plt.xlabel('Importance Score')
    plt.ylabel('Features')
    plt.tight_layout()
    plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
    plt.close()
    # 混淆矩阵可视化
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix - Maintenance Prediction')
    plt.xlabel('Predicted Labels')
    plt.ylabel('True Labels')
    plt.tight_layout()
    plt.savefig('confusion_matrix.png', dpi=300, bbox_inches='tight')
    plt.close()
    return model, training_data

def visualize_maintenance_status(sensor_data, predictions):
    """
    可视化维护状态
    Args:
        sensor_data (pd.DataFrame): 传感器数据
        predictions (np.ndarray): 预测结果
    """
    # 1. 需要维护vs不需要维护的比例饼图
    plt.figure(figsize=(10, 6))
    maintenance_counts = pd.Series(predictions).value_counts()
    plt.pie(maintenance_counts, labels=['Normal', 'Needs Maintenance'], autopct='%1.1f%%', colors=['green', 'red'])
    plt.title('Maintenance Status Distribution')
    plt.tight_layout()
    plt.savefig('maintenance_status_pie.png', dpi=300, bbox_inches='tight')
    plt.close()
    # 2. 需要维护的设备的功率和信号强度散点图
    plt.figure(figsize=(12, 6))
    plt.scatter(
        sensor_data.loc[predictions == 1, 'power'],
        sensor_data.loc[predictions == 1, 'signal_strength'],
        color='red',
        label='Needs Maintenance'
    )
    plt.scatter(
        sensor_data.loc[predictions == 0, 'power'],
        sensor_data.loc[predictions == 0, 'signal_strength'],
        color='green',
        label='Normal'
    )
    plt.title('Power vs Signal Strength - Maintenance Classification')
    plt.xlabel('Power')
    plt.ylabel('Signal Strength')
    plt.legend()
    plt.tight_layout()
    plt.savefig('power_signal_scatter.png', dpi=300, bbox_inches='tight')
    plt.close()
    # 3. 需要维护设备的详细信息
    maintenance_devices = sensor_data[predictions == 1]
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    maintenance_devices['power'].plot(kind='box', title='Power Distribution - Maintenance Devices')
    plt.subplot(1, 2, 2)
    maintenance_devices['signal_strength'].plot(kind='box', title='Signal Strength Distribution - Maintenance Devices')
    plt.tight_layout()
    plt.savefig('maintenance_devices_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    # 打印需要维护的设备数量
    print(f"需要维护的设备数量: {sum(predictions)}")
    print(f"总设备数量: {len(predictions)}")
    print(f"需要维护的比例: {sum(predictions) / len(predictions) * 100:.2f}%")

def main_maintenance_prediction():
    """主函数，执行维护预测和可视化"""
    # 读取训练数据
    train_csv = "intervention_data.csv"
    test_csv = "intervention_data_test.csv"
    # 加载和训练模型
    sensor_data = read_sensor_data(train_csv)
    if sensor_data is not None:
        model, _ = train_maintenance_model(sensor_data.copy())
        # 加载测试数据
        test_data = read_sensor_data(test_csv)
        if test_data is not None:
            # 准备测试数据
            X_test = test_data[['power', 'signal_strength']]
            # 进行预测
            predictions = model.predict(X_test)
            # 可视化维护状态
            visualize_maintenance_status(test_data, predictions)
        else:
            print("无法加载测试数据")
    else:
        print("无法加载训练数据")

if __name__ == "__main__":
    main_maintenance_prediction()
