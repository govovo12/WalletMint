"""
TRON Transaction Builder 工具
使用 tronpy 建立 raw transaction
"""

from workspace.config.error_code import ResultCode
from workspace.tools.chain.client import TronClient


class TronBuilder:
    @staticmethod
    def build_transfer_tx(client: TronClient, from_address: str, to_address: str, amount: int):
        """
        建立 TRX 轉帳交易的 raw transaction (未簽名)
        :param client: TronClient 實例
        :param from_address: 來源地址
        :param to_address: 目標地址
        :param amount: 金額 (單位: Sun)
        :return: (raw_tx, ResultCode)
        """
        try:
            if not from_address or not to_address or amount <= 0:
                return None, ResultCode.tools_builder_invalid_params

            txn = client.client.trx.transfer(from_address, to_address, amount).build()
            return txn, ResultCode.SUCCESS

        except Exception:
            return None, ResultCode.tools_builder_error

    # ---------------- TRC20 專用 ----------------

    @staticmethod
    def get_trc20_contract(client: TronClient, contract_address: str):
        """
        取得 TRC20 合約
        :param client: TronClient 實例
        :param contract_address: TRC20 合約地址
        :return: (contract, ResultCode)
        """
        try:
            if not contract_address:
                return None, ResultCode.tools_builder_invalid_params

            contract = client.client.get_contract(contract_address)

            # 檢查是否有 transfer 方法
            if not hasattr(contract.functions, "transfer"):
                return None, ResultCode.tools_builder_trc20_invalid_method

            return contract, ResultCode.SUCCESS

        except Exception:
            return None, ResultCode.tools_builder_trc20_invalid_contract

    @staticmethod
    def build_trc20_transfer_tx(contract, from_address: str, to_address: str, amount: int):
        """
        建立 TRC20 (例如 USDT) 轉帳交易的 raw transaction (未簽名)
        :param contract: TRC20 合約物件 (先用 get_trc20_contract 取得)
        :param from_address: 來源地址
        :param to_address: 目標地址
        :param amount: 金額 (單位: token 的最小單位，例如 USDT=10^6)
        :return: (raw_tx, ResultCode)
        """
        try:
            if not contract or not from_address or not to_address or amount <= 0:
                return None, ResultCode.tools_builder_invalid_params

            txn = (
                contract.functions.transfer(to_address, int(amount * (10 ** 6)))  # USDT 預設 6 位小數
                .with_owner(from_address)
                .fee_limit(5_000_000)
                .build()
            )
            return txn, ResultCode.SUCCESS

        except Exception:
            return None, ResultCode.tools_builder_trc20_error
