import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 设置时间范围（假设t表示时间）
time_values = np.linspace(0, 2*np.pi, 100)  # 从0到2π，模拟一圈运动
# 椭圆轨道参数
a = 2.0  # 半长轴
e = 0.2  # 偏心率（0 < e < 1 表示椭圆）
# 计算行星的极坐标
r_values = a * (1 - e**2) / (1 + e * np.cos(time_values))  # 极坐标方程
# 转换为笛卡尔坐标
x_values = r_values * np.cos(time_values)
y_values = r_values * np.sin(time_values)
# 定义 z(t) 为正弦 + 线性函数，模拟三维空间运动
z_values = np.sin(time_values) + 0.1 * time_values  # z轴变化：起伏并逐渐增加
# 创建数据框
data = pd.DataFrame({
    'time': time_values,
    'x': x_values,
    'y': y_values,
    'z': z_values
})
# 保存为CSV文件
data.to_csv('planet_motion_data.csv', index=False)
print("数据集已保存为 'planet_motion_data.csv'")
# 绘制轨迹图
fig = plt.figure(figsize=(8,8)) #创建一个8*8的画布
ax = fig.add_subplot(projection = "3d")    # 创建一个3D坐标轴
ax.plot(x_values, y_values, z_values, label='Planetary Trajectory')
ax.set_xlabel('X Position')
ax.set_ylabel('Y Position')
ax.set_title('Planetary Orbit in 3D Space')
ax.legend()  #显示图例
plt.show()   #显示图形

# 导入train_test_split模块，用于数据划分
from sklearn.model_selection import train_test_split
# 加载数据集
data = pd.read_csv("planet_motion_data.csv")
# 使用train_test_split将数据集划分为训练集和测试集，80%训练集，20%测试集
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)
# 从训练集中进一步划分出验证集，60%训练集，20%验证集
train_data, val_data = train_test_split(train_data, test_size=0.25, random_state=42)
# 显示数据集划分后的大小
print(f"Training data size: {len(train_data)}")
print(f"Validation data size: {len(val_data)}")
print(f"Test data size: {len(test_data)}")

# 导入StandardScaler用于数据标准化
from sklearn.preprocessing import StandardScaler
# 导入多项式回归模型
from sklearn.preprocessing import PolynomialFeatures
# 数据标准化与多项式特征转换
features = train_data[['time']]  # 选择时间作为特征
labels = train_data[['x', 'y', 'z']]  # 选择位置（x, y, z）作为标签
scaler = StandardScaler()  # 初始化标准化对象
features_scaled = scaler.fit_transform(features)  # 对时间特征进行标准化
# 使用多项式特征转换，设置多项式的度数为3
poly = PolynomialFeatures(degree=3)
features_poly = poly.fit_transform(features_scaled)  # 转换为多项式特征

# 导入线性回归模型
from sklearn.linear_model import LinearRegression
# 初始化线性回归模型
model = LinearRegression()
# 使用多项式特征训练模型
model.fit(features_poly, labels)
# 输出模型的参数
print(f"模型的截距：{model.intercept_}")
print(f"模型的系数：{model.coef_}")

# 使用训练好的模型预测行星的三维位置
time_series = pd.DataFrame(np.linspace(0, 2 * np.pi, 100).reshape(-1, 1), columns=['time'])  # 创建一个新的时间序列
time_series_scaled = scaler.transform(time_series)  # 对时间序列进行标准化
time_series_poly = poly.transform(time_series_scaled)  # 转换为多项式特征
predicted_positions = model.predict(time_series_poly)  # 预测位置
#  绘制三维轨迹图
fig = plt.figure(figsize=(8,8))   #创建一个8*8的画布
ax = fig.add_subplot(111, projection = "3d") # 创建一个3D坐标轴
# 绘制预测的轨迹
ax.plot(predicted_positions[:, 0], predicted_positions[:, 1], predicted_positions[:, 2], label='Predicted Trajectory')
# 绘制实际轨迹
ax.scatter(labels['x'], labels['y'], labels['z'], color='red', label='Actual Positions')
# 设置坐标轴标签
ax.set_xlabel('X Position')
ax.set_ylabel('Y Position')
ax.set_title('Planet Trajectory in 3D Space')
# 显示图例
ax.legend()
# 显示图形
plt.show()

