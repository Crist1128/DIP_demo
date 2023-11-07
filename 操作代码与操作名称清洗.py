import pandas as pd
import re

# 假设您的数据保存在一个名为“操作编码（未分类）.xlsx”的Excel文件中，且数据位于第一个工作表
data = pd.read_excel('操作编码（未分类）.xlsx')

# 创建两个空队列Q1和Q2
q1 = []
q2 = []

# 遍历数据集，处理操作编码和操作名称，并放入Q1和Q2
for index, row in data.iterrows():
    # 使用fillna将NaN值替换为空字符串
    operation_codes = re.split(r'[+/]', str(row['操作编码']))
    operation_names = re.split(r'[+/]', str(row['操作名称']))
    for code, name in zip(operation_codes, operation_names):
        q1.append(code.strip())  # 去除额外的空格
        q2.append(name.strip())  # 去除额外的空格

# 创建一个字典来建立操作编码到操作名称的映射
operation_mapping = dict(zip(q1, q2))

# 创建一个新DataFrame以保存映射后的数据
result = pd.DataFrame({'操作编码': list(operation_mapping.keys()), '操作名称': list(operation_mapping.values())})

# 将结果保存到新的Excel文件
result.to_excel('mapped_data.xlsx', index=False)
