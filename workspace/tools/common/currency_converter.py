# workspace/tools/common/currency_converter.py
"""
Currency Converter 工具模組
支援 TRX / USDT / USDD 之間的換算
"""

import requests
from workspace.config.error_code import ResultCode


class CurrencyConverter:
    SUPPORTED = ["TRX", "USDT", "USDD"]

    def __init__(self):
        # 緩存匯率 (單位: 1 token = ? USD)
        self.rates: dict[str, float] = {}

    def fetch_rates(self) -> int:
        """
        從 CoinGecko 抓取最新匯率
        :return: ResultCode
        """
        try:
            url = "https://api.coingecko.com/api/v3/simple/price"
            params = {
                "ids": "tron,tether,usdd",
                "vs_currencies": "usd",
            }
            resp = requests.get(url, params=params, timeout=5)
            data = resp.json()

            self.rates = {
                "TRX": data["tron"]["usd"],
                "USDT": data["tether"]["usd"],
                "USDD": data["usdd"]["usd"],
            }
            return ResultCode.SUCCESS
        except Exception:
            return ResultCode.tools_currency_fetch_error

    def convert(self, amount: float, from_token: str, to_token: str) -> tuple[float | None, int]:
        """
        幣別互轉
        :param amount: 數量
        :param from_token: 來源幣種 (TRX / USDT / USDD)
        :param to_token: 目標幣種
        :return: (換算後數量, ResultCode)
        """
        from_token = from_token.upper()
        to_token = to_token.upper()

        if from_token not in self.SUPPORTED or to_token not in self.SUPPORTED:
            return None, ResultCode.tools_currency_not_supported

        try:
            if from_token not in self.rates or to_token not in self.rates:
                return None, ResultCode.tools_currency_fetch_error

            usd_value = amount * self.rates[from_token]   # 換成美金
            result = usd_value / self.rates[to_token]     # 美金換成目標幣
            return result, ResultCode.SUCCESS
        except Exception:
            return None, ResultCode.tools_currency_convert_error
