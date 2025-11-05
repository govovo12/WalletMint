# workspace/controllers/loader_controller.py
"""
Loader 控制器
職責：
    - Step 1: 讀取系統設定
    - Step 2: 讀取名稱設定
    - Step 3: 組合最終 Context
    - 若開啟 Debug 模式，於每步印出完整 Context 狀態
"""

from workspace.tools.printer.step_printer import print_step
from workspace.tools.printer.error_printer import print_result
from workspace.tools.printer.context_printer import print_context
from workspace.tools.helpers.debug_helper import is_debug
from workspace.tasks.loader.load_system_context_task import load_system_context
from workspace.tasks.loader.load_profile_context_task import load_profile_context
from workspace.tasks.loader.assemble_context_task import assemble_context
from workspace.config.error_code import ResultCode


def run_loader_controller(branch_state=None, prefix="Loader"):
    branch_state = branch_state or []

    # ============================================================
    # Step 1. 讀取系統設定
    # ============================================================
    print_step(prefix, 1, "讀取系統設定", branch_state, is_last=False)
    common_context, code1 = load_system_context()
    print_result(code1, branch_state=branch_state + [True, True], prefix=prefix, is_last=False)
    if code1 != ResultCode.SUCCESS:
        return {}

    # 🔹 Step 1 Debug：印出完整 Context（目前只有 COMMON）
    context_step1 = {"COMMON": common_context}
    if is_debug(context_step1):
        print_context(context_step1, prefix, 1, branch_state + [True, True, True])

    # ============================================================
    # Step 2. 讀取名稱設定
    # ============================================================
    print_step(prefix, 2, "讀取名稱設定", branch_state, is_last=False)
    index_context, code2 = load_profile_context()
    print_result(code2, branch_state=branch_state + [True, False], prefix=prefix, is_last=False)
    if code2 != ResultCode.SUCCESS:
        return {}

    # 🔹 Step 2 Debug：印出完整 Context（COMMON + INDEX）
    context_step2 = {
        "COMMON": common_context,
        "INDEX": index_context,
    }
    if is_debug(context_step2):
        print_context(context_step2, prefix, 2, branch_state + [True, True, True])

    # ============================================================
    # Step 3. 組合最終 Context
    # ============================================================
    print_step(prefix, 3, "組合最終 Context", branch_state, is_last=True)
    context, code3 = assemble_context(common_context, index_context)
    print_result(code3, branch_state=branch_state + [True, True], prefix=prefix, is_last=True)
    if code3 != ResultCode.SUCCESS:
        return {}

    # 🔹 Step 3 Debug：印出完整最終 Context（COMMON + INDEX + API）
    if is_debug(context):
        print_context(context, prefix, 3, branch_state + [True, True, True])

    # ============================================================
    # 回傳最終 Context 給 main_controller
    # ============================================================
    return context
