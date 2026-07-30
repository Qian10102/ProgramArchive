import numpy as np
import matplotlib.pyplot as plt

a_vec = np.array([4, 1, 0])
b_vec = np.array([1, 2, 0])
a_plus_b = a_vec + b_vec

plt.figure(figsize=(6, 6, 6))

# 绘制向量 a
plt.quiver(0, 0, 0,
           a_vec[0], a_vec[1], a_vec[2],
           angles='xyz', scale_units='xyz', scale=1, 
           color='r', label="a")

# 绘制向量 b
plt.quiver(0, 0, 0,
           b_vec[0], b_vec[1], b_vec[2],
           angles='xyz', scale_units='xyz', scale=1, 
           color='b', label="b")

# 绘制向量 a + b
plt.quiver(0, 0, 0,
           a_plus_b[0], a_plus_b[1], a_plus_b[2],
           angles='xyz', scale_units='xyz', scale=1, 
           color='pink', label="a + b")

# 画出平行四边形的另外两条边
plt.plot([b_vec[0], a_plus_b[0]], 
         [b_vec[1], a_plus_b[1]], 
         [b_vec[2], a_plus_b[2]], 'k--')

plt.plot([a_vec[0], a_plus_b[0]], 
         [a_vec[1], a_plus_b[1]], 
         [a_vec[2], a_plus_b[2]], 'k--')

# 装饰
plt.gca().set_aspect('equal', adjustable='box')
plt.xlim(0, 5)  # 设置 x 轴范围
plt.ylim(0, 5)  # 设置 y 轴范围
plt.zlim(0, 5)  # 设置 z 轴范围
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.grid(color='gray', alpha=0.8, linestyle='-', linewidth=0.25) 

plt.legend() # 添加图例