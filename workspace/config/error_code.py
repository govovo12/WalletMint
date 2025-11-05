# workspace/config/error_code.py
"""
錯誤碼定義模組
用途：
    - 統一管理所有錯誤代碼與訊息
    - 支援 printer 系列模組使用 (error_printer 等)
結構：
    工具錯誤碼：1000–1999
    任務錯誤碼：2000–2999（預留）
    控制器錯誤碼：3000–3999（預留）
"""

class ResultCode:
    SUCCESS = 0

    # ---------------- 工具錯誤碼 (1000-1999) ----------------

    # --- Loader 工具錯誤碼 (1001–1020) ---
    tools_loader_file_not_found        = 1001  # 找不到設定檔
    tools_loader_read_failed           = 1002  # 載入或解析過程失敗
    tools_loader_unsupported_format    = 1003  # 不支援的設定檔格式
    tools_loader_unknown_error         = 1004  # 其他未知例外
    tools_loader_permission_denied     = 1005  # 無法存取檔案（權限被拒）
    tools_loader_invalid_key_format    = 1006  # .env 變數名稱格式不符（非 prefix_field 格式）
    tools_loader_invalid_group_mapping = 1007  # .env 群組資料不完整（缺少必要欄位或欄位拼錯）

    # --- wallet 工具 (1021-1040) ---
    tools_wallet_invalid_private_key = 1021
    tools_wallet_invalid_address     = 1022
    tools_wallet_mask_error          = 1023

    # --- ledger 工具 (1041-1060) ---
    tools_ledger_balance_error       = 1041
    tools_ledger_trc20_invalid_contract = 1042
    tools_ledger_trc20_invalid_method   = 1043
    tools_ledger_trc20_balance_error    = 1044
    tools_ledger_trc20_unknown_error    = 1045

    # --- currency_converter 工具 (1061-1080) ---
    tools_currency_fetch_error       = 1061
    tools_currency_not_supported     = 1062
    tools_currency_convert_error     = 1063

    # --- request 工具 (1081-1100) ---
    tools_request_error              = 1081
    tools_request_timeout            = 1082
    tools_request_put_error          = 1083 

    # --- response 工具 (1101-1120) ---
    tools_response_none              = 1101
    tools_response_bad_status        = 1102
    tools_response_json_error        = 1103
    tools_response_field_missing     = 1104

    # --- client 工具 (1121-1140) ---
    tools_client_invalid_address     = 1121
    tools_client_account_not_found   = 1122
    tools_client_balance_error       = 1123
    tools_client_broadcast_error     = 1124
    tools_client_unknown_error       = 1125
    tools_client_block_error         = 1126
    tools_client_tx_receipt_error    = 1127
    tools_client_network_error       = 1128

    # --- builder 工具 (1141-1160) ---
    tools_builder_invalid_params     = 1141
    tools_builder_error              = 1142
    tools_builder_trc20_invalid_contract = 1143
    tools_builder_trc20_invalid_method   = 1144
    tools_builder_trc20_error            = 1145

    # --- signer 工具 (1161-1180) ---
    tools_signer_invalid_private_key = 1161
    tools_signer_sign_error          = 1162

    # --- broadcaster 工具 (1181-1200) ---
    tools_broadcaster_invalid_tx     = 1181
    tools_broadcaster_error          = 1182
    tools_broadcaster_broadcast_error= 1183

    # --- otp 工具 (1201-1220) ---
    tools_otp_invalid_secret         = 1201
    tools_otp_generate_error         = 1202
    tools_otp_verify_error           = 1203

    # --- watcher 工具 (1221-1240) ---
    tools_watcher_timeout            = 1221
    tools_watcher_pending            = 1222
    tools_watcher_error              = 1223

    # --- file 工具 (1241–1260) ---
    tools_file_dir_not_found        = 1241  # 目標資料夾不存在
    tools_file_permission_denied    = 1242  # 無法存取資料夾權限
    tools_file_invalid_path         = 1243  # 提供的路徑參數不合法
    tools_file_list_failed          = 1244  # 讀取或列出資料夾內容失敗
    tools_file_no_files_found       = 1245  # 沒有找到任何符合條件的檔案
    tools_file_unknown_error        = 1246  # 未知例外錯誤（捕捉 fallback）

    # ---------------- 任務錯誤碼 (2000-2999) ----------------

    # --- 共用任務 (2001–2020) ---
    task_api_failed               = 2001
    task_payload_build_error      = 2002
    task_response_parse_error     = 2003
    task_missing_field            = 2004
    task_invalid_context          = 2005
    task_json_parse_error         = 2006   # 🔹 回傳非 JSON
    task_invalid_api_code         = 2007   # 🔹 登入 API Code 錯誤（非 0）
    task_result_field_missing     = 2008   # 🔹 登入結果缺少 Sid / Uuid

    # --- loader 任務 (2021–2040) ---
    task_name_invalid_key_format      = 2021  # 名稱 key 含非法字元（非中英文或底線）
    task_name_invalid_key_length      = 2022  # 名稱長度不在 2~20 範圍內
    task_env_missing_key              = 2023  # 系統設定 (.env) 缺少必要欄位或值為空
    task_name_empty_value             = 2024  # 名稱值為空
    task_name_file_missing            = 2025  # 找不到任何名稱設定檔
    task_name_multiple_files_detected = 2026  # 偵測到多個名稱設定檔

    # 密碼 / 信箱驗證
    task_password_missing             = 2027  # 密碼為空
    task_password_invalid_length      = 2028  # 密碼長度不符（需 6~20）
    task_password_invalid_charset     = 2029  # 密碼含非法字元（僅允許英文、數字與符號）
    task_email_missing                = 2030  # 信箱為空
    task_email_invalid_format         = 2031  # 信箱格式錯誤
    task_mode_type_missing            = 2032  # 運營模式欄位缺失或無值
    task_mode_type_invalid_format     = 2033  # 運營模式欄位非數字格式
    task_mode_type_invalid_value      = 2034  # 運營模式欄位值僅允許 0 或 1

    # --- create_agent 任務 (2041–2060) ---
    task_create_agent_failed           = 2041  # API 回傳 Code ≠ 0
    task_create_agent_missing_field    = 2042  # 回傳結果中缺少 Account 欄位
    task_create_agent_invalid_response = 2043  # 回傳格式錯誤或非 JSON

    # --- query_agent 任務 (2061–2080) ---
    task_query_agent_code_invalid       = 2061  # API 回傳 Code 非 0
    task_query_agent_message_invalid    = 2062  # API 回傳 Message 非「sucess」
    task_query_agent_account_mismatch   = 2063  # 回傳 Account 與預期不符
    task_query_agent_name_mismatch      = 2064  # 回傳 Name 與預期不符
    task_query_agent_mail_mismatch      = 2065  # 回傳 Mail 與預期不符
    task_query_agent_uuid_missing       = 2066  # 回傳結果缺少 Uuid 或值為空

    # --- create_merchant 任務 (2081–2100) ---
    task_create_merchant_failed           = 2081  # API 回傳 Code ≠ 0
    task_create_merchant_missing_field    = 2082  # 回傳結果缺少 Account 欄位
    task_create_merchant_invalid_response = 2083  # 回傳格式錯誤或非 JSON

    # --- query_merchant 任務 (2101–2120) ---
    task_query_merchant_code_invalid      = 2101  # API 回傳 Code 非 0
    task_query_merchant_message_invalid   = 2102  # API 回傳 Message 非 "Success"
    task_query_merchant_account_mismatch  = 2103  # 回傳 MerAccount 與預期不符
    task_query_merchant_mail_mismatch     = 2104  # 回傳 Mail 與預期不符
    task_query_merchant_mode_mismatch     = 2105  # 回傳 Mode 與預期不符
    task_query_merchant_status_invalid    = 2106  # 回傳 Status 非 1（未啟用）
    task_query_merchant_account_empty     = 2107  # Items 為空集合（查無商戶帳號）
    task_query_merchant_uuid_missing      = 2108  # 回傳缺少 MerUuid 或值為空


