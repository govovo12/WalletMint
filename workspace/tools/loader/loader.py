# workspace/tools/loader/loader.py
"""
多格式設定載入工具（純工具版）
------------------------------------------------
支援：
  - .env（系統設定 / profiles 任務自行指定）
  - .json
  - .csv

設計理念：
  ✅ 完全不內建任何業務邏輯或欄位名稱
  ✅ 不自動判斷 profiles 型別，交由任務層決定
  ✅ 工具層僅負責「載入檔案、檢查結構、封裝統一格式」
"""

import os
import json
import csv
import re
import pandas as pd
from dotenv import load_dotenv, dotenv_values
from workspace.config.error_code import ResultCode


# ===========================================================
# 🟩 A. 系統設定用 .env（平面結構）
# ===========================================================
def load_system_env(file_path: str) -> tuple[dict, int]:
    """載入系統設定用的 .env（不驗 key、不群組化）"""
    if not file_path or not os.path.exists(file_path):
        return {}, ResultCode.tools_loader_file_not_found
    try:
        data = dict(dotenv_values(file_path))
        wrapped = {
            "records": [data],
            "meta": {
                "path": file_path,
                "source_type": ".env",
                "record_count": 1,
            },
        }
        return wrapped, ResultCode.SUCCESS
    except PermissionError:
        return {}, ResultCode.tools_loader_permission_denied
    except Exception:
        return {}, ResultCode.tools_loader_read_failed


# ===========================================================
# 🟩 B. 客戶 profiles 用 .env（任務層決定 required_fields）
# ===========================================================
def load_profile_env(file_path: str, required_fields: set[str] | None = None) -> tuple[dict, int]:
    """載入 profiles .env，驗證 prefix_field 結構完整性。"""
    if not file_path or not os.path.exists(file_path):
        return {}, ResultCode.tools_loader_file_not_found
    try:
        data = dict(dotenv_values(file_path))
        code = _validate_env_keys(data, required_fields)
        if code != ResultCode.SUCCESS:
            return {}, code
        wrapped = _wrap_as_standard_format(data, file_path, ".env")
        return wrapped, ResultCode.SUCCESS
    except PermissionError:
        return {}, ResultCode.tools_loader_permission_denied
    except Exception:
        return {}, ResultCode.tools_loader_read_failed


# ===========================================================
# 🟩 C. profiles 其他格式 (.json / .csv)
# ===========================================================
def load_profile_file(file_path: str) -> tuple[dict, int]:
    """讀取非 .env 類 profiles 設定檔，統一輸出格式。"""
    if not file_path or not os.path.exists(file_path):
        return {}, ResultCode.tools_loader_file_not_found

    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext == ".json":
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        elif ext == ".csv":
            df = pd.read_csv(file_path, dtype=str).fillna("")
            data = df.to_dict(orient="records")
        else:
            return {}, ResultCode.tools_loader_unsupported_format

        wrapped = _wrap_as_standard_format(data, file_path, ext)
        return wrapped, ResultCode.SUCCESS
    except PermissionError:
        return {}, ResultCode.tools_loader_permission_denied
    except Exception:
        return {}, ResultCode.tools_loader_read_failed


# ===========================================================
# 🟩 D. 驗證工具（可由任務指定 required_fields）
# ===========================================================
def _validate_env_keys(data: dict, required_fields: set[str] | None = None) -> int:
    """檢查 .env key 是否符合 prefix_field 結構。
       若指定 required_fields，則檢查每組群組是否包含這些欄位。
    """
    if not isinstance(data, dict):
        return ResultCode.tools_loader_read_failed
    if not data:
        return ResultCode.SUCCESS

    key_pattern = re.compile(r"^[A-Za-z][A-Za-z0-9]*_[A-Za-z0-9_]+$")
    groups = {}

    for k in data.keys():
        if not key_pattern.match(k):
            return ResultCode.tools_loader_invalid_key_format
        group, field = k.rsplit("_", 1)
        groups.setdefault(group.lower(), set()).add(field.lower())

    if required_fields:
        req_lower = {f.lower() for f in required_fields}
        for g, fields in groups.items():
            if not req_lower.issubset(fields):
                return ResultCode.tools_loader_invalid_group_mapping

    return ResultCode.SUCCESS


# ===========================================================
# 🟩 E. 封裝統一格式
# ===========================================================
def _wrap_as_standard_format(data, file_path: str, ext: str) -> dict:
    """統一封裝格式為 {"records": [...], "meta": {...}}"""
    records = []

    # .env 類資料：群組化處理
    if ext == ".env" and isinstance(data, dict):
        flat_keys = list(data.keys())
        if any("_" in k for k in flat_keys):
            grouped = {}
            for k, v in data.items():
                parts = k.rsplit("_", 1)
                if len(parts) != 2:
                    continue
                group, field = parts
                grouped.setdefault(group, {})[field.lower()] = v
            records = list(grouped.values())

    # 一般資料：維持原結構
    if not records:
        if isinstance(data, list):
            records = data
        elif isinstance(data, dict):
            if all(isinstance(v, (str, int, float)) for v in data.values()):
                records = [data]
            else:
                for v in data.values():
                    records.append(v if isinstance(v, dict) else {"value": v})
        else:
            records = [{"raw": str(data)}]

    return {
        "records": records,
        "meta": {
            "path": file_path,
            "source_type": ext,
            "record_count": len(records),
        },
    }


# ===========================================================
# 🟩 F. 其他輔助 API
# ===========================================================
def load_to_env(file_path: str) -> int:
    """將指定設定檔載入到 os.environ。"""
    if not file_path or not os.path.exists(file_path):
        return ResultCode.tools_loader_file_not_found
    try:
        load_dotenv(file_path, override=True)
        return ResultCode.SUCCESS
    except PermissionError:
        return ResultCode.tools_loader_permission_denied
    except Exception:
        return ResultCode.tools_loader_unknown_error


def get_env(key: str, default=None):
    """安全取得單一環境變數"""
    return os.getenv(key, default)


def get_all_env() -> tuple[dict, int]:
    """取得目前所有環境變數"""
    try:
        return dict(os.environ), ResultCode.SUCCESS
    except Exception:
        return {}, ResultCode.tools_loader_unknown_error
