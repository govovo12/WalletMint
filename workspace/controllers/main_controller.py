"""
Main 控制器
負責：串接 Loader 子控（載入 .env → 回傳 context），再呼叫 OPS 子控。
"""

from workspace.tools.printer.step_printer import print_step
from workspace.controllers.loader_controller import run_loader_controller
from workspace.controllers.ops_controller import run_ops_controller


def run_main_controller(branch_state=None, prefix="Main", max_step=None):
    branch_state = branch_state or []

    # Step 1：呼叫 Loader 控制器
    print_step(prefix, 1, "呼叫 Loader 控制器", branch_state, is_last=False)
    context = run_loader_controller(branch_state=branch_state + [True, True], prefix="Loader")

    # ✅ 若 CLI 指定只執行到 Step 1，這裡就結束（不印提示）
    if max_step == 1:
        return context

    # Step 2：呼叫 OPS 控制器
    print_step(prefix, 2, "呼叫 OPS 控制器", branch_state, is_last=True)
    run_ops_controller(context, branch_state + [True, True], prefix="OPS")

    return context

