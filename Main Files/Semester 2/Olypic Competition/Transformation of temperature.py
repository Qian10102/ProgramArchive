def hex_to_temperature(hex_string, min_temp=20, max_temp=30):
    """
    将16进制字符串转换为指定范围内的温度值
    参数:
    hex_string (str): 10位16进制字符串
    min_temp (float): 温度最小值，默认20°C
    max_temp (float): 温度最大值，默认30°C
    返回:
    float: 转换后的温度值
    """
    # 将16进制字符串转换为整数
    hex_value = int(hex_string, 16)
    # 计算总的可能值范围
    max_hex_value = 2 ** 40 - 1
    # 线性映射到温度范围
    temperature = min_temp + (hex_value / max_hex_value) * (max_temp - min_temp)
    return round(temperature, 2)

# 额外的测试用例
test_cases = [
    "C710600A04",
    "2C05261040"
]

print("多个测试用例: ")
for case in test_cases:
    print(f"字符串 {case} 对应温度: {hex_to_temperature(case)}°C")
