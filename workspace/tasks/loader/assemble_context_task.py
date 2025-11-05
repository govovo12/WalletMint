# workspace/tasks/loader/assemble_context_task.py
"""
Assemble Context 任務模組
職責：
    - 接收 Step 1 (COMMON) 與 Step 2 (INDEX) 的資料
    - 載入 config/api_paths
    - 組合最終 Context 結構
"""

from workspace.config import api_paths
from workspace.config.error_code import ResultCode


def assemble_context(common_context: dict, index_context: dict):
    """組合最終 Context 結構"""
    if not common_context or not index_context:
        return {}, ResultCode.task_invalid_context

    context = {
        "COMMON": common_context,
        "INDEX": index_context,
        "API": {
            "LOGIN_PATHS": api_paths.LOGIN_PATHS,
            "ENDPOINTS": api_paths.ENDPOINTS,
        },
    }

    return context, ResultCode.SUCCESS
