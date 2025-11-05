import json

_line_rule = None
_symbol_rule = None
_indent_rule = None
_label_map = {}

def set_line_rule(rule_func):  global _line_rule; _line_rule = rule_func
def set_symbol_rule(rule_func):  global _symbol_rule; _symbol_rule = rule_func
def set_indent_rule(rule_func):  global _indent_rule; _indent_rule = rule_func
def set_label_map(label_dict):  global _label_map; _label_map = label_dict or {}

def print_context(
    context: dict,
    prefix: str,
    step_no: int | None = None,
    branch_state: list[bool] | None = None,
    is_last: bool = False,
):
    branch_state = branch_state or []
    indent = _indent_rule(prefix, branch_state) if _indent_rule else ""
    show_line = _line_rule(prefix, step_no or 0, "context") if _line_rule else True
    branch_symbol = _symbol_rule(prefix, step_no or 0, "context", is_last) if (_symbol_rule and show_line) else ""

    if branch_symbol and not branch_symbol.startswith(" "):
        branch_symbol = " " + branch_symbol

    label = _label_map.get(prefix, prefix)

    # === 標題行 ===
    if step_no is not None:
        title = f"{label}Step {step_no} 結束時 Context 狀態："
    else:
        title = f"{label} 控制器 Context 狀態："
    print(f"{indent}{branch_symbol}{title}")

    # === 印出 Context JSON ===
    if not context:
        print(f"{indent}  (空)")
        return

    formatted = json.dumps(context, indent=2, ensure_ascii=False)

    # ✅ 補上符號寬度 + 額外兩格縮排
    symbol_space = " " * len(branch_symbol)
    block_indent = indent + symbol_space + "  "

    for line in formatted.splitlines():
        print(f"{block_indent}{line}")
