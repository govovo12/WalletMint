"""
Create Merchant Account 任務模組
------------------------------------------------
職責：
    - 透過 OPS 後台建立商戶帳號
    - 自動帶入代理 UUID、模式、OTP、基本資料
    - 驗證 API 回傳 Code / Message
    - 成功時回寫 Context["INDEX"][name]["merchant"]["account"]
"""

from workspace.tasks.common.common_async_task import send_batch_api_requests
from workspace.config.error_code import ResultCode


async def create_merchant_task(context, debug: bool = False):
    """
    新增商戶帳號任務
    Args:
        context (dict): 當前 Context
        debug (bool): 是否印出 debug 資訊
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
    #    ⚠ Loader 已確保商戶欄位完整，可安全過濾空值
    # ============================================================
    payload_sources = []
    for name, data in index.items():
        agent_info = data.get("agent", {})
        merchant_info = data.get("merchant", {})

        payload = {
            "AgUuid": agent_info.get("uuid"),
            "Name": name,
            "Mail": merchant_info.get("email"),
            "Password": merchant_info.get("password"),
            "Mode": merchant_info.get("modetype"),
            "OtpCode": ("COMMON", "OPS", "LOGIN_OTP"),
            "Remark": "",
            "LineName": "",
            "LineDomain": "",
        }

        # ✅ 過濾掉空值（None 或空字串）
        clean_payload = {k: v for k, v in payload.items() if v not in [None, ""]}

        payload_sources.append((name, clean_payload))

    # ============================================================
    # Step 3. 呼叫共用層批次執行 (POST)
    # ============================================================
    results = await send_batch_api_requests(
        context=context,
        role="OPS",
        api_group="ENDPOINTS",
        path_key="CREATE_MERCHANT_ACCOUNT",
        payload_sources=payload_sources,
        method="POST",
        use_header=True,
        header_type="Sid",
    )

    # ============================================================
    # Step 4. 驗證每筆回傳內容
    # ============================================================
    for name, code, records in results:
        records_all.extend(records)

        if code != ResultCode.SUCCESS:
            records_all.append({
                "type": "error",
                "message": f"[{name}] HTTP 層執行失敗，ResultCode={code}"
            })
            continue

        parsed = records[-1].get("response", {}).get("parsed", {})
        if not isinstance(parsed, dict):
            records_all.append({
                "type": "error",
                "message": f"[{name}] 回傳格式錯誤，非 JSON",
                "result_code": ResultCode.task_create_merchant_invalid_response
            })
            continue

        api_code = parsed.get("Code")
        api_msg = parsed.get("Message")
        result = parsed.get("Result", {})

        # 驗證 Code 與 Message
        if api_code != 0:
            records_all.append({
                "type": "error",
                "message": f"[{name}] 新增商戶帳號失敗 Code={api_code}, Msg={api_msg}",
                "result_code": ResultCode.task_create_merchant_failed
            })
            continue

        if api_msg != "Success":
            records_all.append({
                "type": "error",
                "message": f"[{name}] 回傳 Message 非 'Success'：{api_msg}",
                "result_code": ResultCode.task_create_merchant_failed
            })
            continue

        # 驗證結果欄位
        account_value = result.get("Account")
        if not account_value:
            records_all.append({
                "type": "error",
                "message": f"[{name}] 回傳結果缺少 Account 欄位",
                "result_code": ResultCode.task_create_merchant_missing_field
            })
            continue

        # ========================================================
        # Step 5. 寫回 Context 並紀錄成功訊息
        # ========================================================
        context["INDEX"][name]["merchant"]["account"] = account_value

        records_all.append({
            "type": "info",
            "message": f"[{name}] 新增商戶帳號成功 → Account: {account_value}"
        })

    # ============================================================
    # Step 6. 統一回傳
    # ============================================================
    return context, ResultCode.SUCCESS, records_all
