# workspace/config/paths.py
"""
Paths 工具模組
統一管理專案路徑，避免硬寫路徑
可以透過 ROOT_DEPTH 調整往上跳幾層
"""

import os
import sys

# --- 可調整的變數 ---
ROOT_DEPTH = 2  # 往上跳幾層 (預設: 2 層，從 config → workspace → project_root)

if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    # PyInstaller 打包模式
    ROOT_DIR = sys._MEIPASS
else:
    # 原始碼模式
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = current_dir
    for _ in range(ROOT_DEPTH):
        root_dir = os.path.dirname(root_dir)
    ROOT_DIR = root_dir

# --- 常用路徑 ---
ENV_FILE = os.path.join(ROOT_DIR, ".env")
WORKSPACE_DIR = os.path.join(ROOT_DIR, "workspace")

# --- 名稱設定檔路徑（profiles） ---
PROFILES_DIR = os.path.join(ROOT_DIR, "profiles")           # 專放名稱設定檔的資料夾
PROFILE_FILE_BASENAME = "names"                             # 固定名稱前綴
PROFILE_FILE_PATH = os.path.join(PROFILES_DIR, PROFILE_FILE_BASENAME)  # 不含副檔名