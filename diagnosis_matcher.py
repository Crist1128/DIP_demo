def match_procedure_codes(user_operation_code, procedure_codes):
    #
    if user_operation_code is None and procedure_codes is None:
        return (True, "格式0")
    elif user_operation_code is None and procedure_codes is not None:
        return (False, "格式0")
    elif user_operation_code is not None and procedure_codes is None:
        return (False, "格式0")
    # 继续处理其他情况

    # 将 ProcedureCodes 按 '+' 分隔成多个组
    procedure_groups = procedure_codes.split('+')
    user_groups = user_operation_code.split('+')
    if len(user_groups) != len(procedure_groups):
        return (False, "格式0")  # 组数不匹配，直接返回 False
    
    # 格式1：用户操作编码为 xxx
    elif '/' not in user_operation_code and '+' not in user_operation_code:
        for group in procedure_groups:
            group_codes = group.split('/')
            if user_operation_code in group_codes:
                return (True, "格式1")
        return (False, "格式1")
        

    # 格式2：用户操作编码包含 '/'
    elif '/' in user_operation_code and '+' not in user_operation_code:
        user_codes = user_operation_code.split('/')
        used_groups = []  # 用于存放已匹配的组
        for code in user_codes:
            matched = False
            for group in procedure_groups:
                if group not in used_groups:
                    group_codes = group.split('/')
                    if code in group_codes:
                        matched = True
                        used_groups.append(group)
                        break
            if not matched:
                return (False, "格式2")
        return (True, "格式2")

    # 格式3：用户操作编码包含 '+'
    elif '+' in user_operation_code:
        used_groups = []  # 用于存放已匹配的组
        for user_group in user_groups:
            group_match = False
            user_codes = user_group.split('/')
            for code in user_codes:
                for group in procedure_groups:
                    if group not in used_groups:
                        group_codes = group.split('/')
                        if code in group_codes:
                            group_match = True
                            used_groups.append(group)
                            break
                if not group_match:
                    return (False, "格式3")
        return (True, "格式3")

    return (False, "未匹配到任何格式")

if __name__ == "__main__":
    # 示例用法
    user_operation_code = "12+33j+66"
    procedure_codes = "32/56s/12+555l/33j+66/77"

    result, matching_format = match_procedure_codes(user_operation_code, procedure_codes)
    if result:
        print(f"匹配成功，匹配格式为 {matching_format}")
    else:
        print(f"未匹配成功，匹配格式为 {matching_format}")
