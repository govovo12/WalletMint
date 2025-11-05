from workspace.config.error_code import ResultCode


class ResponseParser:
    @staticmethod
    def check_status(resp):
        """檢查 HTTP 狀態碼"""
        if resp is None:
            return ResultCode.tools_response_none
        if 200 <= resp.status_code < 300:
            return ResultCode.SUCCESS
        return ResultCode.tools_response_bad_status

    @staticmethod
    def parse_json(resp):
        """嘗試解析 JSON"""
        try:
            return resp.json(), ResultCode.SUCCESS
        except Exception:
            return None, ResultCode.tools_response_json_error

    @staticmethod
    def get_field(data: dict, *keys):
        """安全取欄位，例如 get_field(data, "result", "txID")"""
        try:
            for k in keys:
                data = data[k]
            return data, ResultCode.SUCCESS
        except Exception:
            return None, ResultCode.tools_response_field_missing
