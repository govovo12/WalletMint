"""
file_helper.py
-----------------
用途：
    - 提供基礎檔案操作功能（無業務邏輯）
    - 僅回傳結果與錯誤碼，不印 log、不 raise Exception
    - 供任務模組調用，例如：
        load_context_task 先呼叫 list_files_by_ext() 檢查 profiles 內檔案狀況

錯誤碼範圍：
    tools_file_xxx (1241–1260)
"""

import os
from typing import Tuple, List
from workspace.config.error_code import ResultCode


# ------------------------------------------------------------
# 🔹 列出符合指定副檔名的檔案
# ------------------------------------------------------------
def list_files_by_ext(directory: str, exts: tuple = (".env", ".json", ".xlsx", ".csv")) -> Tuple[List[str], int]:
    """
    列出指定資料夾中所有符合副檔名的檔案。

    Parameters
    ----------
    directory : str
        要搜尋的資料夾路徑
    exts : tuple[str]
        可接受的副檔名（預設為 .env/.json/.xlsx/.csv）

    Returns
    -------
    (files, code)
        files : list[str] - 找到的完整路徑清單
        code  : ResultCode
    """
    if not directory or not isinstance(directory, str):
        return [], ResultCode.tools_file_invalid_path

    if not os.path.exists(directory):
        return [], ResultCode.tools_file_dir_not_found

    try:
        files = [
            os.path.join(directory, f)
            for f in os.listdir(directory)
            if f.lower().endswith(exts)
        ]
        if not files:
            return [], ResultCode.tools_file_no_files_found
        return files, ResultCode.SUCCESS

    except PermissionError:
        return [], ResultCode.tools_file_permission_denied
    except Exception:
        return [], ResultCode.tools_file_list_failed


# ------------------------------------------------------------
# 🔹 檢查單一檔案是否存在
# ------------------------------------------------------------
def file_exists(file_path: str) -> Tuple[bool, int]:
    """
    檢查單一檔案是否存在。

    Returns
    -------
    (exists, code)
        exists : bool - 檔案是否存在
        code   : ResultCode
    """
    if not file_path or not isinstance(file_path, str):
        return False, ResultCode.tools_file_invalid_path

    try:
        return os.path.exists(file_path), ResultCode.SUCCESS
    except Exception:
        return False, ResultCode.tools_file_unknown_error


# ------------------------------------------------------------
# 🔹 取得資料夾內所有檔案名稱（不含路徑）
# ------------------------------------------------------------
def list_all_files(directory: str) -> Tuple[List[str], int]:
    """
    列出資料夾內所有檔案名稱（不含子資料夾）。
    """
    if not directory or not isinstance(directory, str):
        return [], ResultCode.tools_file_invalid_path

    if not os.path.exists(directory):
        return [], ResultCode.tools_file_dir_not_found

    try:
        items = [
            f for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, f))
        ]
        if not items:
            return [], ResultCode.tools_file_no_files_found
        return items, ResultCode.SUCCESS

    except PermissionError:
        return [], ResultCode.tools_file_permission_denied
    except Exception:
        return [], ResultCode.tools_file_list_failed
