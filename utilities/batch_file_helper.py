from utilities.error_constants import ERROR_MAP


def validate_bus_ack_file(context) -> bool:
    content = context.fileContent
    lines = content.strip().split("\n")
    header = lines[0].split("|")
    expected_columns = 14

    if len(header) != expected_columns:
        print(f"Header column count mismatch: expected {expected_columns}, got {len(header)}")
        return False

    valid_ids = set(
        context.vaccine_df["UNIQUE_ID"].astype(str) + "^" + context.vaccine_df["UNIQUE_ID_URI"].astype(str)
    )

    # Create a mapping from LOCAL_ID to IMMS_ID
    local_to_imms = {}
    overall_valid = True

    for i, line in enumerate(lines[1:], start=2):
        fields = line.split("|")
        row_valid = True  # Reset for each row

        if len(fields) != expected_columns:
            print(f"Row {i}: column count mismatch ({len(fields)} fields)")
            overall_valid = False
            continue

        header_response_code = fields[1]
        issue_severity = fields[2]
        issue_code = fields[3]
        response_code = fields[6]
        response_display = fields[7]
        local_id = fields[10]
        imms_id = fields[11]
        message_delivery = fields[13]

        if header_response_code != "OK":
            print(f"Row {i}: HEADER_RESPONSE_CODE is not OK")
            row_valid = False
        if issue_severity != "Information":
            print(f"Row {i}: ISSUE_SEVERITY is not Information")
            row_valid = False
        if issue_code != "OK":
            print(f"Row {i}: ISSUE_CODE is not OK")
            row_valid = False
        if response_code != "30001":
            print(f"Row {i}: RESPONSE_CODE is not 30001")
            row_valid = False
        if response_display != "Success":
            print(f"Row {i}: RESPONSE_DISPLAY is not Success")
            row_valid = False
        if local_id not in valid_ids:
            print(f"Row {i}: LOCAL_ID not found in vaccine_df")
            row_valid = False
        if not imms_id:
            print(f"Row {i}: IMMS_ID is missing")
            row_valid = False
        if message_delivery != "True":
            print(f"Row {i}: MESSAGE_DELIVERY is not True")
            row_valid = False
        if row_valid:
            local_to_imms[local_id] = imms_id
        else:
            overall_valid = False

    context.vaccine_df["LOCAL_ID"] = ( context.vaccine_df["UNIQUE_ID"].astype(str) + "^" + context.vaccine_df["UNIQUE_ID_URI"].astype(str) )
    context.vaccine_df["IMMS_ID"] = context.vaccine_df["LOCAL_ID"].map(local_to_imms)

    print("IMMS_ID mapping:")
    print(context.vaccine_df[["LOCAL_ID", "IMMS_ID"]])
    return overall_valid


def validate_inf_ack_file(context, success: bool = True) -> bool:
    content = context.fileContent
    lines = content.strip().split("\n")
    header = lines[0].split("|")
    row = lines[1].split("|")
    expected_columns = 12

    if len(header) != expected_columns:
        print(f"Header column count mismatch: expected {expected_columns}, got {len(header)}")
        return False
    
    row_valid = True  # Reset for each row

    if len(row) != expected_columns:
        print(f"Row {i}: column count mismatch ({len(row)} fields)")
        overall_valid = False
        return False

    header_response_code = row[1]
    issue_severity = row[2]
    issue_code = row[3]
    response_code = row[6]
    response_display = row[7]
    message_delivery = row[11]
    
    if success:
        expected_message_delivery = "True"
        excepted_header_response_code = "Success"
        excepted_issue_severity = "Information"
        excepted_issue_code = "OK"  
        excepted_response_code = "20013"
        expected_response_display = "Success"
    else:
        expected_message_delivery = "False"
        excepted_header_response_code = "Failure"
        excepted_issue_severity = "Fatal"
        excepted_issue_code = "Fatal Error"  
        excepted_response_code = "10001"
        expected_response_display

    if header_response_code != excepted_header_response_code:
        print(f"Row {i}: HEADER_RESPONSE_CODE is not {excepted_header_response_code}")
        row_valid = False
    if issue_severity != excepted_issue_severity:
        print(f"Row {i}: ISSUE_SEVERITY is not {excepted_issue_severity}")
        row_valid = False
    if issue_code != excepted_issue_code:
        print(f"Row {i}: ISSUE_CODE is not {excepted_issue_code}")
        row_valid = False
    if response_code != excepted_response_code:
        print(f"Row {i}: RESPONSE_CODE is not {excepted_response_code}")
        row_valid = False
    if response_display != expected_response_display:
        print(f"Row {i}: RESPONSE_DISPLAY is not {expected_response_display}")
        row_valid = False
    if message_delivery != expected_message_delivery:
        print(f"Row {i}: MESSAGE_DELIVERY is not {expected_message_delivery}")
        row_valid = False
    
    return row_valid

