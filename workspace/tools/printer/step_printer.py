"""
Step Printer 工具模組（由註冊表完全控制）
功能：
    - 可由外部設定畫線開關、符號與縮排層級。
    - 支援「先空格 → 再畫線」的視覺格式。
    - 顯示名稱由註冊表注入（不再寫死）。
"""

_line_rule = None
_symbol_rule = None
_indent_rule = None
_label_map = {}  # ✅ 改成由外部注入


def set_line_rule(rule_func):
    global _line_rule
    _line_rule = rule_func


def set_symbol_rule(symbol_func):
    global _symbol_rule
    _symbol_rule = symbol_func


def set_indent_rule(indent_func):
    global _indent_rule
    _indent_rule = indent_func


def set_label_map(label_dict):
    """由 print_rule_loader 注入顯示名稱對應表"""
    global _label_map
    _label_map = label_dict or {}


def print_step(
    prefix: str,
    step_no: int,
    title: str,
    branch_state: list[bool] | None = None,
    is_last: bool = False,
):
    """印出統一格式的層級步驟（支援中文名稱顯示）"""
    branch_state = branch_state or []

    indent = _indent_rule(prefix, branch_state) if _indent_rule else ""
    show_line = _line_rule(prefix, step_no, title) if _line_rule else True
    branch_symbol = _symbol_rule(prefix, step_no, title, is_last) if (_symbol_rule and show_line) else ""

    # 自動在符號前補一格空白
    if branch_symbol and not branch_symbol.startswith(" "):
        branch_symbol = " " + branch_symbol

    # === 顯示名稱（從註冊表注入） ===
    label = _label_map.get(prefix, prefix)

    # === 最終印出格式 ===
    print(f"{indent}{branch_symbol}{label}Step {step_no}: {title}")
