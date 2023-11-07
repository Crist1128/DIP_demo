import pandas as pd

class ExcelDataImporter:
    def __init__(self, file_path):
        self.file_path = file_path

    def import_data(self):
        try:
            df = pd.read_excel(self.file_path)
            for index, row in df.iterrows():
                case_number = row['病例号']
                diagnosis_code_1 = row['第一诊断编码']
                diagnosis_code_2 = row['第二诊断编码']
                diagnosis_code_3 = row['第三诊断编码']
                operation_code_1 = row['第一操作编码']
                operation_code_2 = row['第二操作编码']
                operation_code_3 = row['第三操作编码']
                payment_amount = row['付费金额']

                # 处理空值，将空值替换为 None
                if pd.isna(diagnosis_code_1):
                    diagnosis_code_1 = None
                if pd.isna(diagnosis_code_2):
                    diagnosis_code_2 = None
                if pd.isna(diagnosis_code_3):
                    diagnosis_code_3 = None
                if pd.isna(operation_code_1):
                    operation_code_1 = None
                if pd.isna(operation_code_2):
                    operation_code_2 = None
                if pd.isna(operation_code_3):
                    operation_code_3 = None
                if pd.isna(payment_amount):
                    payment_amount = None

                yield case_number, diagnosis_code_1, diagnosis_code_2, diagnosis_code_3, operation_code_1, operation_code_2, operation_code_3, payment_amount

        except Exception as e:
            print(f"Error importing data: {e}")

if __name__ == "__main__":
    file_path = "userdata_test.xlsx"  # 替换为你的 Excel 文件路径

    data_importer = ExcelDataImporter(file_path)
    for row_data in data_importer.import_data():
        print(row_data)
