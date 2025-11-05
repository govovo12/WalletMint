"""
Printer 規則載入器（支援數字縮排 + 覆寫 + 符號對齊版）
說明：
    - 自動結合控制器層級 + Printer 偏移。
    - 支援控制器覆寫（enabled/symbol）。
    - INDENT_UNIT 可為數字（空格數）或字串（例如 "\t"）。
    - 所有符號統一「空格 → 符號 → 文字」的視覺格式。
    - 自動注入 label_map（顯示名稱映射）給各 Printer。
"""

from workspace.tools.printer.step_printer import (
    set_line_rule as set_step_line,
    set_symbol_rule as set_step_symbol,
    set_indent_rule as set_step_indent,
    set_label_map as set_step_label,   # ✅ 新增
)
from workspace.tools.printer.debug_printer import (
    set_line_rule as set_debug_line,
    set_symbol_rule as set_debug_symbol,
    set_indent_rule as set_debug_indent,
)
from workspace.tools.printer.error_printer import (
    set_line_rule as set_error_line,
    set_symbol_rule as set_error_symbol,
    set_indent_rule as set_error_indent,
)
from workspace.tools.printer.context_printer import (
    set_line_rule as set_context_line,
    set_symbol_rule as set_context_symbol,
    set_indent_rule as set_context_indent,
    set_label_map as set_context_label,   # ✅ 新增
)


def apply_global_print_rules(registry: dict):
    """
    根據註冊表設定所有 Printer 規則。
    縮排 = 控制器層級 + Printer offset
    支援：
        - 數字型 INDENT_UNIT（自動轉為空格）
        - 控制器覆寫（enabled/symbol）
        - 符號自動補空格（確保先空格再畫線）
        - label_map 注入（顯示名稱）
    """

    # ------------------------------------------------------------
    # 取得縮排單位（數字 → 空格字串）
    # ------------------------------------------------------------
    indent_unit = registry.get("indent_unit", "  ")
    if isinstance(indent_unit, int):
        indent_unit = " " * indent_unit

    controller_levels = registry.get("controller_level", {})
    printer_rules = registry.get("printer_rules", {})
    overrides = registry.get("overrides", {})
    label_map = registry.get("label_map", {})  # ✅ 讀取 label_map

    # ------------------------------------------------------------
    # 規則合併（default + override + 符號前空格）
    # ------------------------------------------------------------
    def get_rule(print_type: str, prefix: str):
        base = printer_rules.get(print_type, {}).copy()
        over = overrides.get(print_type, {}).get(prefix, {})
        base.update(over)

        # 🔧 統一符號：確保前面多一格空白（視覺一致）
        symbol = base.get("symbol", "")
        if symbol and not symbol.startswith(" "):
            base["symbol"] = " " + symbol

        return base

    # ------------------------------------------------------------
    # 共用縮排計算函式
    # ------------------------------------------------------------
    def calc_indent(prefix: str, print_type: str):
        ctrl_level = controller_levels.get(prefix, 0)
        rule = get_rule(print_type, prefix)
        offset = rule.get("offset", 0)
        return indent_unit * (ctrl_level + offset)

    # ============================================================
    # Step Printer
    # ============================================================
    def step_line(prefix, step_no, title):
        rule = get_rule("step", prefix)
        return rule.get("enabled", False)

    def step_symbol(prefix, step_no, title, is_last):
        rule = get_rule("step", prefix)
        return rule.get("symbol", "")

    set_step_line(step_line)
    set_step_symbol(step_symbol)
    set_step_indent(lambda p, b: calc_indent(p, "step"))
    set_step_label(label_map)  # ✅ 注入 label_map

    # ============================================================
    # Debug Printer
    # ============================================================
    def debug_line(prefix, step_no, title):
        rule = get_rule("debug", prefix)
        return rule.get("enabled", False)

    def debug_symbol(prefix, step_no, title, is_last):
        rule = get_rule("debug", prefix)
        return rule.get("symbol", "")

    set_debug_line(debug_line)
    set_debug_symbol(debug_symbol)
    set_debug_indent(lambda p, b: calc_indent(p, "debug"))

    # ============================================================
    # Error Printer
    # ============================================================
    def error_line(prefix, step_no, title):
        rule = get_rule("error", prefix)
        return rule.get("enabled", False)

    def error_symbol(prefix, step_no, title, is_last):
        rule = get_rule("error", prefix)
        return rule.get("symbol", "")

    set_error_line(error_line)
    set_error_symbol(error_symbol)
    set_error_indent(lambda p, b: calc_indent(p, "error"))

    # ============================================================
    # Context Printer
    # ============================================================
    def context_line(prefix, step_no, title):
        rule = get_rule("context", prefix)
        return rule.get("enabled", False)

    def context_symbol(prefix, step_no, title, is_last):
        rule = get_rule("context", prefix)
        return rule.get("symbol", "")

    set_context_line(context_line)
    set_context_symbol(context_symbol)
    set_context_indent(lambda p, b: calc_indent(p, "context"))
    set_context_label(label_map)  # ✅ 注入 label_map
