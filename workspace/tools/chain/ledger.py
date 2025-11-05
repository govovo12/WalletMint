from workspace.config.error_code import ResultCode
import requests


class Ledger:
    def __init__(self, client):
        self.client = client

    def get_trc20_balance(self, address: str, contract_address: str):
        """
        查詢 TRC20 餘額（優先使用 tronpy 合約介面）
        """
        try:
            if not contract_address or not address:
                return None, ResultCode.tools_ledger_trc20_invalid_contract

            # 用 tronpy 直接取合約
            contract = self.client.client.get_contract(contract_address)
            balance = contract.functions.balanceOf(address)



            # 預設 USDT 6 位小數
            return balance / (10 ** 6), ResultCode.SUCCESS

        except Exception as e:
            
            return None, ResultCode.tools_ledger_trc20_balance_error

    def get_trc20_balance_with_fallback(self, address: str, contract_address: str, symbol: str = "USDT"):
        """
        查 TRC20 餘額：
        - 測試網 (Nile/Shasta) → 只用 RPC (tronpy contract.functions)
        - 主網 → RPC 失敗才打 Tronscan API
        """
        balance, code = self.get_trc20_balance(address, contract_address)
        if code == ResultCode.SUCCESS and balance is not None:
            return balance, code

        if "nile" in self.client.node_url or "shasta" in self.client.node_url:
            return None, ResultCode.tools_ledger_trc20_balance_error

        try:
            url = f"https://apilist.tronscanapi.com/api/account/tokens?address={address}"
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                tokens = data.get("data", [])
                for t in tokens:
                    if (
                        t.get("tokenAbbr") == symbol
                        or t.get("tokenId") == contract_address
                        or t.get("tokenName") == symbol
                    ):
                        raw_balance = float(t.get("balance", 0))
                        decimals = int(t.get("tokenDecimal", 6))
                        print(f"[DEBUG][Ledger] Tronscan Raw balance({address}) = {raw_balance}")
                        return raw_balance / (10 ** decimals), ResultCode.SUCCESS
            return None, ResultCode.tools_ledger_trc20_balance_error
        except Exception as e:
            
            return None, ResultCode.tools_ledger_trc20_balance_error
