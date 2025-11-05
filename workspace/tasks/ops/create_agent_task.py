"""
Create Agent 任務模組（批次版）
職責：
    - 組出所有名稱索引的 payload_source
    - 呼叫共用層批次併發 API（send_batch_api_requests）
    - 檢查每筆回應是否 Code=0
    - 將每筆成功結果回寫至 Context INDEX[name]["agent"]["account"]
"""

from workspace.tasks.common.common_async_task import send_batch_api_requests
from workspace.config.error_code import ResultCode


async def create_agent_task(context, debug: bool = False):
    """
    批次建立代理商帳號任務
    Args:
        context (dict): 當前 Context
        debug (bool): 是否輸出 debug log（由上層控制印出，不傳給共用層）
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
    # Step 2. 組出所有 payload_source
    # ============================================================
    payload_sources = []
    for name in index.keys():
        payload_source = {
            "Name": name,  # 名稱本身是 key
            "Password": ("INDEX", name, "agent", "password"),
            "Mail": ("INDEX", name, "agent", "email"),
            "OtpCode": ("COMMON", "OPS", "LOGIN_OTP"),
        }
        payload_sources.append((name, payload_source))

    # ============================================================
    # Step 3. 呼叫共用層批次執行
    # ============================================================
    results = await send_batch_api_requests(
        context=context,
        role="OPS",
        api_group="ENDPOINTS",
        path_key="CREATE_AGENT_ACCOUNT",
        payload_sources=payload_sources,
        method="POST",
        use_header=True,
        header_type="Sid",  # 明確指定 Sid header
    )

    # ============================================================
    # Step 4. 解析每筆結果並更新 Context
    # ============================================================
    for name, code, records in results:
        records_all.extend(records)

        if code != ResultCode.SUCCESS:
            records_all.append({
                "type": "error",
                "message": f"[{name}] HTTP 層執行失敗，ResultCode={code}"
            })
            continue

        # 解析共用層回傳結果
        parsed = records[-1].get("response", {}).get("parsed", {})
        api_code = parsed.get("Code")
        api_msg = parsed.get("Message")
        result = parsed.get("Result", {})

        # 檢查 API Code
        if api_code != 0:
            records_all.append({
                "type": "error",
                "message": f"[{name}] API 回傳錯誤 Code={api_code}, Msg={api_msg}"
            })
            continue

        # 檢查 Result 欄位
        account = result.get("Account")
        if not account:
            records_all.append({
                "type": "error",
                "message": f"[{name}] 回傳結果缺少 Account 欄位"
            })
            continue

        # ✅ 寫回 Context
        context["INDEX"][name]["agent"]["account"] = account

        records_all.append({
            "type": "info",
            "message": f"[{name}] 建立代理帳號成功 → Account: {account}"
        })

    # ============================================================
    # Step 5. 統一回傳
    # ============================================================
    return context, ResultCode.SUCCESS, records_all
