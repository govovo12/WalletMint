from workspace.config.error_code import ResultCode
from tronpy import Tron
from tronpy.providers import HTTPProvider  # 新增

class TronBroadcaster:
    @staticmethod
    def broadcast_transaction(signed_tx, node_url: str | None = None):
        """
        廣播交易到節點
        :param signed_tx: 已簽名交易
        :param node_url: 例如 https://nile.trongrid.io
        :return: (txid, ok, code)
        """
        if not signed_tx:
            return None, False, ResultCode.tools_broadcaster_invalid_tx

        try:
            client = Tron(provider=HTTPProvider(node_url)) if node_url else Tron()  # ★ 用同一個節點
            result = client.broadcast(signed_tx)

            # 節點有回應但拒絕
            if isinstance(result, dict) and not result.get("result"):
                return result.get("txid"), False, ResultCode.tools_broadcaster_broadcast_error

            # 成功
            return result.get("txid"), True, ResultCode.SUCCESS

        except Exception:
            # 未知/網路等例外（仍維持 1182）
            return None, False, ResultCode.tools_broadcaster_error
