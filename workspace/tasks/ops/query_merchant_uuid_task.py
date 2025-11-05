"""
Query Merchant UUID 任務模組
------------------------------------------------
職責：
    - 查詢商戶帳號是否成功建立
    - 驗證 API 回傳結構與欄位值正確性
    - 將取得的 MerUuid 寫入 Context["INDEX"][name]["merchant"]["uuid"]
"""

from workspace.tasks.common.common_async_task import send_batch_api_requests
from workspace.config.error_code import ResultCode


async def query_merchant_uuid_task(context, debug: bool = False):
    """
    查詢商戶帳號 UUID 任務
    Args:
        context (dict): 當前 Context
        debug (bool): 是否輸出 debug log
    Returns:
        tuple(context, result_code, records_all)
    """
    records_all = []

    # ============================================================
    # Step 1. 基本檢查
    # ============================================================
    index = context.get("INDEX")
    if not index or not isinstance(index, dict):
        records_all.append({"type": "error", "message": "[OPS] 找不到 INDEX 結構"})
        return context, ResultCode.task_invalid_context, records_all

    # ============================================================
    # Step 2. 組出 payload_sources
    # ============================================================
    payload_sources = []
    for name in index.keys():
        merchant_info = index[name].get("merchant", {})
        payload_source = {
            "MerAccount": merchant_info.get("account"),
            "Page": 1,
            "Limit": 20,
        }
        payload_sources.append((name, payload_source))

    # ============================================================
    # Step 3. 呼叫共用層批次執行 (GET)
    # ============================================================
    results = await send_batch_api_requests(
        context=context,
        role="OPS",
        api_group="ENDPOINTS",
        path_key="QUERY_MERCHANT_ACCOUNT",
        payload_sources=payload_sources,
        method="GET",
        use_header=True,
        header_type="Sid",
    )

    # ============================================================
    # Step 4. 驗證每筆回傳內容
    # ============================================================
    for name, code, records in results:
        records_all.extend(records)

        # 4-1. HTTP 層失敗
        if code != ResultCode.SUCCESS:
            records_all.append({
                "type": "error",
                "message": f"[{name}] HTTP 執行失敗，ResultCode={code}"
            })
            continue

        # 4-2. 解析回傳 JSON 結構
        parsed = records[-1].get("response", {}).get("parsed", {})
        api_code = parsed.get("Code")
        api_msg = parsed.get("Message")
        result = parsed.get("Result", {}) or {}
        items = result.get("Items") or []

        # ========================================================
        # 驗證 API 基本欄位
        # ========================================================
        if api_code != 0:
            records_all.append({
                "type": "error",
                "message": f"[{name}] 查詢商戶帳號失敗 Code={api_code}",
                "result_code": ResultCode.task_query_merchant_code_invalid
            })
            continue

        if api_msg != "Success":
            records_all.append({
                "type": "error",
                "message": f"[{name}] 查詢商戶帳號回傳 Message 非 'Success'：{api_msg}",
                "result_code": ResultCode.task_query_merchant_message_invalid
            })
            continue

        if not items:
            records_all.append({
                "type": "error",
                "message": f"[{name}] 查無 Items 結果",
                "result_code": ResultCode.task_query_merchant_account_empty
            })
            continue

        # 4-3. 依帳號比對目標
        merchant_info = index[name]["merchant"]
        expected_account = merchant_info.get("account")
        expected_mail = merchant_info.get("email")
        expected_mode = int(merchant_info.get("modetype", 0))

        target = next((it for it in items if it.get("MerAccount") == expected_account), None)
        if not target:
            records_all.append({
                "type": "error",
                "message": f"[{name}] 找不到對應的商戶帳號：{expected_account}",
                "result_code": ResultCode.task_query_merchant_account_mismatch
            })
            continue

        uuid_value = target.get("MerUuid")
        account_value = target.get("MerAccount")
        mail_value = target.get("Mail")
        mode_value = int(target.get("Mode", -1))
        status_value = target.get("Status")

        # ========================================================
        # 驗證欄位一致性
        # ========================================================
        if not uuid_value or not isinstance(uuid_value, str):
            records_all.append({
                "type": "error",
                "message": f"[{name}] MerUuid 缺失或為空值",
                "result_code": ResultCode.task_query_merchant_uuid_missing
            })
            continue

        if account_value != expected_account:
            records_all.append({
                "type": "error",
                "message": f"[{name}] 回傳 MerAccount 不符：{account_value} ≠ {expected_account}",
                "result_code": ResultCode.task_query_merchant_account_mismatch
            })
            continue

        if mail_value != expected_mail:
            records_all.append({
                "type": "error",
                "message": f"[{name}] 回傳 Mail 不符：{mail_value} ≠ {expected_mail}",
                "result_code": ResultCode.task_query_merchant_mail_mismatch
            })
            continue

        if mode_value != expected_mode:
            records_all.append({
                "type": "error",
                "message": f"[{name}] 回傳 Mode 不符：{mode_value} ≠ {expected_mode}",
                "result_code": ResultCode.task_query_merchant_mode_mismatch
            })
            continue

        if status_value != 1:
            records_all.append({
                "type": "error",
                "message": f"[{name}] 商戶帳號狀態異常（Status ≠ 1）",
                "result_code": ResultCode.task_query_merchant_status_invalid
            })
            continue

        # ========================================================
        # Step 5. 寫回 Context 並紀錄成功訊息
        # ========================================================
        context["INDEX"][name]["merchant"]["uuid"] = uuid_value
        records_all.append({
            "type": "info",
            "message": f"[{name}] 查詢商戶帳號成功 → MerUuid: {uuid_value}"
        })

    # ============================================================
    # Step 6. 統一回傳
    # ============================================================
    return context, ResultCode.SUCCESS, records_all
