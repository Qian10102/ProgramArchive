import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

def generate_random_dataset(num_samples):
    """生成随机数据集"""
    np.random.seed(42)  # 设置随机种子以确保结果可重现
    data = {
        'voltage': np.random.uniform(2.75, 3.25, num_samples),  # 电压范围
        'current': np.random.uniform(3e-4,4e-4 , num_samples),  # 电流范围
        'signal_strength': np.random.uniform(-80, -50, num_samples),  # 信号强度范围
        'response_frequency': np.random.uniform(2.14e13, 3.75e13, num_samples),  # 响应频率范围
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
    # 绘制特征重要性图
    plt.figure(figsize=(10, 6))
    sns.barplot(x=model.feature_importances_, y=X.columns)
    plt.title('Feature Importance')
    plt.xlabel('Importance')
    plt.ylabel('Feature')
    plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
    plt.close()
    # 绘制混淆矩阵
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted Labels')
    plt.ylabel('True Labels')
    plt.savefig('confusion_matrix.png', dpi=300, bbox_inches='tight')
    plt.close()
    return model

def visualize_data_distribution(training_data):
    """可视化数据分布"""
    plt.figure(figsize=(12, 8))
    for idx, feature in enumerate(training_data.drop('needs_maintenance', axis=1).columns):
        plt.subplot(2, 2, idx + 1)
        sns.kdeplot(data=training_data, x=feature, hue='needs_maintenance', fill=True)
        plt.title(f'Distribution of {feature}')
        plt.xlabel('Value')
        plt.ylabel('Density')
    plt.tight_layout()
    plt.savefig('data_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()

def predict_maintenance(model, new_data):
    """预测新数据是否需要维护"""
    predictions = model.predict(new_data)
    return predictions

def visualize_predictions(new_data, predictions):
    """可视化预测结果"""
    plt.figure(figsize=(10, 6))
    sns.countplot(x=predictions)
    plt.title('Prediction Results')
    plt.xlabel('Prediction')
    plt.ylabel('Count')
    plt.savefig('prediction_results.png', dpi=300, bbox_inches='tight')
    plt.close()

# 示例用法
if __name__ == "__main__":
    # 生成随机数据集
    num_samples = 5000  # 数据样本数量
    training_data = generate_random_dataset(num_samples)
    # 可视化数据分布
    visualize_data_distribution(training_data)
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
    # 可视化预测结果
    visualize_predictions(new_data, predictions)