"""
共用任務模組：common_task.py（正式版）
功能：
    - 建立共用 Headers（Sid / Uuid）
    - 統一發送 API 請求（使用 Requester + ResponseParser）
"""

from workspace.tools.request.requester import Requester
from workspace.tools.response.parser import ResponseParser
from workspace.config.error_code import ResultCode


def build_common_headers(context: dict, role: str, index: int = 0, extra: dict = None) -> dict:
    """建立角色共用 Header（自動帶入 Sid / Uuid）"""
    headers = {"Content-Type": "application/json"}
    key_map = {"OPS": "Sid", "MERCHANT": "Sid", "AGENT": "Sid"}

    common = context.get("COMMON", {})
    data = common.get(role)

    if isinstance(data, list) and index < len(data):
        entry = data[index]
    elif isinstance(data, dict):
        entry = data
    else:
        entry = {}

    session_id = entry.get("SESSION_ID") or entry.get("SSID")
    uuid = entry.get("UUID")

    if session_id:
        key = key_map.get(role, "Sid")
        headers[key] = session_id
    if uuid:
        headers["Uuid"] = uuid

    if extra:
        headers.update(extra)

    return headers


def send_api_request(
    context: dict,
    role: str,
    url: str,
    payload: dict | None = None,
    method: str = "POST",
    use_header: bool = True,
    timeout: int = 5,
) -> tuple[dict, int]:
    """
    統一 API 呼叫接口：
    - 自動建立 Headers
    - 呼叫 Requester.{get|post|put}
    - 用 ResponseParser 解析 JSON
    - 統一回傳 (data, ResultCode)
    """
    headers = build_common_headers(context, role) if use_header else {}

    # === Step 1. 選擇正確 HTTP 方法 ===
    method = method.upper()
    if method == "GET":
        resp, code = Requester.get(url, params=payload, headers=headers, timeout=timeout)
    elif method == "PUT":
        resp, code = Requester.put(url, json=payload, headers=headers, timeout=timeout)
    else:
        resp, code = Requester.post(url, json=payload, headers=headers, timeout=timeout)

    # === Step 2. 若 Requester 層就失敗，直接回傳 ===
    if code != ResultCode.SUCCESS or resp is None:
        return {}, code

    # === Step 3. 驗證 HTTP 狀態 ===
    status_code = ResponseParser.check_status(resp)
    if status_code != ResultCode.SUCCESS:
        return {}, status_code

    # === Step 4. 嘗試解析 JSON ===
    data, parse_code = ResponseParser.parse_json(resp)
    if parse_code != ResultCode.SUCCESS:
        return {}, parse_code

    return data or {}, ResultCode.SUCCESS
