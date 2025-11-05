"""
Query Agent UUID 任務模組
------------------------------------------------
職責：
    - 查詢代理帳號是否成功建立
    - 驗證 API 回傳結構與欄位值正確性
    - 將取得的 Uuid 寫入 Context["INDEX"][name]["agent"]["uuid"]
    - ⚠️ 注意：後端實際回傳 Message="Success"（前端顯示為「成功」）
"""

from workspace.tasks.common.common_async_task import send_batch_api_requests
from workspace.config.error_code import ResultCode


async def query_agent_uuid_task(context, debug: bool = False):
    """
    查詢代理帳號 UUID 任務
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
        agent_info = index[name].get("agent", {})
        payload_source = {
            "Account": agent_info.get("account"),
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
        path_key="QUERY_AGENT_ACCOUNT",
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
        result = parsed.get("Result", {})

        # ========================================================
        # 驗證 API 基本欄位
        # ========================================================
        if api_code != 0:
            records_all.append({
                "type": "error",
                "message": f"[{name}] 查詢代理帳號失敗 Code={api_code}",
                "result_code": ResultCode.task_query_agent_code_invalid
            })
            continue

        # ✅ 後端實際回傳 "Success"，前端才會轉譯成中文「成功」
        if api_msg != "Success":
            records_all.append({
                "type": "error",
                "message": f"[{name}] 查詢代理帳號回傳 Message 非 'Success'：{api_msg}",
                "result_code": ResultCode.task_query_agent_message_invalid
            })
            continue

        items = result.get("Items") or []
        if not items:
            records_all.append({
                "type": "error",
                "message": f"[{name}] 查無 Items 結果",
                "result_code": ResultCode.task_query_agent_uuid_missing
            })
            continue

        item = items[0]
        uuid_value = item.get("Uuid")
        account_value = item.get("Account")
        name_value = item.get("Name")
        mail_value = item.get("Mail")

        # ========================================================
        # 驗證關鍵欄位一致性
        # ========================================================
        expected_account = index[name]["agent"].get("account")
        expected_name = name
        expected_mail = index[name]["agent"].get("email")

        if account_value != expected_account:
            records_all.append({
                "type": "error",
                "message": f"[{name}] 回傳 Account 不符：{account_value} ≠ {expected_account}",
                "result_code": ResultCode.task_query_agent_account_mismatch
            })
            continue

        if name_value != expected_name:
            records_all.append({
                "type": "error",
                "message": f"[{name}] 回傳 Name 不符：{name_value} ≠ {expected_name}",
                "result_code": ResultCode.task_query_agent_name_mismatch
            })
            continue

        if mail_value != expected_mail:
            records_all.append({
                "type": "error",
                "message": f"[{name}] 回傳 Mail 不符：{mail_value} ≠ {expected_mail}",
                "result_code": ResultCode.task_query_agent_mail_mismatch
            })
            continue

        if not uuid_value or not isinstance(uuid_value, str):
            records_all.append({
                "type": "error",
                "message": f"[{name}] Uuid 缺失或為空值",
                "result_code": ResultCode.task_query_agent_uuid_missing
            })
            continue

        # ========================================================
        # Step 5. 寫回 Context 並紀錄成功訊息
        # ========================================================
        context["INDEX"][name]["agent"]["uuid"] = uuid_value
        records_all.append({
            "type": "info",
            "message": f"[{name}] 查詢代理帳號成功 → UUID: {uuid_value}"
        })

    # ============================================================
    # Step 6. 統一回傳
    # ============================================================
    return context, ResultCode.SUCCESS, records_all
