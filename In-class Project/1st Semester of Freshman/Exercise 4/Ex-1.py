import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.sans-serif'] = ['SimSong']
matplotlib.rcParams['axes.unicode_minus'] = False
data = pd.read_excel('movies.xlsx')

data.dropna(inplace=True)
data['时长'] = pd.to_numeric(data['时长'], errors='coerce')
data['评分人数'] = data['评分人数'].astype(int)

china_movies = data[data['地区'] == '中国大陆']

fig, axs = plt.subplots(4, 3, figsize=(50, 20))
fig.suptitle('电影数据可视化', fontsize=50)

axs[0, 0].hist(data['评分'], bins=10, color='skyblue', edgecolor='black')
axs[0, 0].set_title('电影评分分布')
axs[0, 0].set_xlabel('评分')
axs[0, 0].set_ylabel('频数')

data.groupby('上映年份')['评分'].mean().plot(ax=axs[0, 1], marker='o')
axs[0, 1].set_title('评分与上映年份关系')
axs[0, 1].set_xlabel('上映年份')
axs[0, 1].set_ylabel('平均评分')

director_ratings = data.groupby('导演')['评分'].mean().sort_values(ascending=False).head(10)
director_ratings.plot(kind='barh', ax=axs[1, 0], color='lightgreen')
axs[1, 0].set_title('不同导演的电影平均评分')
axs[1, 0].set_xlabel('平均评分')
axs[1, 0].set_ylabel('导演')

axs[0, 2].scatter(data['评分人数'], data['评分'], s=data['评分人数'] / 100, alpha=0.5, color='orange')
axs[0, 2].set_title('评分与评分人数的关系')
axs[0, 2].set_xlabel('评分人数')
axs[0, 2].set_ylabel('评分')

region_counts = data['地区'].value_counts()
region_counts.plot(kind='bar', ax=axs[1, 1], color='lightcoral')
axs[1, 1].set_title('不同地区电影数量分布')
axs[1, 1].set_xlabel('地区')
axs[1, 1].set_ylabel('电影数量')

top_china_movies = china_movies.nlargest(10, '评分')
top_china_movies.plot(kind='bar', x='标题', y='评分', ax=axs[1, 2], color='lightblue')
axs[1, 2].set_title('中国大陆评分前 10 名的电影')
axs[1, 2].set_xlabel('电影标题')
axs[1, 2].set_ylabel('评分')

ax4 = plt.subplot(2,1,2)
plt.pie(top_china_movies['评分人数'], labels=top_china_movies['标题'], autopct='%1.1f%%', startangle=140)
plt.suptitle('中国大陆评分前 10 名的电影')
plt.axis('equal')

axs[2, 0].axis('off')
axs[2, 1].axis('off')
axs[2, 2].axis('off')
axs[3, 0].axis('off')
axs[3, 1].axis('off')
axs[3, 2].axis('off')

plt.tight_layout(rect=[0.08, 0.08, 1, 0.95])
plt.subplots_adjust(wspace =0.5, hspace =1)
plt.show()
plt.savefig('plot.pdf')