# 导入用于评估的指标
from sklearn.metrics import mean_squared_error, r2_score
# 验证集评估
val_features_scaled = scaler.transform(val_data[['time']])  # 标准化验证集特征
val_features_poly = poly.transform(val_features_scaled)  # 转换为多项式特征
val_labels = val_data[['x', 'y', 'z']]  # 验证集标签
val_predictions = model.predict(val_features_poly)  # 预测验证集的位置
val_mse = mean_squared_error(val_labels, val_predictions)  # 计算均方误差
val_r2 = r2_score(val_labels, val_predictions)  # 计算R²得分
print(f'Validation MSE: {val_mse:.4f}')
print(f'Validation R²: {val_r2:.4f}')

# 导入用于岭回归的Ridge模型
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV
param_grid = {
    'poly__degree': [3, 4, 5],  # 多项式的度数范围
    'ridge__alpha': [0.01, 0.1, 1]  # 正则化参数范围
}
# 使用管道（Pipeline）将多项式特征转换与岭回归结合
from sklearn.pipeline import Pipeline
pipe = Pipeline([
    ('poly', PolynomialFeatures()),  # 多项式特征转换
    ('scaler', StandardScaler()),  # 数据标准化
    ('ridge', Ridge())  # 岭回归模型
])
# 设置GridSearchCV优化超参数
grid_search = GridSearchCV(pipe, param_grid, cv=5, scoring='neg_mean_squared_error')
# 使用交叉验证找到最佳超参数
grid_search.fit(features, labels)
# 输出最佳超参数组合
best_params = grid_search.best_params_
print(f"最佳超参数：{best_params}")
# 获取最佳的多项式度数和正则化参数
best_degree = best_params['poly__degree']
best_alpha = best_params['ridge__alpha']
# 使用找到的最佳超参数重新训练模型
best_pipe = Pipeline([
    ('poly', PolynomialFeatures(degree=best_degree)),
    ('scaler', StandardScaler()),
    ('ridge', Ridge(alpha=best_alpha))
])
best_pipe.fit(features, labels)
# 预测新的时间序列数据
time_series = pd.DataFrame(np.linspace(0, 2 * np.pi, 100).reshape(-1, 1), columns=['time'])  # 创建新的时间序列
time_series_scaled = scaler.transform(time_series)  # 对时间序列进行标准化
time_series_poly = poly.fit_transform(time_series_scaled)  # 转换为多项式特征
val_predictions = best_pipe.predict(val_data[['time']])  # 进行预测
val_mse = mean_squared_error(val_labels, val_predictions)  # 计算均方误差（MSE）
val_r2 = r2_score(val_labels, val_predictions)  # 计算R²得分，衡量模型拟合的好坏
# 输出验证集的评估结果
print(f'Validation MSE: {val_mse:.4f}')
print(f'Validation R²: {val_r2:.4f}')
# 测试集评估
test_features_scaled = scaler.transform(test_data[['time']])  # 对测试集特征进行标准化
test_features_poly = poly.transform(test_features_scaled)  # 转换为多项式特征
test_labels = test_data[['x', 'y', 'z']]  # 获取测试集的标签
test_predictions = best_pipe.predict(test_data[['time']])  # 进行预测
test_mse = mean_squared_error(test_labels, test_predictions)  # 计算均方误差（MSE）
test_r2 = r2_score(test_labels, test_predictions)  # 计算R²得分
# 输出测试集的评估结果
print(f'Test MSE: {test_mse:.4f}')
print(f'Test R²: {test_r2:.4f}')