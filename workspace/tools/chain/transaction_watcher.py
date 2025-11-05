# workspace/tools/chain/transaction_watcher.py

import asyncio
from workspace.config.error_code import ResultCode


class TransactionWatcher:
    def __init__(self, client):
        self.client = client

    async def watch_confirm_async(
        self,
        txid: str,
        blocks: int = 19,
        timeout: int = 180,
        interval: int = 3
    ):
        """
        純 async 版：監聽交易是否完成指定數量的區塊確認
        - 每過 interval 秒查一次
        - 呼叫端用 async for 逐筆拿結果
        yield: (tx_info, code, confirmed_blocks)
        """
        confirmed_blocks = 0
        elapsed = 0
        loop = asyncio.get_running_loop()

        while elapsed < timeout:
            try:
                # client.get_transaction_info 是同步的 → 用 executor 包起來
                tx_info = await loop.run_in_executor(
                    None, lambda: self.client.get_transaction_info(txid)
                )
            except Exception:
                yield None, ResultCode.tools_watcher_error, confirmed_blocks
                return

            if not tx_info:
                # 還沒進塊
                yield None, ResultCode.tools_watcher_pending, confirmed_blocks
            else:
                # 如果回傳是 dict，就從欄位抓確認數；否則手動加 1
                if isinstance(tx_info, dict):
                    confirmed_blocks = tx_info.get("confirmed_blocks", confirmed_blocks + 1)
                else:
                    confirmed_blocks += 1

                yield tx_info, ResultCode.SUCCESS, confirmed_blocks

                if confirmed_blocks >= blocks:
                    return  # 已達指定確認數，結束

            await asyncio.sleep(interval)
            elapsed += interval

        # 超時
        yield None, ResultCode.tools_watcher_timeout, confirmed_blocks
