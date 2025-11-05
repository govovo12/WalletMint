import pyotp
from workspace.config.error_code import ResultCode


def generate_otp(secret: str, digits: int = 6, interval: int = 30) -> tuple[str | None, int]:
    """
    根據 Secret Key 產生動態 OTP
    :param secret: Base32 格式的 Secret Key
    :param digits: OTP 位數 (預設 6)
    :param interval: OTP 更新間隔 (秒) (預設 30)
    :return: (OTP, ResultCode)
    """
    try:
        if not secret:
            return None, ResultCode.tools_otp_invalid_secret

        totp = pyotp.TOTP(secret, digits=digits, interval=interval)
        return totp.now(), ResultCode.SUCCESS
    except Exception:
        return None, ResultCode.tools_otp_generate_error


def verify_otp(secret: str, otp: str, digits: int = 6, interval: int = 30) -> tuple[bool, int]:
    """
    驗證使用者輸入的 OTP 是否正確
    :param secret: Base32 格式的 Secret Key
    :param otp: 使用者輸入的 OTP
    :param digits: OTP 位數 (預設 6)
    :param interval: OTP 更新間隔 (秒) (預設 30)
    :return: (驗證結果, ResultCode)
    """
    try:
        if not secret:
            return False, ResultCode.tools_otp_invalid_secret

        totp = pyotp.TOTP(secret, digits=digits, interval=interval)
        return totp.verify(otp), ResultCode.SUCCESS
    except Exception:
        return False, ResultCode.tools_otp_verify_error
