"""
Error Printer 工具模組（穩定對齊版）
功能：
    - 自動補齊 emoji 寬度（確保符號等寬）
    - 符號統一以中括號包起 + 固定一格間距
    - 完全相容現有註冊表與 loader
"""

from workspace.config.error_code import (
    ResultCode,
    ERROR_MESSAGES,
    SUCCESS_CODES,
    TOOL_ERROR_CODES,
    TASK_ERROR_CODES,
    CTRL_ERROR_CODES,
)

_line_rule = None
_symbol_rule = None
_indent_rule = None


def set_line_rule(rule_func):  global _line_rule; _line_rule = rule_func
def set_symbol_rule(rule_func):  global _symbol_rule; _symbol_rule = rule_func
def set_indent_rule(rule_func):  global _indent_rule; _indent_rule = rule_func


# ==============================================================
# 🧩 emoji 寬度修正工具
# ==============================================================

def format_symbol(symbol: str, width: int = 3) -> str:
    """
    將 emoji 類符號補滿固定寬度（避免字寬不等）
    width=3 → 約等於 3 個半形字的空間
    """
    length = len(symbol.encode("utf-8")) // 3  # 粗略估算 emoji 寬度
    pad = max(0, width - length)
    return symbol + " " * pad


# ==============================================================
# 🧱 主印出邏輯
# ==============================================================

def print_result(code: int, branch_state: list[bool], prefix: str = "Main", is_last: bool = False):
    indent = _indent_rule(prefix, branch_state) if _indent_rule else ""
    show_line = _line_rule(prefix, 0, "error") if _line_rule else True
    branch_symbol = _symbol_rule(prefix, 0, "error", is_last) if (_symbol_rule and show_line) else ""

    if branch_symbol and not branch_symbol.startswith(" "):
        branch_symbol = " " + branch_symbol

    msg = ERROR_MESSAGES.get(code, f"未知錯誤碼: {code}")

    def render(symbol, text):
        """符號補齊對齊、視覺固定長度"""
        sym_fixed = format_symbol(symbol, width=2)  # 保留 2 寬度區
        return f"{indent}{branch_symbol}{sym_fixed}[{text}] code={code} msg={msg}"

    # --- 成功 ---
    if code in SUCCESS_CODES:
        print(render("✅", "成功"))
        return

    # --- 工具層錯誤 ---
    if code in TOOL_ERROR_CODES:
        print(render("⚠", "工具失敗"))
        return

    # --- 任務層錯誤 ---
    if code in TASK_ERROR_CODES:
        print(render("❌", "任務失敗"))
        return

    # --- 控制器層錯誤 ---
    if code in CTRL_ERROR_CODES:
        print(render("❌", "控制器失敗"))
        return

    # --- 其他未知錯誤 ---
    print(render("❌", "未知失敗"))

