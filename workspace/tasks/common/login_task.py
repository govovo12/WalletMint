# workspace/tasks/common/login_task.py
"""
共用任務模組：login_task.py（最終版）
功能：
    - 支援新版 context 結構 (OPS 在 COMMON 內)
    - 自動從 context 組出登入 URL
    - 呼叫 common_task.send_api_request() 發送登入請求
    - 登入成功後回寫 SSID、UUID 到 context
"""

from workspace.tasks.common.common_task import  send_api_request
from workspace.config.error_code import ResultCode


def common_login(context: dict, role: str = "OPS", debug: bool = False):
    """
    通用登入任務
    :param context: 主 context
    :param role: 登入角色，例如 "OPS" / "AGENT" / "MERCHANT"
    :param debug: 是否開啟除錯輸出
    :return: (context, code, records)
    """
    records = []

    try:
        # === Step 0. 檢查角色資料 ===
        role_data = context.get("COMMON", {}).get(role)
        if not role_data:
            records.append({
                "type": "error",
                "message": f"[{role}] 在 context['COMMON'] 中找不到登入資料"
            })
            return context, ResultCode.task_invalid_context, records

        # === Step 1. 自動組合登入 URL ===
        base_url = context["COMMON"].get("BACKEND_RA_BASE_URL", "")
        path = context.get("API", {}).get("LOGIN_PATHS", {}).get(role)
        if not base_url or not path:
            records.append({
                "type": "error",
                "message": f"[{role}] 缺少對應的 Base URL 或 LOGIN_PATHS"
            })
            return context, ResultCode.task_invalid_context, records



        # 組完整 URL（自動處理斜線）
        if base_url.endswith("/") and path.startswith("/"):
            login_url = base_url[:-1] + path
        elif not base_url.endswith("/") and not path.startswith("/"):
            login_url = base_url + "/" + path
        else:
            login_url = base_url + path

        # === Step 2. 組建登入 Payload ===
        payload = {
            "Account": role_data.get("USERNAME") or role_data.get("ACCOUNT"),
            "Password": role_data.get("PASSWORD"),
            "OtpCode": role_data.get("LOGIN_OTP") or role_data.get("OTP_SECRET"),
        }

        records.append({"type": "debug", "message": f"[{role}] 登入請求 → {login_url}"})
        records.append({"type": "debug", "message": f"[{role}] Payload: {payload}"})

        # === Step 3. 發送登入 API ===
        data, code = send_api_request(
            context=context,
            role=role,
            url=login_url,
            payload=payload,
            method="POST",
            use_header=False,  # 登入時不帶 Sid/Uuid
        )

        if code != ResultCode.SUCCESS:
            records.append({
                "type": "error",
                "message": f"[{role}] 登入請求失敗，ResultCode={code}"
            })
            return context, code, records

        # === Step 4. 解析登入結果 ===
        code_field = data.get("Code")
        msg_field = data.get("Message")
        result = data.get("Result", {}) or {}

        sid = result.get("Sid") or result.get("sid") or result.get("SSID")
        uuid = result.get("Uuid") or result.get("uuid") or result.get("UUID")

        if code_field != 0:
            records.append({
                "type": "error",
                "message": f"[{role}] 登入失敗 Code={code_field}, Message={msg_field}"
            })
            return context, ResultCode.task_invalid_api_code, records

        if not sid or not uuid:
            records.append({
                "type": "error",
                "message": f"[{role}] 登入結果缺少 Sid 或 Uuid"
            })
            return context, ResultCode.task_result_field_missing, records

        # === Step 5. 回寫 context ===
        role_data["SSID"] = sid
        role_data["UUID"] = uuid

        records.append({
            "type": "debug",
            "message": f"[{role}] 登入成功 → SSID={sid[:8]}..., UUID={uuid[:8]}..."
        })

        return context, ResultCode.SUCCESS, records

    except Exception as e:
        records.append({
            "type": "error",
            "message": f"[{role}] 任務例外: {e}"
        })
        return context, ResultCode.task_api_failed, records
