# workspace/tasks/loader/load_profile_context_task.py
"""
Profile Context 任務模組（純資料直通版）
------------------------------------------------
職責：
    - 讀取 profiles 目錄下的名稱設定檔 (.env / .csv / .xlsx)
    - 驗證欄位結構與值格式（不做欄位名轉換）
    - 回傳 INDEX 結構（名稱為 key，內容為原始欄位值）

設計理念：
    ✅ Loader 層：只檢查結構，不改 key
    ✅ Task 層：不做資料轉換，照原欄位命名使用
    ✅ 嚴格分層、資料原樣流通
"""

import os
import re
from workspace.config import paths
from workspace.tools.file.file_helper import list_files_by_ext
from workspace.tools.loader.loader import (
    load_profile_env,
    load_profile_file,
)
from workspace.config.error_code import ResultCode


# ===========================================================
# 🧩 驗證規則設定（由任務層自行定義）
# ===========================================================
_REQUIRED_FIELDS = {"name", "password", "email", "modetype"}  # 與 .env 一致
_NAME_RE = re.compile(r"^[A-Za-z\u4e00-\u9fa5]+$")
_PASSWORD_ALLOWED_RE = re.compile(r"^[A-Za-z0-9!@#$%^&*()_+\-=\[\]{};:'\",.<>/?\\|`~]+$")
_EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def load_profile_context():
    """載入 profiles 設定檔，驗證結構與內容（不轉換欄位名）"""
    # -------------------------------------------------------
    # 1️⃣ 搜尋 profiles 資料夾內可用檔案
    # -------------------------------------------------------
    profile_dir = os.path.dirname(paths.PROFILE_FILE_PATH)
    files, code = list_files_by_ext(profile_dir)
    if code not in (ResultCode.SUCCESS, ResultCode.tools_file_no_files_found):
        return {}, code
    if not files:
        return {}, ResultCode.task_name_file_missing
    if len(files) > 1:
        return {}, ResultCode.task_name_multiple_files_detected

    file_path = files[0]
    ext = os.path.splitext(file_path)[1].lower()

    # -------------------------------------------------------
    # 2️⃣ 載入檔案內容（明確指定 required_fields）
    # -------------------------------------------------------
    if ext == ".env":
        raw_data, code2 = load_profile_env(file_path, required_fields=_REQUIRED_FIELDS)
    else:
        raw_data, code2 = load_profile_file(file_path)
    if code2 != ResultCode.SUCCESS:
        return {}, code2

    if not isinstance(raw_data, dict) or "records" not in raw_data:
        return {}, ResultCode.task_api_failed
    records = raw_data["records"]

    # -------------------------------------------------------
    # 3️⃣ 驗證每筆欄位值內容（不改 key 名）
    # -------------------------------------------------------
    index_dict = {}
    for rec in records:
        name = str(rec.get("name", "")).strip()
        password = str(rec.get("password", "")).strip()
        email = str(rec.get("email", "")).strip()
        modetype = str(rec.get("modetype", "")).strip()

        # 名稱檢查
        if not name:
            return {}, ResultCode.task_name_empty_value
        if not _NAME_RE.match(name):
            return {}, ResultCode.task_name_invalid_key_format
        if not (2 <= len(name) <= 20):
            return {}, ResultCode.task_name_invalid_key_length

        # 密碼檢查
        if not password:
            return {}, ResultCode.task_password_missing
        if not (6 <= len(password) <= 20):
            return {}, ResultCode.task_password_invalid_length
        if not _PASSWORD_ALLOWED_RE.match(password):
            return {}, ResultCode.task_password_invalid_charset

        # 信箱檢查
        if not email:
            return {}, ResultCode.task_email_missing
        if not _EMAIL_RE.match(email):
            return {}, ResultCode.task_email_invalid_format

        # 運營模式檢查
        if not modetype:
            return {}, ResultCode.task_mode_type_missing
        if not modetype.isdigit():
            return {}, ResultCode.task_mode_type_invalid_format
        if modetype not in ("1", "2"):  # ✅ 改成檢查 1、2
            return {}, ResultCode.task_mode_type_invalid_value

        # ---------------------------------------------------
        # 4️⃣ 組成 INDEX 結構（商戶與代理共用密碼/信箱）
        # ---------------------------------------------------
        index_dict[name] = {
            "agent": {
                "account": None,
                "password": password,
                "email": email,
            },
            "merchant": {
                "account": None,
                "password": password,  # ✅ 同 agent
                "email": email,        # ✅ 同 agent
                "modetype": int(modetype),
            },
        }

    return index_dict, ResultCode.SUCCESS
