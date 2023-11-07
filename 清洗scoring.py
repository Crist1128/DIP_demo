import pandas as pd

# 假设表一的数据保存在名为 "table1.xlsx" 的Excel文件中，表二的数据保存在名为 "table2.xlsx" 的Excel文件中
table1 = pd.read_excel("分值表test.xlsx")
table2 = pd.read_excel("diagnosis.xlsx")

# 使用merge函数将表一和表二根据诊断编码（DiagnosisCode）进行匹配，并添加DiagnosisID列
result = table1.merge(table2, left_on="诊断编码", right_on="DiagnosisCode", how="left")

# 保存结果到新的Excel文件
result.to_excel("result.xlsx", index=False)
