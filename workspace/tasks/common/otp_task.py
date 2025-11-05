"""
共用任務模組：otp_task.py（新結構）
功能：
    - 從 context["COMMON"][role] 中取出 OTP_SECRET
    - 呼叫 otp_generator 產生 OTP
    - 產生成功則寫回 LOGIN_OTP
    - 若發生錯誤，回傳對應的 ResultCode
"""

from workspace.tools.otp.otp_generator import generate_otp
from workspace.config.error_code import ResultCode


def generate_role_otp(context: dict, role: str, debug: bool = False):
    """通用 OTP 任務（新結構版）"""
    try:
        # 🔹 新結構：從 COMMON 區塊取角色設定
        target = context.get("COMMON", {}).get(role)
        if not target:
            return context, ResultCode.task_invalid_context  # 沒有該角色設定

        # 🔹 支援防呆 list 結構
        if isinstance(target, list):
            target = target[0]

        secret = target.get("OTP_SECRET")
        if not secret:
            return context, ResultCode.tools_otp_invalid_secret  # 缺少密鑰

        # 呼叫工具層產生 OTP（會回傳 (otp, code)）
        otp, code = generate_otp(secret)

        if code != ResultCode.SUCCESS:
            # 工具層若回傳失敗，直接轉傳
            return context, code

        if not otp:
            return context, ResultCode.tools_otp_generate_error

        # 寫回 context
        target["LOGIN_OTP"] = otp
        if debug:
            print(f"[DEBUG] 為 {role} 產生 OTP：{otp}")

        return context, ResultCode.SUCCESS

    except Exception as e:
        print(f"[❌ OTP 任務例外] {role}: {e}")
        return context, ResultCode.EXCEPTION
