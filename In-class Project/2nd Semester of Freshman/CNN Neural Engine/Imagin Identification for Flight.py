import os
import pandas as pd
import zipfile
import random
from torch.utils.data import Dataset
from torchvision import transforms
from PIL import Image

# 定义压缩文件路径和目标文件夹路径
zip_path = 'fgvc-aircraft-2013b-subset.zip'
extract_folder = 'fgvc-aircraft-2013b-subset'
# 创建目标文件夹（如果不存在）
if not os.path.exists(extract_folder):
    os.makedirs(extract_folder)
# 解压文件
(f = zipfile.ZipFile(zip_path,'r'))
f.extractall(extract_folder)
print(f"文件已解压到 {extract_folder} 文件夹中。")
# 定义标签文件路径
label_file = "fgvc-aircraft-2013b-subset/labels.txt"
# 读取标签文件
labels = []
with open(label_file, 'r') as file:
    for line in file:
        parts = line.strip().split()  # 按空格拆分
        if len(parts) >= 2:  # 确保每行至少有两个字段
            image_name = parts[0]  # 第一个部分是图片名
            label = " ".join(parts[1:])  # 后续部分合并为标签
            labels.append([image_name, label])
        else:
            print(f"Warning: Skipping malformed line: {line.strip()}")
# 将标签转换为DataFrame
labels = pd.DataFrame(labels, columns=['image_id', 'label'])
print("原始标签文件内容：")
print(labels.head())
# 定义图片文件夹路径
data_dir = "fgvc-aircraft-2013b-subset/data"
# 获取所有图片文件名
image_files = [f for f in os.listdir(data_dir) if f.endswith(".jpg")]
print(f"找到 {len(image_files)} 张图片")
# 创建一个字典，用于存储图片编号和飞机类型的映射
image_to_label = dict(zip(labels["image_id"], labels["label"]))
# 检查每张图片是否在标签文件中
matched_images = []
for image_file in image_files:
    image_id = image_file.split(".")[0]  # 去掉文件扩展名，获取图片编号
    if image_id in image_to_label:
        matched_images.append((image_id, image_to_label[image_id]))
    else:
        print(f"警告：图片 {image_file} 没有对应的标签")
print(f"匹配到 {len(matched_images)} 张图片")
# 创建一个新的文件夹，用于保存重命名后的图片
new_data_dir = "fgvc-aircraft-2013b-subset/renamed_data"
os.makedirs(new_data_dir, exist_ok=True)
# 生成新的编号（从 001 开始）
new_labels = []
for idx, (image_id, label) in enumerate(matched_images):
    new_image_id = f"{idx + 1:03d}"  # 生成三位数的编号，如 001, 002, ...
    old_image_path = os.path.join(data_dir, f"{image_id}.jpg")  # 旧图片路径
    new_image_path = os.path.join(new_data_dir, f"{new_image_id}.jpg")  # 新图片路径
    os.rename(old_image_path, new_image_path)  # 重命名图片
    new_labels.append((new_image_id, label))  # 保存新的标签
# 将新的标签保存到文件
new_label_file = os.path.join(new_data_dir, "label.txt")
with open(new_label_file, "w") as f:
    for new_image_id, label in new_labels:
        f.write(f"{new_image_id} {label}\n")
print("图片重命名完成，新的标签文件已保存")
# 打印新的标签文件内容
with open(new_label_file, "r") as f:
    print("新的标签文件内容：")
    print(f.read())

# 定义标签映射
label_map = {
    'Cessna Citation': 0,
    'ATR-72': 1,
    'Saab 340': 2,
    'Embraer Legacy 600': 3,
    'Fokker 100': 4,
    'MD-90': 5,
    'Boeing 757': 6,
    'Metroliner': 7,
    'A340': 8,
    'A320': 9
}
# 定义新的标签文件路径
new_label_file = "fgvc-aircraft-2013b-subset/renamed_data/label.txt"
# 读取新的标签文件
with open(new_label_file, "r") as f:
    lines = f.readlines()
    new_labels = []
    for line in lines:
        # 将每行内容拆分为图片编号和标签名称
        parts = line.strip().split(" ")
        image_id = parts[0]  # 图片编号
        label_name = " ".join(parts[1:])  # 标签名称（可能包含多个空格）
        new_labels.append((image_id, label_name))  # 添加到标签列表
