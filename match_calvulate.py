import pymysql
import config
from database_connector import DatabaseConnector
from data_importer import ExcelDataImporter
from diagnosis_matcher import match_procedure_codes
from database_connector import DatabaseQueries

def calculate_match(file_path, scoring_unit_price):
    # 定义数据库连接参数
    database_config = config.database_config

    total_scoring_value = 0
    total_payment_amount = 0
    results_per_case = []
    match_failure_info = []

    try:
        # 使用 DatabaseConnector 类来处理数据库连接
        with DatabaseConnector(**database_config) as db_connector:
            # 创建游标
            cursor = db_connector.cursor

            # 创建数据库查询助手对象
            query_helper = DatabaseQueries(cursor)

            # 初始化 ExcelDataImporter，并提供 Excel 文件路径
            data_importer = ExcelDataImporter(file_path)

            for row_data in data_importer.import_data():
                case_number = row_data[0]
                diagnosis_codes = row_data[1:4]
                operation_codes = row_data[4:7]

                scoring_values = []

                for diagnosis_code, operation_code in zip(diagnosis_codes, operation_codes):
                    if diagnosis_code is not None:
                        # 使用查询助手类执行数据库查询
                        diagnosis_result = query_helper.get_diagnosis_by_code(diagnosis_code)

                        if diagnosis_result:
                            diagnosis_id, diagnosis_name = diagnosis_result

                            scoring_records = query_helper.get_scoring_records_by_diagnosis_id(diagnosis_id)

                            match_found = False

                            for record in scoring_records:
                                scoring_id, procedure_codes, scoring_value = record

                                operation_code_match, matching_format = match_procedure_codes(str(operation_code), str(procedure_codes))

                                if operation_code_match:
                                    match_found = True
                                    scoring_values.append(scoring_value)

                            if not match_found:
                                match_failure_info.append(f"No matching scoring records found for the Case Number {case_number} with given operation code ({operation_code}).")
                        else:
                            match_failure_info.append(f"Diagnosis not found in the database (Case Number: {case_number}, Diagnosis Code: {diagnosis_code}).")

                if scoring_values:
                    total_scoring_value += sum(scoring_values)
                    total_payment_amount += row_data[-1]
                    # 计算每列病例号的分值单价*分值总和和与总费用的相差值
                    case_value = sum(scoring_values) * scoring_unit_price
                    case_difference = case_value - row_data[-1]
                    results_per_case.append((case_number, case_value, case_difference))

    except Exception as e:
        print(f"Error: {e}")

    return total_scoring_value, total_payment_amount, results_per_case, match_failure_info


if __name__ == "__main__":
    # 这里是原来的主函数，现在不再包含计算和输出，只是用于演示
    calculate_match("userdata_test.xlsx", 0.5)
