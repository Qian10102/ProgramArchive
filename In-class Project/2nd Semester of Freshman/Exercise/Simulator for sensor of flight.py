# 生成模拟的飞机传感器数据
import numpy as np
import pandas as pd
data_size = 1000  # 设置数据集的大小
data = pd.DataFrame({
    'Engine_RPM': np.random.normal(2000, 200, data_size),  # 引擎转速（RPM）
    'Throttle_Position': np.random.normal(50, 10, data_size),  # 油门位置（%）
    'Fuel_Flow': np.random.normal(150, 20, data_size),  # 燃油流量（L/h）
    'Engine_Temperature': np.random.normal(200, 10, data_size),  # 发动机温度（℃）
    'Airspeed': np.random.normal(500, 50, data_size),  # 空速（km/h）
    'Altitude': np.random.normal(10000, 1000, data_size)  # 高度（m）
})
# 查看数据的前五行，确保数据格式正确
data.head()

# 导入train_test_split库
from sklearn.model_selection import train_test_split
# 将数据集划分为训练集、测试集和验证集
train_data, temp_data = train_test_split(data, test_size=0.3, random_state=42)  # 70%训练集，30%暂时数据集
test_data, val_data = train_test_split(temp_data, test_size=0.33, random_state=42)  # 33%的验证集，剩下是测试集
# 查看划分后数据集的大小
print(f'Training data size: {train_data.shape[0]}')
print(f'Test data size: {test_data.shape[0]}')
print(f'Validation data size: {val_data.shape[0]}')
# 保存划分后的数据集到CSV文件 读取文件 train_data.csv  test_data.csv val_data.csv
train_data.to_csv('train', index=False)
test_data.to_csv('test', index=False)
val_data.to_csv('val', index=False)

# 导入StandardScaler库
from sklearn.preprocessing import StandardScaler
# 加载数据集  读取文件 train_data.csv  test_data.csv val_data.csv
train_data = pd.read_csv('train')
test_data = pd.read_csv('test')
val_data = pd.read_csv('val')
# 标准化处理数据，使得不同特征具有相同的量纲
scaler = StandardScaler()
train_data_scaled = scaler.fit_transform(train_data)  #
test_data_scaled = scaler.transform(test_data)  # 测试集标准化
val_data_scaled = scaler.transform(val_data)  # 验证集标准化
# 查看标准化后的数据（前五行）
pd.DataFrame(train_data_scaled, columns=train_data.columns).head()

# 导入KMeans库
from sklearn.cluster import KMeans
# 构建K-means模型，设置聚类数量为3（可以调整为不同的K值） 调用KMeans
kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
# 训练模型  输入训练集标准化后的数据
kmeans.fit(train_data_scaled)
# 输出聚类中心（即每个簇的中心位置）
print(f'聚类中心:\n{kmeans.cluster_centers_}')
# 导入KMeans库
from sklearn.cluster import KMeans
# 构建K-means模型，设置聚类数量为3（可以调整为不同的K值） 调用KMeans
kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
# 训练模型  输入训练集标准化后的数据
kmeans.fit(train_data_scaled)
# 输出聚类中心（即每个簇的中心位置）
print(f'聚类中心:\n{kmeans.cluster_centers_}')

# 导入silhouette_score库
from sklearn.metrics import silhouette_score
# 使用轮廓系数来评估模型效果，值越接近1，聚类效果越好
silhouette_avg = silhouette_score(test_data_scaled, kmeans.predict(test_data_scaled))
print(f'轮廓系数 (Silhouette Score): {silhouette_avg:.4f}')

# 导入matplotlib.pyplot库用于绘图
import matplotlib.pyplot as plt
# 使用肘部法则（Elbow Method）来选择最佳的K值
wcss = []  # 存储不同K值对应的WCSS（Within-Cluster Sum of Squares）
for i in range(1, 16):  # 从1到15测试不同的K值
    kmeans = KMeans(n_clusters=i, random_state=42, n_init='auto')
    #输入训练集标准化后的数据
    kmeans.fit(train_data_scaled)
    wcss.append(kmeans.inertia_)  # inertia_是WCSS
# 绘制肘部法则图
plt.plot(range(1, 16), wcss)
plt.title('Elbow Method')
plt.xlabel('K')
plt.ylabel('WCSS')
plt.show()
# 解释：可以观察图中K值变化对WCSS的影响。随着K值增加，WCSS会持续下降，
# 但当K值达到某个点后，WCSS下降的速度会减缓，形成一个肘部。
# 这个K值就是我们选择的最佳聚类数。肘部代表着进一步增加K值的收益逐渐变小。

# 使用K-means++初始化方法来优化聚类初始中心的选择
kmeans_plus = KMeans(n_clusters=7, init='k-means++', random_state=42, n_init='auto')
kmeans_plus.fit(train_data_scaled)
# 输出使用K-means++初始化后的聚类中心
print(f'K-means++初始化后的聚类中心:\n{kmeans_plus.cluster_centers_}')
# 解释：与传统的随机选择K个初始中心的方法相比，K-means++通过更智能的选择初始化中心，
# 从而通常能够得到更好的聚类结果，尤其是在数据分布不均的情况下。

# 导入pairwise_distances库，用于计算不同的距离度量
from sklearn.metrics import pairwise_distances
# 使用曼哈顿距离（Manhattan Distance）
kmeans_manhattan = KMeans(n_clusters=7, random_state=42, n_init='auto')
kmeans_manhattan.fit(pairwise_distances(train_data_scaled, metric='manhattan'))
# 输出曼哈顿距离下的聚类中心
print(f'使用曼哈顿距离的聚类中心:\n{kmeans_manhattan.cluster_centers_}')
# 解释：K-means算法通常使用欧氏距离来衡量数据点之间的相似度，但不同的距离度量方法（如欧氏距离、曼哈顿距离）
# 适用于不同的数据类型。在欧氏空间中，欧氏距离是最常用的度量方法，但对于某些数据（如离散数据、稀疏数据等），
# 曼哈顿距离可能更合适。选择适当的距离度量方法对于提高聚类效果至关重要。

# 导入SelectKBest和f_classif库用于特征选择
from sklearn.feature_selection import SelectKBest, f_classif
# 使用SelectKBest方法选择对聚类效果影响最大的特征
selector = SelectKBest(score_func=f_classif, k=3)  # 选择最重要的3个特征
train_data_selected = selector.fit_transform(train_data_scaled, kmeans.labels_)
# 输出选择的特征和训练后的模型聚类中心
print(f'选择的特征:\n{selector.get_support(indices=True)}')
kmeans_features = KMeans(n_clusters=7, random_state=42, n_init='auto')
kmeans_features.fit(train_data_selected)
# 输出优化后的聚类中心
print(f'优化后聚类中心:\n{kmeans_features.cluster_centers_}')
# 解释：特征选择是优化机器学习模型的重要步骤。在聚类问题中，选择对类别划分最有影响的特征
# 可以帮助我们提高模型的聚类效果。通过使用SelectKBest方法，我们可以通过计算特征与聚类标签之间的关系
# 来选择最重要的特征，从而去除冗余的或无关的特征，减少计算复杂度，并提高模型的性能。