print("新的标签文件内容：")
print(new_labels[:5])  # 打印前 5 行标签数据
# 定义自定义数据集类
class AircraftDataset(Dataset):
    def __init__(self, data_dir, labels, label_map, transform=None):
        self.data_dir = data_dir  # 图像文件夹路径
        self.labels = labels  # 标签数据（列表形式）
        self.label_map = label_map  # 标签映射
        self.transform = transform  # 图像预处理方法
    def __len__(self):
        return len(self.labels)  # 返回数据集的大小
    def __getitem__(self, idx):
        image_id, label_name = self.labels[idx]  # 获取图片编号和标签名称
        img_name = os.path.join(self.data_dir, image_id + ".jpg")  # 获取图像路径
        image = Image.open(img_name).convert("RGB")  # 加载图像并转换为 RGB 格式
        label = self.label_map[label_name]  # 将标签名称转换为数字编号
        if self.transform:
            image = self.transform(image)  # 对图像进行预处理
        return image, label  # 返回图像和标签
# 定义图像预处理方法
transform = transforms.Compose([
    transforms.Resize((128, 128)),  # 将图像调整为 128x128 大小
    transforms.ToTensor(),  # 将图像转换为张量
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # 归一化
])
# 定义新的图片文件夹路径
new_data_dir = "fgvc-aircraft-2013b-subset/renamed_data"
# 创建数据集实例
dataset = AircraftDataset(new_data_dir, new_labels, label_map, transform=transform)
# 打印数据集大小
print(f"数据集大小：{len(dataset)}")
# 检查数据集中的第一张图片和标签
image, label = dataset[0]
print(f"图像形状：{image.shape}")  # 打印图像形状
print(f"标签：{label}")  # 打印标签

# 导入 PyTorch 的数据集划分工具
from torch.utils.data import random_split
# 导入 PyTorch 的数据加载器模块
from torch.utils.data import DataLoader
# 导入以下库设置随机数种子，以确保实验的可重复性
import numpy as np
import random
import torch
# 计算训练集、验证集和测试集的大小
total_size = len(dataset)  # 数据集总大小
train_size = int(0.7 * total_size)  # 训练集占 70%
val_size = int(0.2 * total_size)  # 验证集占 20%
test_size = total_size - train_size - val_size  # 测试集占 10%
# 定义图像预处理方法
transform = transforms.Compose([
    transforms.Resize((128, 128)),  # 将图像调整为 128x128 大小
    transforms.RandomRotation(10),  # 随机旋转图像，旋转角度范围为[-10, 10]度
    transforms.RandomHorizontalFlip(),  # 随机水平翻转图像
    transforms.ToTensor(),  # 将图像转换为张量
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # 归一化
])
# 创建数据集实例
dataset = AircraftDataset(new_data_dir, new_labels, label_map, transform=transform)
# 使用 random_split 划分数据集
train_dataset, val_dataset, test_dataset = random_split(dataset, [train_size, val_size, test_size])
# 创建训练集、验证集和测试集的数据加载器
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)  # 训练集，批量大小为 32，打乱数据顺序
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)  # 验证集，批量大小为 32，不打乱数据顺序
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)  # 测试集，批量大小为 32，不打乱数据顺序

import torchvision.models as models
import torch.nn as nn
import torch.optim as optim
# 检测设备类型
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"当前设备: {device}")
# 定义 ResNet18 模型
model = models.resnet18(weights=None)  # 使用预训练的 ResNet18
model.load_state_dict(torch.load('resnet18-f37072fd.pth', weights_only=True),strict=True)
model.fc = nn.Linear(model.fc.in_features, 10)  # 修改最后一层，适应本实验的 10 个类别
model = model.to(device)  # 将模型移动到设备上

