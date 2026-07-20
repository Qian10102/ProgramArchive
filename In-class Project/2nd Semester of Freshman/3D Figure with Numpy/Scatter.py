import matplotlib.pyplot as plt
import numpy as np
fig = plt.figure() #创建画布
x = np.array([1, 3, 6, 7, 8, 10, 14]) #将x指定为方括号内的数组的遍历
y = np.array([2, 3, 5, 7, 15, 8, 20]) #将y指定为方括号内的数组的遍历
plt.scatter(x, y) #以x和y为坐标创建散点图
plt.show() #展示散点图