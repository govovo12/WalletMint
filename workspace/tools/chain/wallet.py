# workspace/tools/chain/wallet.py
from tronpy.keys import PrivateKey
import base58
from workspace.config.error_code import ResultCode


class Wallet:
    def __init__(self, private_key_hex: str):
        """
        建立錢包實例
        :param private_key_hex: 16進位字串格式的私鑰
        """
        try:
            self._private_key = PrivateKey(bytes.fromhex(private_key_hex))
        except Exception:
            # 私鑰格式錯誤
            self._private_key = None
            self._error = ResultCode.tools_wallet_invalid_private_key
        else:
            self._error = ResultCode.SUCCESS

    def get_error(self) -> int:
        """取得初始化時的錯誤碼"""
        return self._error

    def get_address(self) -> str | None:
        """取得地址（若私鑰有誤則回傳 None）"""
        if self._private_key:
            return self._private_key.public_key.to_base58check_address()
        return None

    def get_private_key(self) -> PrivateKey | None:
        """取得私鑰物件（tronpy.keys.PrivateKey）"""
        return self._private_key

    def get_private_key_hex(self) -> str | None:
        """取得私鑰字串 (64 字元 hex)"""
        if self._private_key:
            return self._private_key.hex()
        return None


def is_valid_address(address: str) -> int:
    """
    驗證地址是否合法
    :param address: TRON 錢包地址
    :return: ResultCode.SUCCESS or ResultCode.tools_wallet_invalid_address
    """
    try:
        base58.b58decode_check(address)
        return ResultCode.SUCCESS
    except Exception:
        return ResultCode.tools_wallet_invalid_address


def mask_private_key(key: str) -> tuple[str | None, int]:
    """
    遮罩私鑰（Debug 用）
    :param key: 原始私鑰字串
    :return: (遮罩後字串, ResultCode)
    """
    try:
        if len(key) <= 10:
            return key, ResultCode.SUCCESS
        return key[:6] + "..." + key[-4:], ResultCode.SUCCESS
    except Exception:
        return None, ResultCode.tools_wallet_mask_error
