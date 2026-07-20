import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_boston
# 加载波士顿房价数据集
boston = load_boston()
# 创建DataFrame
boston_df = pd.DataFrame(data=boston.data, columns=boston.feature_names)
boston_df['PRICE'] = boston.target  # 添加房价作为目标变量
# 显示数据的前5行
print(boston_df.head())
# 检查缺失值
print(boston_df.isnull().sum())
# 通过IQR方法清除异常值（如RM和AGE列）
Q1 = boston_df[['RM', 'AGE']].quantile(0.25)
Q3 = boston_df[['RM', 'AGE']].quantile(0.75)
IQR = Q3 - Q1
filtered_df = boston_df[~((boston_df[['RM', 'AGE']] < (Q1 - 1.5 * IQR)) | (boston_df[['RM', 'AGE']] > (Q3 + 1.5 * IQR))).any(axis=1)]
# 标准化处理数值型特征
# 1. 选择需要标准化的特征（不包括 'AGE', 'CRIM', 'ZN'，'RM'）
features_to_scale = ['INDUS', 'CHAS', 'NOX', 'DIS', 'RAD', 'TAX', 'PTRATIO','B', 'LSTAT']

# 2. 标准化处理选定的数值型特征
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()

# 将这些特征进行标准化
scaled_features = scaler.fit_transform(filtered_df[features_to_scale])

# 将标准化后的特征与原数据合并
scaled_df = pd.DataFrame(scaled_features, columns=features_to_scale)

# 将目标变量（'PRICE'）和不需要标准化的特征合并回去
scaled_df['PRICE'] = filtered_df['PRICE'].reset_index(drop=True)
scaled_df['AGE'] = filtered_df['AGE'].reset_index(drop=True)
scaled_df['CRIM'] = filtered_df['CRIM'].reset_index(drop=True)
scaled_df['ZN'] = filtered_df['ZN'].reset_index(drop=True)
scaled_df['RM'] = filtered_df['RM'].reset_index(drop=True)
# 查看标准化后的数据框
print(scaled_df.head())
# 删除与房价无关的特征（如'TAX'和'RAD'）
scaled_df.drop(columns=['TAX', 'RAD'], inplace=True)
# 将房价分为低、中、高三类
bins = [0, 20, 40, np.inf]
labels = ['Low', 'Medium', 'High']
scaled_df['PRICE_Category'] = pd.cut(scaled_df['PRICE'], bins=bins, labels=labels)
print(scaled_df[['PRICE', 'PRICE_Category']].head())
# 按房价分类分组，查看每类的平均特征值
grouped = scaled_df.groupby('PRICE_Category').agg('mean')
print(grouped)
# 创建透视表，计算不同CRIM和ZN值下的平均房价
pivot_table = pd.pivot_table(scaled_df, values='PRICE', index='CRIM', columns='ZN', aggfunc='mean')
print(pivot_table)
# 查看 'AGE' 和 'CRIM' 列的基本统计信息
print(scaled_df[['AGE', 'CRIM']].describe())
# 筛选出年龄大于 60 且 CRIM 值小于 1 的数据
filtered_data = scaled_df[(scaled_df['AGE'] > 60) & (scaled_df['CRIM'] < 1)]
# 显示筛选后的数据
print(filtered_data)
# 1. 绘制房价分布
sns.histplot(scaled_df['PRICE'], kde=True)
plt.title('Distribution of Prices')
plt.show()
# 2. 绘制每个房价分类的特征分布
sns.boxplot(x='PRICE_Category', y='CRIM', data=scaled_df)
plt.title('CRIM Distribution by Price Category')
plt.show()
# 3. 绘制房价与房间数量(RM)的关系
sns.scatterplot(x='RM', y='PRICE', data=scaled_df)
plt.title('Price vs RM')
plt.show()