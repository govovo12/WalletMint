# workspace/tools/printer/live_display.py

import asyncio
import time
from rich.live import Live
from rich.table import Table
from typing import Callable, Awaitable


def run_live_display(
    title: str,
    make_table: Callable[[int], Table],
    total_steps: int,
    refresh_per_second: int = 2,
):
    """
    通用即時顯示工具 (同步版，適合倒數等待)
    :param title: 顯示用標題
    :param make_table: 建立表格的方法，參數為剩餘數字，回傳 Table
    :param total_steps: 總倒數次數
    :param refresh_per_second: 每秒刷新次數
    """
    with Live(make_table(total_steps), refresh_per_second=refresh_per_second) as live:
        for remaining in range(total_steps, 0, -1):
            time.sleep(1)
            live.update(make_table(remaining - 1))


async def run_live_display_async(
    make_table: Callable[[], Table],
    task_coro: Awaitable,
    refresh_per_second: int = 2,
):
    """
    通用即時顯示工具 (async 版本，適合區塊確認等長時間任務)
    :param make_table: 建立表格的方法 (無參數)，回傳 Table
    :param task_coro: 要執行的 async 任務 (例如 confirm_all())
    :param refresh_per_second: 每秒刷新次數
    :return: 任務回傳值
    """
    with Live(make_table(), refresh_per_second=refresh_per_second) as live:
        task = asyncio.create_task(task_coro)

        while not task.done():
            await asyncio.sleep(1)
            live.update(make_table())

        return await task
