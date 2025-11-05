"""
TRON Client 工具
負責鏈上資料查詢：帳號、餘額、交易、區塊
"""

from tronpy import Tron
from workspace.config.error_code import ResultCode


class TronClient:
    def __init__(self, node_url: str = "https://nile.trongrid.io"):
        """
        TRON Client 包裝器
        :param node_url: 節點 URL，例如 https://nile.trongrid.io 或 https://api.trongrid.io
        """
        self.node_url = node_url

        # 自動判斷 network，傳給 tronpy
        if "nile" in node_url:
            self.client = Tron(network="nile")
        elif "shasta" in node_url:
            self.client = Tron(network="shasta")
        else:
            self.client = Tron(network="mainnet")

    def get_account(self, address: str):
        """
        查詢帳號資訊
        :param address: TRON 地址
        :return: (account_info, ResultCode)
        """
        try:
            account = self.client.get_account(address)
            return account, ResultCode.SUCCESS
        except Exception:
            return None, ResultCode.tools_client_account_not_found

    def get_balance(self, address: str):
        """
        查詢 TRX 餘額
        :param address: TRON 地址
        :return: (balance, ResultCode)
        """
        try:
            balance = self.client.get_account_balance(address)
            return balance, ResultCode.SUCCESS
        except Exception:
            return None, ResultCode.tools_client_balance_error

    def get_transaction_info(self, txid: str):
        try:
            tx_info = self.client.get_transaction_info(txid)

            # txid 查無資料
            if not tx_info:
                return None, ResultCode.tools_client_tx_receipt_error

            return tx_info, ResultCode.SUCCESS

        except ConnectionError:
            # 節點連線失敗
            return None, ResultCode.tools_client_network_error

        except Exception:
            # 其他未歸類例外
            return None, ResultCode.tools_client_unknown_error


    def get_latest_block_number(self):
        """
        查詢最新區塊號
        :return: (block_number, ResultCode)
        """
        try:
            latest_block = self.client.get_latest_block()
            block_number = latest_block["block_header"]["raw_data"]["number"]
            return block_number, ResultCode.SUCCESS
        except Exception:
            return None, ResultCode.tools_client_block_error

    def get_transaction_receipt(self, txid: str):
        """
        查詢交易回執（包含 blockNumber）
        :param txid: 交易 ID
        :return: (tx_receipt, ResultCode)
        """
        try:
            tx_receipt = self.client.get_transaction(txid)
            # 確認至少有 blockNumber，才算有效
            if not tx_receipt or "raw_data" not in tx_receipt:
                return None, ResultCode.tools_client_tx_receipt_error
            return tx_receipt, ResultCode.SUCCESS
        except Exception:
            return None, ResultCode.tools_client_tx_receipt_error

