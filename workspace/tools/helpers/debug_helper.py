# workspace/tools/helpers/debug_helper.py
"""
Debug Helper
功能：
    - 提供 is_debug() 判斷目前是否開啟 Debug 模式
    - 支援 CLI 參數優先於 .env 設定
    - CLI 可用:
        --debug     強制開啟
        --no-debug  強制關閉
"""

import sys


def is_debug(context: dict | None = None) -> bool:
    """
    判斷是否開啟 Debug 模式
    優先順序：
        1. CLI 傳入 --debug 或 --no-debug
        2. context["COMMON"]["DEBUG"] (.env)
        3. 預設 False
    """
    argv_lower = [arg.lower() for arg in sys.argv]

    # Step 1. CLI 強制開關判斷
    if "--debug" in argv_lower:
        return True
    if "--no-debug" in argv_lower:
        return False

    # Step 2. 從 context 讀取 (.env 載入結果)
    try:
        if context:
            common = context.get("COMMON", {})
            value = common.get("DEBUG")
            if isinstance(value, bool):
                return value
            if isinstance(value, str):
                return value.lower() in ("1", "true", "yes", "on")
    except Exception:
        pass

    # Step 3. 預設關閉
    return False
