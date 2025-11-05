"""
Debug Printer 工具模組（由註冊表完全控制）
功能：
    - 支援多層級縮排。
    - 所有畫線開關、符號與空格縮排皆由外部注入。
"""

_line_rule = None
_symbol_rule = None
_indent_rule = None


def set_line_rule(rule_func):  global _line_rule; _line_rule = rule_func
def set_symbol_rule(rule_func):  global _symbol_rule; _symbol_rule = rule_func
def set_indent_rule(rule_func):  global _indent_rule; _indent_rule = rule_func


def debug_print(debug: bool, message: str, prefix: str = "Main", branch_state: list[bool] | None = None, is_last: bool = False):
    if not debug:
        return

    branch_state = branch_state or []
    indent = _indent_rule(prefix, branch_state) if _indent_rule else ""
    show_line = _line_rule(prefix, 0, message) if _line_rule else True
    branch_symbol = _symbol_rule(prefix, 0, message, is_last) if (_symbol_rule and show_line) else ""

    if branch_symbol and not branch_symbol.startswith(" "):
        branch_symbol = " " + branch_symbol

    print(f"{indent}{branch_symbol}[DEBUG] {message}")
