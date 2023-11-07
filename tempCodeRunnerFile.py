import pymysql
from database_connector import DatabaseConnector
from data_importer import ExcelDataImporter
from diagnosis_matcher import match_procedure_codes

def main():
    # 定义数据库连接参数
    host = "localhost"
    port = 3306
    user = "root"
    password = "20021219"
    database = "dip_database"

    try:
        # 使用 DatabaseConnector 类来处理数据库连接
        with DatabaseConnector(host, port, user, password, database) as db_connector:
            # 创建游标
            cursor = db_connector.cursor

            # 初始化 ExcelDataImporter，并提供 Excel 文件路径
            excel_file_path = "userdata_test.xlsx"  # 替换为你的 Excel 文件路径
            data_importer = ExcelDataImporter(excel_file_path)

            for row_data in data_importer.import_data():
                case_number = row_data[0]
                diagnosis_codes = row_data[1:4]  # 获取三个诊断编码
                operation_codes = row_data[4:7]  # 获取三个操作编码

                scoring_values = []  # 用于存放匹配成功的ScoringValue

                for diagnosis_code, operation_code in zip(diagnosis_codes, operation_codes):
                    # 跳过值为None的诊断编码和操作编码
                    if diagnosis_code is not None :
                        # 查询DiagnosisID和DiagnosisName
                        query = "SELECT DiagnosisID, DiagnosisName FROM diagnosis WHERE DiagnosisCode = %s"
                        cursor.execute(query, (diagnosis_code,))
                        result = cursor.fetchone()

                        if result:
                            diagnosis_id, diagnosis_name = result
                            #print(f"DiagnosisID: {diagnosis_id}, DiagnosisName: {diagnosis_name}")

                            # 查询scoring表中相关行
                            query = "SELECT ScoringID, ProcedureCodes, ScoringValue FROM scoring WHERE DiagnosisID = %s"
                            cursor.execute(query, (diagnosis_id,))
                            scoring_records = cursor.fetchall()

                            match_found = False  # 用于标记是否有匹配成功的记录

                            for record in scoring_records:
                                scoring_id, procedure_codes, scoring_value = record

                                # 匹配操作编码
                                operation_code_match, matching_format = match_procedure_codes(str(operation_code), str(procedure_codes))

                                if operation_code_match:
                                    match_found = True
                                    scoring_values.append(scoring_value)
                                    #print(f"ScoringID: {scoring_id}, ProcedureCodes: {procedure_codes}, ScoringValue: {scoring_value if scoring_value is not None else 'N/A'}, 匹配格式: {matching_format}")

                            if not match_found:
                                print(f"No matching scoring records found for the given operation code ({operation_code}).")

                        else:
                            print(f"Diagnosis not found in the database ({diagnosis_code}).")

                if scoring_values:
                    print(f"ScoringValues for Case Number {case_number}: {', '.join(str(value) for value in scoring_values)}")
                else:
                    print(f"No matching ScoringValues found for Case Number {case_number}.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
