"""
Printer 行為註冊表（支援數字縮排 + 開關集中版）

說明：
    - 控制器層級決定邏輯層次。
    - Printer 偏移決定顯示層級（相對於控制器層級）。
    - INDENT_UNIT 可為數字（自動轉空格）或字串（例如 "\t"）。
    - PRINTER_OVERRIDES 可引用上方開關變數，方便集中管理。
    - LABEL_MAP 為顯示名稱映射（英文 prefix → 中文外觀名稱）。
"""

# ==========================================================
# 🔧 全域可調變數區（集中開關設定）
# ==========================================================

# 每層縮排單位，可為數字（空格數）或字串（例如 "\t"）
INDENT_UNIT = 2

# 控制器層級（Main=0, Loader/OPS=1）
CONTROLLER_LEVELS = {
    "Main": 0,
    "Loader": 1,
    "OPS": 1,
}

# === 顯示名稱映射（英文 prefix → 中文外觀名稱） ===
LABEL_MAP = {
    "Main": "總控",
    "Loader": "loader子控",
    "OPS": "OPS子控",
}

# === Printer 類型共通層級偏移 ===
STEP_OFFSET    = 0
ERROR_OFFSET   = 1
DEBUG_OFFSET   = 2
CONTEXT_OFFSET = 2

# === Printer 類型開關（全域控制） ===
STEP_ON     = True
DEBUG_ON    = True
ERROR_ON    = True
CONTEXT_ON  = True

# === 個別控制器開關 ===
MAIN_STEP_ON   = False    # Main 的 Step
LOADER_STEP_ON = True     # Loader 的 Step
OPS_STEP_ON    = True     # OPS 的 Step


# ==========================================================
# ⚙️ Printer 行為定義（自動引用上方變數）
# ==========================================================

DEFAULT_PRINTER_RULES = {
    "step": {
        "enabled": STEP_ON,
        "symbol": "└─ ",
        "offset": STEP_OFFSET,
    },
    "debug": {
        "enabled": DEBUG_ON,
        "symbol": "└─ ",
        "offset": DEBUG_OFFSET,
    },
    "error": {
        "enabled": ERROR_ON,
        "symbol": "└─ ",
        "offset": ERROR_OFFSET,
    },
    "context": {
        "enabled": CONTEXT_ON,
        "symbol": "└─ ",
        "offset": CONTEXT_OFFSET,
    },
}

PRINTER_OVERRIDES = {
    "step": {
        "Main":   {"enabled": MAIN_STEP_ON},
        "Loader": {"enabled": LOADER_STEP_ON},
        "OPS":    {"enabled": OPS_STEP_ON},
    },
    # 其他 Printer 可日後擴充
}

# ==========================================================
# 📦 組合後的正式註冊表（供 print_rule_loader 使用）
# ==========================================================

PRINT_REGISTRY = {
    "indent_unit": INDENT_UNIT,
    "controller_level": CONTROLLER_LEVELS,
    "printer_rules": DEFAULT_PRINTER_RULES,
    "overrides": PRINTER_OVERRIDES,
    "label_map": LABEL_MAP,   # ✅ 新增這個欄位
}
