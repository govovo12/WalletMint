# main.py
"""
BatchForge / AdminSeed 專案入口檔
只負責：解析 CLI、列出任務、呼叫對應控制器/任務。
"""

import argparse
from workspace.config.task_registry import get_task
from workspace.config.print_registry import PRINT_REGISTRY
from workspace.tools.loader.print_rule_loader import apply_global_print_rules


def main():
    parser = argparse.ArgumentParser(description="🔧 後台批次建立工具入口檔")
    parser.add_argument("category", choices=["task", "controller", "tool", "list"], help="任務類型或 'list'")
    parser.add_argument("id", nargs="?", help="任務/控制器/工具 ID（list 模式可省略）")

    # 仍保留 CLI 旗標；實際判斷交由 debug_helper.is_debug() 在各層處理
    debug_group = parser.add_mutually_exclusive_group()
    debug_group.add_argument("--debug", action="store_true", help="強制開啟除錯模式")
    debug_group.add_argument("--no-debug", action="store_true", help="強制關閉除錯模式")

    # ✅ 新增：指定「總控」執行到第幾步（目前支援 1 或 2）
    parser.add_argument(
        "--step",
        type=int,
        choices=[1, 2],
        help="指定總控執行到的步驟（僅在 controller main 有效）"
    )

    args = parser.parse_args()

    # 列表模式
    from workspace.config import task_registry
    if args.category == "list":
        print("\n📜 可用任務清單：\n")
        for cat, mapping in task_registry.TASK_REGISTRY.items():
            if mapping:
                print(f"[{cat}]")
                for name in mapping.keys():
                    print(f"  - {name}")
        print()
        return

    # 取得任務/控制器
    task_func = get_task(args.category, args.id)
    if not task_func:
        print(f"❌ 找不到 {args.category}:{args.id}")
        return

    # 初始化 Printer 規則
    apply_global_print_rules(PRINT_REGISTRY)

    # ✅ 執行：僅在 controller main 考慮 --step；其餘完全不動
    if args.category == "controller" and args.id == "main" and args.step is not None:
        # 為了相容尚未改簽名的總控：若不接受 max_step，就退回不帶參數
        try:
            task_func(max_step=args.step)
        except TypeError:
            task_func()
    else:
        task_func()


if __name__ == "__main__":
    main()
