import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

def generate_random_dataset(num_samples):
    """生成随机数据集"""
    np.random.seed(42)  # 设置随机种子以确保结果可重现
    data = {
        'voltage': np.random.uniform(2.5, 3.5, num_samples),  # 电压范围
        'current': np.random.uniform(0.3, 1.0, num_samples),  # 电流范围
        'signal_strength': np.random.uniform(-100, -50, num_samples),  # 信号强度范围
        'response_frequency': np.random.uniform(4.0, 5.5, num_samples),  # 响应频率范围
        'needs_maintenance': np.random.choice([0, 1], num_samples, p=[0.7, 0.3])  # 创建维护需求标签，70%正常，30%需要维护
    }
    return pd.DataFrame(data)

def train_maintenance_model(training_data):
    """训练维护模型"""
    # 特征选择
    X = training_data[["voltage", "current", "signal_strength", "response_frequency"]]
    y = training_data["needs_maintenance"]  # 0=正常, 1=需要维护
    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # 初始化并训练模型
    model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
    model.fit(X_train, y_train)
    # 评估模型
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"模型准确率: {accuracy:.2f}")
    print("分类报告:")
    print(classification_report(y_test, y_pred))
    return model

def predict_maintenance(model, new_data):
    """预测新数据是否需要维护"""
    predictions = model.predict(new_data)
    return predictions

# 示例用法
if __name__ == "__main__":
    # 生成随机数据集
    num_samples = 5000  # 数据样本数量
    training_data = generate_random_dataset(num_samples)
    # 训练模型
    model = train_maintenance_model(training_data)
    # 假设 new_data 是一个新的 DataFrame，包含待预测的数据
    new_data = pd.DataFrame({
        'voltage': [3.2, 2.9, 3.1, 3.3],
        'current': [0.5, 0.3, 0.6, 0.4],
        'signal_strength': [-60, -95, -70, -65],
        'response_frequency': [5.1, 4.1, 4.8, 5.0]
    })
    # 进行预测
    predictions = predict_maintenance(model, new_data)
    print("预测结果:", predictions)