# ===== 工具層錯誤碼集合 (1000–1999) =====
TOOL_ERROR_CODES = {
    
    # Loader
    ResultCode.tools_loader_file_not_found,
    ResultCode.tools_loader_read_failed,
    ResultCode.tools_loader_unsupported_format,
    ResultCode.tools_loader_unknown_error,
    ResultCode.tools_loader_permission_denied,
    ResultCode.tools_loader_invalid_key_format,
    ResultCode.tools_loader_invalid_group_mapping,


    # Wallet
    ResultCode.tools_wallet_invalid_private_key,
    ResultCode.tools_wallet_invalid_address,
    ResultCode.tools_wallet_mask_error,

    # Ledger
    ResultCode.tools_ledger_balance_error,
    ResultCode.tools_ledger_trc20_invalid_contract,
    ResultCode.tools_ledger_trc20_invalid_method,
    ResultCode.tools_ledger_trc20_balance_error,
    ResultCode.tools_ledger_trc20_unknown_error,

    # Currency Converter
    ResultCode.tools_currency_fetch_error,
    ResultCode.tools_currency_not_supported,
    ResultCode.tools_currency_convert_error,

    # Request / Response
    ResultCode.tools_request_error,
    ResultCode.tools_request_timeout,
    ResultCode.tools_request_put_error,
    ResultCode.tools_response_none,
    ResultCode.tools_response_bad_status,
    ResultCode.tools_response_json_error,
    ResultCode.tools_response_field_missing,

    # Client
    ResultCode.tools_client_invalid_address,
    ResultCode.tools_client_account_not_found,
    ResultCode.tools_client_balance_error,
    ResultCode.tools_client_broadcast_error,
    ResultCode.tools_client_unknown_error,
    ResultCode.tools_client_block_error,
    ResultCode.tools_client_tx_receipt_error,
    ResultCode.tools_client_network_error,

    # Builder
    ResultCode.tools_builder_invalid_params,
    ResultCode.tools_builder_error,
    ResultCode.tools_builder_trc20_invalid_contract,
    ResultCode.tools_builder_trc20_invalid_method,
    ResultCode.tools_builder_trc20_error,

    # Signer
    ResultCode.tools_signer_invalid_private_key,
    ResultCode.tools_signer_sign_error,

    # Broadcaster
    ResultCode.tools_broadcaster_invalid_tx,
    ResultCode.tools_broadcaster_error,
    ResultCode.tools_broadcaster_broadcast_error,

    # OTP
    ResultCode.tools_otp_invalid_secret,
    ResultCode.tools_otp_generate_error,
    ResultCode.tools_otp_verify_error,

    # Watcher
    ResultCode.tools_watcher_timeout,
    ResultCode.tools_watcher_pending,
    ResultCode.tools_watcher_error,

    # File
    ResultCode.tools_file_dir_not_found,
    ResultCode.tools_file_permission_denied,
    ResultCode.tools_file_invalid_path,
    ResultCode.tools_file_list_failed,
    ResultCode.tools_file_no_files_found,
    ResultCode.tools_file_unknown_error,

}


