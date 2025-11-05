import requests
import urllib3
from workspace.config.error_code import ResultCode

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Requester:
    """HTTP 請求工具模組（強化版）"""

    @staticmethod
    def _check_response(resp):
        """共用的 HTTP 狀態檢查"""
        if not resp.ok:  # 非 2xx 狀態碼
            print(f"[❌ Requester] HTTP 請求失敗 → {resp.status_code} {resp.reason}")
            return None, ResultCode.tools_request_error
        return resp, ResultCode.SUCCESS

    @staticmethod
    def get(url, params=None, headers=None, timeout=5):
        """發送 GET 請求"""
        try:
            resp = requests.get(url, params=params, headers=headers, timeout=timeout, verify=False)
            return Requester._check_response(resp)
        except requests.Timeout:
            return None, ResultCode.tools_request_timeout
        except Exception:
            return None, ResultCode.tools_request_error

    @staticmethod
    def post(url, data=None, json=None, headers=None, timeout=5):
        """發送 POST 請求"""
        try:
            resp = requests.post(url, data=data, json=json, headers=headers, timeout=timeout, verify=False)
            return Requester._check_response(resp)
        except requests.Timeout:
            return None, ResultCode.tools_request_timeout
        except Exception:
            return None, ResultCode.tools_request_error

    @staticmethod
    def put(url, data=None, json=None, headers=None, timeout=5):
        """發送 PUT 請求"""
        try:
            resp = requests.put(url, data=data, json=json, headers=headers, timeout=timeout, verify=False)
            return Requester._check_response(resp)
        except requests.Timeout:
            return None, ResultCode.tools_request_timeout
        except Exception:
            return None, ResultCode.tools_request_put_error
