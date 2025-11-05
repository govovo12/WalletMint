from workspace.tools.printer.live_display import run_live_display
from workspace.config.error_code import ResultCode
from rich.table import Table

def wait_for_sync(context: dict, wait_seconds: int = 140) -> tuple[dict, int]:
    """
    任務模組: 等待後台同步寫入交易紀錄
    :param context: 總控傳入的上下文
    :param wait_seconds: 等待秒數 (預設 140)
    :return: (context, ResultCode.SUCCESS)
    """

    def make_table(remaining: int) -> Table:
        table = Table(title="後台同步倒數")
        table.add_column("狀態", justify="left")
        table.add_column("剩餘秒數", justify="right")
        table.add_row("等待寫入", f"{remaining} 秒")
        return table

    run_live_display("後台同步倒數", make_table, wait_seconds)

    return context, ResultCode.SUCCESS