# ===== 成功碼與預留分類 =====
SUCCESS_CODES = {
    ResultCode.SUCCESS,
}

TASK_ERROR_CODES = {
    ResultCode.task_api_failed,
    ResultCode.task_payload_build_error,
    ResultCode.task_response_parse_error,
    ResultCode.task_missing_field,
    ResultCode.task_invalid_context,
    ResultCode.task_json_parse_error,
    ResultCode.task_invalid_api_code,
    ResultCode.task_result_field_missing,

    # loader 任務
    ResultCode.task_name_invalid_key_format,
    ResultCode.task_name_invalid_key_length,
    ResultCode.task_env_missing_key,
    ResultCode.task_name_empty_value,
    ResultCode.task_name_file_missing,
    ResultCode.task_name_multiple_files_detected,

    # loader 任務 - 運營模式檢查
    ResultCode.task_mode_type_missing,
    ResultCode.task_mode_type_invalid_format,
    ResultCode.task_mode_type_invalid_value,


    # 密碼 / 信箱
    ResultCode.task_password_missing,
    ResultCode.task_password_invalid_length,
    ResultCode.task_password_invalid_charset,
    ResultCode.task_email_missing,
    ResultCode.task_email_invalid_format,

    # --- create_agent 任務 ---
    ResultCode.task_create_agent_failed,
    ResultCode.task_create_agent_missing_field,
    ResultCode.task_create_agent_invalid_response,

    # --- query_agent 任務 ---
    ResultCode.task_query_agent_code_invalid,
    ResultCode.task_query_agent_message_invalid,
    ResultCode.task_query_agent_account_mismatch,
    ResultCode.task_query_agent_name_mismatch,
    ResultCode.task_query_agent_mail_mismatch,
    ResultCode.task_query_agent_uuid_missing,

    # --- create_merchant 任務 ---
    ResultCode.task_create_merchant_failed,
    ResultCode.task_create_merchant_missing_field,
    ResultCode.task_create_merchant_invalid_response,

    # --- query_merchant 任務 ---
    ResultCode.task_query_merchant_code_invalid,
    ResultCode.task_query_merchant_message_invalid,
    ResultCode.task_query_merchant_account_mismatch,
    ResultCode.task_query_merchant_mail_mismatch,
    ResultCode.task_query_merchant_mode_mismatch,
    ResultCode.task_query_merchant_status_invalid,
    ResultCode.task_query_merchant_account_empty,   
    ResultCode.task_query_merchant_uuid_missing,    




}
CTRL_ERROR_CODES = set()   # 預留控制器錯誤碼


