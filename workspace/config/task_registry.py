# workspace/config/task_registry.py
"""
Task Registry (方法 A 架構版)

這裡集中管理所有任務的註冊，分區如下：
- task       : 一般任務
- controller : 控制器
- tool       : 工具
"""

# ===== 匯入區 =====
from workspace.controllers.main_controller import run_main_controller


TASK_REGISTRY = {
    "task": {
        # e.g. "loader": load_context,
    },
    "controller": {
        "main": run_main_controller,
    },
    "tool": {
        # e.g. "wallet": tool_wallet.run,
    },
}


def get_task(category: str, name: str):
    """
    從註冊表取得對應的任務函式
    :param category: "task" | "controller" | "tool"
    :param name: 任務或工具 ID
    :return: 可執行的函式 or None
    """
    return TASK_REGISTRY.get(category, {}).get(name)
