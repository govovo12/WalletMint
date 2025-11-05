# workspace/controllers/ops_controller.py
"""
OPS 控制器
職責：
    - Step 1：產生 OTP (登入用)
    - Step 2：登入運營後台
    - Step 3：重新產生 OTP（用於後續批次任務）
    - Step 4：批次新增代理商帳號
    - Step 5：查詢代理帳號（確認建立成功並取得 UUID）
"""

from workspace.tools.printer.step_printer import print_step
from workspace.tools.printer.error_printer import print_result
from workspace.tools.printer.debug_printer import debug_print
from workspace.tools.printer.context_printer import print_context
from workspace.tools.helpers.debug_helper import is_debug

from workspace.tasks.common.otp_task import generate_role_otp
from workspace.tasks.common.login_task import common_login
from workspace.tasks.ops.create_agent_task import create_agent_task
from workspace.tasks.ops.query_agent_uuid_task import query_agent_uuid_task  
from workspace.tasks.ops.create_merchant_task import create_merchant_task 
from workspace.tasks.ops.query_merchant_uuid_task import query_merchant_uuid_task 
from workspace.config.error_code import ResultCode
import asyncio


def run_ops_controller(context, branch_state=None, prefix="OPS"):
    branch_state = branch_state or []

    def handle_step_result(step_no, code, records):
        """統一處理任務結果輸出與流程中斷邏輯"""
        print_result(code, branch_state=branch_state + [True, True], prefix=prefix, is_last=False)

        # 🧩 若 debug 模式 → 印所有記錄 + context
        if is_debug(context):
            if records:
                _print_records(records, prefix, branch_state)
            print_context(context, prefix, step_no, branch_state + [True, True, True])

        # 🧩 若非 debug 模式但有錯誤 → 仍要印出錯誤訊息
        elif code != ResultCode.SUCCESS and records:
            error_records = [r for r in records if r.get("type") == "error"]
            if error_records:
                _print_records(error_records, prefix, branch_state)

        # 若任務失敗則回傳 False → 中止後續流程
        return code == ResultCode.SUCCESS

    # ============================================================
    # Step 1：產生 OTP（登入用）
    # ============================================================
    print_step(prefix, 1, "產生一次性登入碼 (OTP for Login)", branch_state, is_last=False)
    context, code = generate_role_otp(context, "OPS")
    if not handle_step_result(1, code, []):
        return context

    # ============================================================
    # Step 2：登入運營後台
    # ============================================================
    print_step(prefix, 2, "登入運營後台", branch_state, is_last=False)
    context, code, records = common_login(context=context, role="OPS", debug=is_debug(context))
    if not handle_step_result(2, code, records):
        return context

    # ============================================================
    # Step 3：重新產生 OTP（用於後續批次任務）
    # ============================================================
    print_step(prefix, 3, "重新產生一次性驗證碼 (OTP for Batch Tasks)", branch_state, is_last=False)
    context, code = generate_role_otp(context, "OPS")
    if not handle_step_result(3, code, []):
        return context

    # ============================================================
    # Step 4：批次新增代理商帳號
    # ============================================================
    print_step(prefix, 4, "批次新增代理商帳號", branch_state, is_last=False)
    context, code, records = asyncio.run(create_agent_task(context, debug=is_debug(context)))
    if not handle_step_result(4, code, records):
        return context

    # ============================================================
    # Step 5：查詢代理帳號（確認建立成功並取得 UUID）
    # ============================================================
    print_step(prefix, 5, "查詢代理帳號（確認建立成功並取得 UUID）", branch_state, is_last=False)
    context, code, records = asyncio.run(query_agent_uuid_task(context, debug=is_debug(context)))
    if not handle_step_result(5, code, records):
        return context

    # ============================================================
    # Step 6：產生 OTP（用於新增商戶帳號）
    # ============================================================
    print_step(prefix, 6, "產生一次性驗證碼 (OTP for Merchant Creation)", branch_state, is_last=False)
    context, code = generate_role_otp(context, "OPS")
    if not handle_step_result(6, code, []):
        return context

    # ============================================================
    # Step 7：批次新增商戶帳號
    # ============================================================
    print_step(prefix, 7, "批次新增商戶帳號", branch_state, is_last=False)
    context, code, records = asyncio.run(create_merchant_task(context, debug=is_debug(context)))
    if not handle_step_result(7, code, records):
        return context

    # ============================================================
    # Step 8：查詢商戶帳號（確認建立成功並取得 MerUuid）
    # ============================================================
    print_step(prefix, 8, "查詢商戶帳號（確認建立成功並取得 MerUuid）", branch_state, is_last=True)
    context, code, records = asyncio.run(query_merchant_uuid_task(context, debug=is_debug(context)))
    handle_step_result(8, code, records)

    return context





# ============================================================
# 輔助：統一輸出 API Debug 紀錄（整合 Printer Framework + 批次分隔）
# ============================================================
def _print_records(records, prefix, branch_state, name=None):
    name_prefix = f"{prefix}-{name}" if name else prefix

    for record in records:
        rtype = record.get("type", "")
        msg = record.get("message", "")
        req = record.get("request", {})
        res = record.get("response", {})

        # === 印訊息本身 ===
        if rtype == "error":
            debug_print(True, f"❌ {msg}", name_prefix, branch_state)
        else:
            debug_print(True, msg, name_prefix, branch_state)

        # === 特殊分隔（每筆查詢成功後空一行）===
        if msg and ("查詢代理帳號成功" in msg or "查詢商戶帳號成功" in msg):
            print()

        # === 印出 Request ===
        if req:
            method = req.get("method")
            url = req.get("url")
            headers = req.get("headers")
            params = req.get("params")
            payload = req.get("payload")

            if method:
                debug_print(True, f"method: {method}", name_prefix, branch_state)
            if url:
                debug_print(True, f"url: {url}", name_prefix, branch_state)
            if headers:
                debug_print(True, f"headers: {headers}", name_prefix, branch_state)
            if params:
                debug_print(True, f"params: {params}", name_prefix, branch_state)
            elif payload:
                debug_print(True, f"payload: {payload}", name_prefix, branch_state)

        # === 印出 Response（展開完整 text，不再截斷）===
        if res:
            status = res.get("status_code")
            if status:
                debug_print(True, f"status: {status}", name_prefix, branch_state)
            if "text" in res:
                text = res.get("text", "")
                # 🆕 不再截斷，完整輸出 JSON
                debug_print(True, f"response: {text}", name_prefix, branch_state)

    print()