# ---------------- 訊息區 ----------------
ERROR_MESSAGES = {
    ResultCode.SUCCESS: "操作成功",

    # --- tools_loader (1001–1020) ---
    ResultCode.tools_loader_file_not_found:       "Loader 工具：找不到設定檔",
    ResultCode.tools_loader_read_failed:          "Loader 工具：載入設定檔失敗",
    ResultCode.tools_loader_unsupported_format:   "Loader 工具：不支援的設定檔格式",
    ResultCode.tools_loader_unknown_error:        "Loader 工具：未知錯誤",
    ResultCode.tools_loader_permission_denied:    "Loader 工具：無法存取檔案（權限被拒）",
    ResultCode.tools_loader_invalid_key_format:    "Loader 工具：.env 變數名稱格式不符，需使用 <群組>_<欄位> 形式（例如 a_name）",
    ResultCode.tools_loader_invalid_group_mapping: "Loader 工具：.env 群組資料不完整，請確認每組包含 name、password、email 欄位",


    # --- tools_wallet (1021–1040) ---
    ResultCode.tools_wallet_invalid_private_key: "Wallet 工具：私鑰不合法",
    ResultCode.tools_wallet_invalid_address: "Wallet 工具：地址不合法",
    ResultCode.tools_wallet_mask_error: "Wallet 工具：地址遮罩錯誤",

    # --- tools_ledger (1041–1060) ---
    ResultCode.tools_ledger_balance_error: "Ledger 工具：餘額查詢錯誤",
    ResultCode.tools_ledger_trc20_invalid_contract: "Ledger 工具：TRC20 合約不合法",
    ResultCode.tools_ledger_trc20_invalid_method: "Ledger 工具：TRC20 方法不合法",
    ResultCode.tools_ledger_trc20_balance_error: "Ledger 工具：TRC20 餘額查詢錯誤",
    ResultCode.tools_ledger_trc20_unknown_error: "Ledger 工具：TRC20 未知錯誤",

    # --- tools_currency_converter (1061–1080) ---
    ResultCode.tools_currency_fetch_error: "Currency 工具：幣別匯率獲取失敗",
    ResultCode.tools_currency_not_supported: "Currency 工具：幣別不支援",
    ResultCode.tools_currency_convert_error: "Currency 工具：幣別轉換錯誤",

    # --- tools_request_response (1081–1120) ---
    ResultCode.tools_request_error: "Request 工具：發送錯誤",
    ResultCode.tools_request_timeout: "Request 工具：請求逾時",
    ResultCode.tools_request_put_error: "Request 工具：PUT 請求錯誤",
    ResultCode.tools_response_none: "Response 工具：回應為空",
    ResultCode.tools_response_bad_status: "Response 工具：HTTP 狀態不正確",
    ResultCode.tools_response_json_error: "Response 工具：解析 JSON 失敗",
    ResultCode.tools_response_field_missing: "Response 工具：必要欄位缺失",

    # --- tools_client (1121–1140) ---
    ResultCode.tools_client_invalid_address: "Client 工具：地址不合法",
    ResultCode.tools_client_account_not_found: "Client 工具：帳號不存在",
    ResultCode.tools_client_balance_error: "Client 工具：餘額查詢錯誤",
    ResultCode.tools_client_broadcast_error: "Client 工具：交易廣播錯誤",
    ResultCode.tools_client_unknown_error: "Client 工具：未知錯誤",
    ResultCode.tools_client_block_error: "Client 工具：區塊查詢錯誤",
    ResultCode.tools_client_tx_receipt_error: "Client 工具：交易回執查詢錯誤",
    ResultCode.tools_client_network_error: "Client 工具：網路錯誤",

    # --- tools_builder (1141–1160) ---
    ResultCode.tools_builder_invalid_params: "Builder 工具：參數不合法",
    ResultCode.tools_builder_error: "Builder 工具：建構交易錯誤",
    ResultCode.tools_builder_trc20_invalid_contract: "Builder 工具：TRC20 合約不合法",
    ResultCode.tools_builder_trc20_invalid_method: "Builder 工具：TRC20 方法不合法",
    ResultCode.tools_builder_trc20_error: "Builder 工具：TRC20 建構錯誤",

    # --- tools_signer (1161–1180) ---
    ResultCode.tools_signer_invalid_private_key: "Signer 工具：私鑰不合法",
    ResultCode.tools_signer_sign_error: "Signer 工具：簽名失敗",

    # --- tools_broadcaster (1181–1200) ---
    ResultCode.tools_broadcaster_invalid_tx: "Broadcaster 工具：交易不合法",
    ResultCode.tools_broadcaster_error: "Broadcaster 工具：未知錯誤",
    ResultCode.tools_broadcaster_broadcast_error: "Broadcaster 工具：交易廣播失敗",

    # --- tools_otp (1201–1220) ---
    ResultCode.tools_otp_invalid_secret: "OTP 工具：密鑰不合法",
    ResultCode.tools_otp_generate_error: "OTP 工具：生成失敗",
    ResultCode.tools_otp_verify_error: "OTP 工具：驗證失敗",

    # --- tools_watcher (1221–1240) ---
    ResultCode.tools_watcher_timeout: "Watcher 工具：等待超時",
    ResultCode.tools_watcher_pending: "Watcher 工具：交易仍在等待中",
    ResultCode.tools_watcher_error: "Watcher 工具：未知錯誤",

    # --- tools_file (1241–1260) ---
    ResultCode.tools_file_dir_not_found: "File 工具：目標資料夾不存在",
    ResultCode.tools_file_permission_denied: "File 工具：無法存取資料夾（權限被拒）",
    ResultCode.tools_file_invalid_path: "File 工具：路徑參數不合法",
    ResultCode.tools_file_list_failed: "File 工具：列出資料夾內容時發生錯誤",
    ResultCode.tools_file_no_files_found: "File 工具：未找到任何符合條件的檔案",
    ResultCode.tools_file_unknown_error: "File 工具：未知錯誤",

    # --- task_common (2001–2020) ---
    ResultCode.task_api_failed: "共用任務：API 呼叫失敗",
    ResultCode.task_payload_build_error: "共用任務：Payload 建立失敗",
    ResultCode.task_response_parse_error: "共用任務：回應解析錯誤",
    ResultCode.task_missing_field: "共用任務：缺少必要欄位",
    ResultCode.task_invalid_context: "共用任務：Context 無效",
    ResultCode.task_json_parse_error: "共用任務：回傳格式非 JSON",
    ResultCode.task_invalid_api_code: "共用任務：API Code 錯誤（非 200）",
    ResultCode.task_result_field_missing: "共用任務：回傳結果缺少 Sid 或 Uuid",

    # --- task_loader (2021–2040) ---
    ResultCode.task_name_invalid_key_format:      "名稱設定任務：變數名稱包含非法字元（僅允許中英文與底線）",
    ResultCode.task_name_invalid_key_length:      "名稱設定任務：變數名稱長度需介於 2～20 字元之間",
    ResultCode.task_env_missing_key:              "名稱設定任務：系統設定 (.env) 缺少必要欄位或為空",
    ResultCode.task_name_empty_value:             "名稱設定任務：名稱值為空，請提供有效名稱",
    ResultCode.task_name_file_missing:            "名稱設定任務：找不到任何名稱設定檔，請確認 profiles 資料夾內容",
    ResultCode.task_name_multiple_files_detected: "名稱設定任務：偵測到多個名稱設定檔，請僅保留一份 (.env/.json/.xlsx/.csv)",

    # 密碼 / 信箱
    ResultCode.task_password_missing:             "名稱設定任務：密碼欄位為空或缺失",
    ResultCode.task_password_invalid_length:      "名稱設定任務：密碼長度需介於 6～20 個字元之間",
    ResultCode.task_password_invalid_charset:     "名稱設定任務：密碼僅允許英文、數字與常見符號",
    ResultCode.task_email_missing:                "名稱設定任務：信箱欄位為空或缺失",
    ResultCode.task_email_invalid_format:         "名稱設定任務：信箱格式錯誤，請輸入有效的電子郵件地址",

    # --- 運營模式檢查 ---
    ResultCode.task_mode_type_missing:        "名稱設定任務：缺少運營模式欄位或未填值 (a_mode_type)",
    ResultCode.task_mode_type_invalid_format: "名稱設定任務：運營模式欄位格式錯誤，僅允許數字 1 或 2",
    ResultCode.task_mode_type_invalid_value:  "名稱設定任務：運營模式欄位值不合法，僅允許 1=手續費模式 或 2=月租費模式",



    # --- create_agent 任務 (2041–2060) ---
    ResultCode.task_create_agent_failed: "新增代理商任務：API 回傳 Code 非 0",
    ResultCode.task_create_agent_missing_field: "新增代理商任務：回傳結果缺少 Account 欄位",
    ResultCode.task_create_agent_invalid_response: "新增代理商任務：回傳格式錯誤或非 JSON",

    # --- query_agent 任務 (2061–2080) ---
    ResultCode.task_query_agent_code_invalid:      "查詢代理帳號任務：API 回傳 Code 非 0",
    ResultCode.task_query_agent_message_invalid:   "查詢代理帳號任務：API 回傳 Message 非「成功」",
    ResultCode.task_query_agent_account_mismatch:  "查詢代理帳號任務：回傳的 Account 與預期不符",
    ResultCode.task_query_agent_name_mismatch:     "查詢代理帳號任務：回傳的 Name 與預期不符",
    ResultCode.task_query_agent_mail_mismatch:     "查詢代理帳號任務：回傳的 Mail 與預期不符",
    ResultCode.task_query_agent_uuid_missing:      "查詢代理帳號任務：回傳結果缺少 Uuid 或值為空",

    # --- create_merchant 任務 (2081–2100) ---
    ResultCode.task_create_merchant_failed: "新增商戶帳號任務：API 回傳 Code 非 0",
    ResultCode.task_create_merchant_missing_field: "新增商戶帳號任務：回傳結果缺少 Account 欄位",
    ResultCode.task_create_merchant_invalid_response: "新增商戶帳號任務：回傳格式錯誤或非 JSON",

    # --- query_merchant 任務 (2101–2120) ---
    ResultCode.task_query_merchant_code_invalid:       "查詢商戶帳號任務：API 回傳 Code 非 0",
    ResultCode.task_query_merchant_message_invalid:    "查詢商戶帳號任務：API 回傳 Message 非 'Success'",
    ResultCode.task_query_merchant_account_mismatch:   "查詢商戶帳號任務：回傳 MerAccount 與預期不符",
    ResultCode.task_query_merchant_mail_mismatch:      "查詢商戶帳號任務：回傳 Mail 與預期不符",
    ResultCode.task_query_merchant_mode_mismatch:      "查詢商戶帳號任務：回傳 Mode 與預期不符",
    ResultCode.task_query_merchant_status_invalid:     "查詢商戶帳號任務：商戶帳號狀態異常（Status ≠ 1）",
    ResultCode.task_query_merchant_account_empty:      "查詢商戶帳號任務：API 回傳 Items 為空集合",
    ResultCode.task_query_merchant_uuid_missing:       "查詢商戶帳號任務：回傳缺少 MerUuid 或值為空",








}
