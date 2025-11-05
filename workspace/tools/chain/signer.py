from tronpy.keys import PrivateKey
from workspace.config.error_code import ResultCode


class TronSigner:
    @staticmethod
    def sign_transaction(raw_tx, private_key: PrivateKey):
        """
        簽署交易
        :param raw_tx: 未簽名交易 (tronpy Transaction 物件)
        :param private_key: 私鑰 (tronpy.keys.PrivateKey 物件)
        :return: (signed_tx, ResultCode)
        """
        try:
            if not isinstance(private_key, PrivateKey):
                return None, ResultCode.tools_signer_invalid_private_key

            signed_tx = raw_tx.sign(private_key)
            return signed_tx, ResultCode.SUCCESS

        except Exception:
            return None, ResultCode.tools_signer_sign_error
