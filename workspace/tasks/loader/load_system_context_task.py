# workspace/tasks/loader/load_system_context_task.py
"""
System Context 任務模組
職責：
    - 讀取系統設定 .env
    - 驗證必要欄位（DEBUG / OPS / BACKEND 等）
    - 回傳 COMMON 結構
"""

from workspace.tools.loader.loader import load_system_env
from workspace.config import paths
from workspace.config.error_code import ResultCode


# 必要欄位定義
REQUIRED_COMMON_KEYS = [
    "DEBUG",
    "TRANSFER_CHAIN",
    "BACKEND_RA_BASE_URL",
    "BACKEND_DR_BASE_URL",
    "OPS_USERNAME",
    "OPS_PASSWORD",
    "OPS_OTP_SECRET",
]


def load_system_context():
    """載入系統設定 .env，回傳 COMMON 結構"""
    env_raw, code = load_system_env(paths.ENV_FILE)
    if code != ResultCode.SUCCESS:
        return {}, code

    # 結構驗證：需包含 records
    if not isinstance(env_raw, dict) or "records" not in env_raw:
        return {}, ResultCode.task_env_missing_key
    recs = env_raw["records"]
    if not recs or not isinstance(recs[0], dict):
        return {}, ResultCode.task_env_missing_key

    env_dict = recs[0]

    # 檢查必要欄位
    missing = [k for k in REQUIRED_COMMON_KEYS if not env_dict.get(k)]
    if missing:
        print(f"[DEBUG] 系統設定缺少欄位: {missing}")
        return {}, ResultCode.task_env_missing_key

    # 組成 COMMON 結構
    common_context = {
        "DEBUG": str(env_dict["DEBUG"]).lower() == "true",
        "TRANSFER_CHAIN": env_dict["TRANSFER_CHAIN"],
        "BACKEND_RA_BASE_URL": env_dict["BACKEND_RA_BASE_URL"],
        "BACKEND_DR_BASE_URL": env_dict["BACKEND_DR_BASE_URL"],
        "OPS": {
            "USERNAME": env_dict["OPS_USERNAME"],
            "PASSWORD": env_dict["OPS_PASSWORD"],
            "OTP_SECRET": env_dict["OPS_OTP_SECRET"],
        },
    }

    return common_context, ResultCode.SUCCESS