def normalize_for_lookup(id_str: str) -> str:
    parts = str(id_str).split("^")
    prefix = parts[0].strip() if len(parts) > 0 else ""
    suffix = parts[1].strip() if len(parts) > 1 else ""
    normalized_prefix = "" if prefix in ["", "nan"] else prefix
    normalized_suffix = "" if suffix in ["", "nan"] else suffix
    return f"{normalized_prefix}^{normalized_suffix}"

def validate_bus_ack_file_for_error(context) -> bool:
    content = context.fileContent
    lines = content.strip().split("\n")
    header = lines[0].split("|")

    file_rows = {}
    for i, line in enumerate(lines[1:], start=2):
        fields = line.split("|")
        local_id = fields[10]
        normalized_id = normalize_for_lookup(local_id)
        entry = {
            "row": i,
            "fields": fields,
            "original_local_id": local_id
        }
        file_rows.setdefault(normalized_id, []).append(entry)

    valid_ids = set(
        context.vaccine_df["UNIQUE_ID"].astype(str) + "^" + context.vaccine_df["UNIQUE_ID_URI"].astype(str)
    )

    overall_valid = True

    for valid_id in valid_ids:
        normalized_id = normalize_for_lookup(valid_id)
        row_data_list = file_rows.get(normalized_id)

        if not row_data_list:
            print(f"Valid ID '{valid_id}' not found in file")
            overall_valid = False
            continue
        
        for row_data in row_data_list:
            i = row_data["row"]
            fields = row_data["fields"]
            row_valid = True

            header_response_code = fields[1]
            issue_severity = fields[2]
            issue_code = fields[3]
            response_code = fields[6]
            response_display = fields[7]
            local_id = fields[10]
            imms_id = fields[11]
            operation_outcome = fields[12]
            message_delivery = fields[13]

        
            if header_response_code != "Fatal Error":
                print(f"Row {i}: HEADER_RESPONSE_CODE is not 'Fatal Error'")
                row_valid = False
            if issue_severity != "Fatal":
                print(f"Row {i}: ISSUE_SEVERITY is not 'Fatal'")
                row_valid = False
            if issue_code != "Fatal Error":
                print(f"Row {i}: ISSUE_CODE is not 'Fatal Error'")
                row_valid = False
            if response_code != "30002":
                print(f"Row {i}: RESPONSE_CODE is not '30002'")
                row_valid = False
            if response_display != "Business Level Response Value - Processing Error":
                print(f"Row {i}: RESPONSE_DISPLAY is not expected value")
                row_valid = False
            if imms_id:
                print(f"Row {i}: IMMS_ID is populated but should be null")
                row_valid = False
            if message_delivery != "False":
                print(f"Row {i}: MESSAGE_DELIVERY is not 'False'")
                row_valid = False

            try:
                valid_id_df = context.vaccine_df.loc[i-2]
                prefix = str(valid_id_df["UNIQUE_ID"]).strip()

                if prefix in ["", " ","nan"]:
                    expected_error = valid_id_df["PERSON_SURNAME"] if not valid_id_df.empty else "no_valid_surname"

                else:
                    split_parts = prefix.split("-")
                    expected_error = split_parts[2] if len(split_parts) > 2 else "invalid_prefix_format"

                expected_diagnostic = ERROR_MAP.get(expected_error, {}).get("diagnostics")

                if operation_outcome != expected_diagnostic:
                    print(f"Row {i}: operation_outcome does not match expected diagnostics '{expected_diagnostic}' for '{expected_error}' but got '{operation_outcome}'")
                    row_valid = False

            except Exception as e:
                print(f"Row {i}: error extracting expected diagnostics from local_id '{valid_id}': {e}")
                row_valid = False

            overall_valid = overall_valid and row_valid

    return overall_valid