# 检测设备类型
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"当前设备: {device}")
# 将模型移动到设备上
model = model.to(device)
# 定义损失函数：交叉熵损失，用于分类任务
criterion = nn.CrossEntropyLoss()
# 定义优化器：Adam 优化器，学习率为 0.0001
optimizer = optim.Adam(model.parameters(), lr=0.0001, weight_decay=1e-4)
# 打印损失函数和优化器信息
print("损失函数：", criterion)
print("优化器：", optimizer)
# 初始化列表，用于记录训练和验证的损失和准确率
train_losses = []
train_accuracies = []
val_losses = []
val_accuracies = []
# 训练模型
num_epochs = 50  # 训练轮数
for epoch in range(num_epochs):
    model.train()  # 将模型设置为训练模式
    train_loss = 0.0  # 训练损失
    train_correct = 0  # 训练集正确预测的样本数
    train_total = 0  # 训练集总样本数
    for images, labels in train_loader:
        # 将数据移动到设备上
        images = images.to(device)
        labels = labels.to(device)
        # 前向传播：计算模型输出
        outputs = model(images)
        # 计算损失
        loss = criterion(outputs, labels)
        # 反向传播：计算梯度
        optimizer.zero_grad()  # 清空梯度
        loss.backward()  # 反向传播
        optimizer.step()  # 更新参数
        train_loss += loss.item()  # 累加损失
        # 获取预测类别
        _, predicted = torch.max(outputs.data, 1)
        # 统计正确预测的样本数
        train_total += labels.size(0)
        train_correct += (predicted == labels).sum().item()
    # 计算训练集的平均损失和准确率
    train_loss_avg = train_loss / len(train_loader)
    train_acc = 100 * train_correct / train_total
    train_losses.append(train_loss_avg)
    train_accuracies.append(train_acc)
    # 验证模型
    model.eval()  # 将模型设置为评估模式
    val_loss = 0.0  # 验证损失
    val_correct = 0  # 验证集正确预测的样本数
    val_total = 0  # 验证集总样本数
    with torch.no_grad():  # 禁用梯度计算
        for images, labels in val_loader:
            # 将数据移动到设备上
            images = images.to(device)
            labels = labels.to(device)

            # 前向传播：计算模型输出
            outputs = model(images)
            # 计算损失
            loss = criterion(outputs, labels)
            val_loss += loss.item()  # 累加损失
            # 获取预测类别
            _, predicted = torch.max(outputs.data, 1)
            # 统计正确预测的样本数
            val_total += labels.size(0)
            val_correct += (predicted == labels).sum().item()
    # 计算验证集的平均损失和准确率
    val_loss_avg = val_loss / len(val_loader)
    val_acc = 100 * val_correct / val_total
    val_losses.append(val_loss_avg)
    val_accuracies.append(val_acc)
    # 打印每轮训练和验证的结果
    print(f"Epoch [{epoch+1}/{num_epochs}], Train Loss: {train_loss_avg:.4f}, Train Acc: {train_acc:.2f}%, Val Loss: {val_loss_avg:.4f}, Val Acc: {val_acc:.2f}%")

# 测试模型
model.eval()  # 将模型设置为评估模式
test_loss = 0.0  # 测试损失
test_correct = 0  # 测试集正确预测的样本数
test_total = 0  # 测试集总样本数
with torch.no_grad():  # 禁用梯度计算
    for images, labels in test_loader:
        # 将数据移动到设备上
        images = images.to(device)
        labels = labels.to(device)

        # 前向传播：计算模型输出
        outputs = model(images)
        # 计算损失
        loss = criterion(outputs, labels)
        test_loss += loss.item()  # 累加损失
        # 获取预测类别
        _, predicted = torch.max(outputs.data, 1)
        # 统计正确预测的样本数
        test_total += labels.size(0)
        test_correct += (predicted == labels).sum().item()
# 打印测试集的平均损失和准确率
test_acc = 100 * test_correct / test_total
print(f"测试集 Loss: {test_loss/len(test_loader):.4f}, 测试集 Acc: {test_acc:.2f}%")

import matplotlib.pyplot as plt
# 创建画布和子图
plt.figure(figsize=(12, 5))  # 画布大小为 12x5
# 子图 1：绘制准确率
plt.subplot(1, 2, 1)  # 1 行 2 列，第 1 个子图
plt.plot(range(1, num_epochs + 1), train_accuracies, label="Train Acc", marker="o")
plt.plot(range(1, num_epochs + 1), val_accuracies, label="Val Acc", marker="o")
plt.xlabel("Epoch")
plt.ylabel("Accuracy (%)")
plt.title("Training and Validation Accuracy")
plt.legend()
plt.grid(True)
# 子图 2：绘制损失
plt.subplot(1, 2, 2) # 1 行 2 列，第 2 个子图
plt.plot(range(1, num_epochs + 1), train_losses, label="Train Loss", marker="o")
plt.plot(range(1, num_epochs + 1), val_losses, label="Val Loss", marker="o")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("Training and Validation Loss")
plt.legend()
plt.grid(True)
# 显示图像
plt.tight_layout()  # 自动调整子图间距
plt.show()
