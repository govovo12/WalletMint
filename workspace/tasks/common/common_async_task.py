"""
common_async_task.py
------------------------------------------------
📘 職責：
    - 從 context 依 mapping 自動組成 payload
    - 支援單筆與批次併發 API 發送
    - 回傳完整紀錄：method、url、headers、payload、response
------------------------------------------------
"""

import asyncio
from workspace.tools.request.requester import Requester
from workspace.tools.response.parser import ResponseParser
from workspace.config.error_code import ResultCode


# ============================================================
# 小工具：依路徑從 context 取值（支援直接值）
# ============================================================
def _extract_from_context(context: dict, path):
    """根據路徑 tuple 從 context 取值；若 path 非 tuple/list，視為字面值。"""
    if not isinstance(path, (tuple, list)):
        return path
    data = context
    for key in path:
        if not isinstance(data, dict) or key not in data:
            return None
        data = data[key]
    return data


# ============================================================
# 單筆發送：共用底層 API 執行單位
# ============================================================
async def send_api_request_async(
    context: dict,
    role: str,
    api_group: str,
    path_key: str,
    payload_source: dict,
    method: str = "POST",
    use_header: bool = True,
    header_type: str = "Sid",
    timeout: int = 10,
) -> tuple[int, list]:
    """
    通用 API 發送器 (單筆)
    Returns:
        (code, records)
    """
    records: list = []

    try:
        # === Step 1. 組出 URL ===
        api_section = context.get("API", {}).get(api_group, {})
        base_url = context["COMMON"].get("BACKEND_RA_BASE_URL", "")
        api_path = api_section.get(path_key, "")
        if not base_url or not api_path:
            records.append({
                "type": "error",
                "message": f"[{role}] 缺少 Base URL 或 API Path"
            })
            return ResultCode.task_invalid_context, records

        target_url = f"{base_url.rstrip('/')}/{api_path.lstrip('/')}"

        # === Step 2. 自動組 Payload ===
        payload = {field: _extract_from_context(context, path) for field, path in payload_source.items()}

        # === Step 3. 準備 Header ===
        headers = {}
        if use_header:
            ssid = context.get("COMMON", {}).get(role, {}).get("SSID")
            if ssid:
                headers[header_type] = ssid

        # === Step 4. 發送請求 ===
        resp, code = None, ResultCode.SUCCESS
        request_info = {
            "method": method.upper(),
            "url": target_url,
            "headers": headers,
            "payload": payload,
        }
        response_info = None

        try:
            if method.upper() == "POST":
                resp, code = Requester.post(target_url, json=payload, headers=headers, timeout=timeout)
            elif method.upper() == "GET":
                resp, code = Requester.get(target_url, params=payload, headers=headers, timeout=timeout)
            elif method.upper() == "PUT":
                resp, code = Requester.put(target_url, json=payload, headers=headers, timeout=timeout)
            else:
                records.append({
                    "type": "error",
                    "message": f"[{role}] 不支援的 HTTP 方法: {method}"
                })
                return ResultCode.task_api_failed, records

            if resp is not None:
                response_info = {
                    "status_code": getattr(resp, "status_code", None),
                    "text": getattr(resp, "text", None),
                }

        except Exception as e:
            code = ResultCode.task_api_failed
            records.append({
                "type": "error",
                "message": f"[{role}] 請求階段異常: {e}",
                "request": request_info
            })
            return code, records

        # === Step 5. 檢查 HTTP 層結果 ===
        if code != ResultCode.SUCCESS or resp is None:
            records.append({
                "type": "error",
                "message": f"[{role}] HTTP 請求失敗，ResultCode={code}",
                "request": request_info,
                "response": response_info
            })
            return code, records

        # === Step 6. 嘗試解析 JSON ===
        data, parse_code = ResponseParser.parse_json(resp)
        if parse_code != ResultCode.SUCCESS or data is None:
            records.append({
                "type": "error",
                "message": f"[{role}] 回傳非 JSON 格式",
                "request": request_info,
                "response": response_info
            })
            return ResultCode.task_api_failed, records

        # === Step 7. 成功紀錄 ===
        records.append({
            "type": "debug",
            "message": f"[{role}] API 請求完成 → {target_url}",
            "request": request_info,
            "response": {
                "status_code": getattr(resp, "status_code", None),
                "text": getattr(resp, "text", None),
                "parsed": data
            }
        })

        return ResultCode.SUCCESS, records

    except Exception as e:
        records.append({
            "type": "error",
            "message": f"[{role}] 發送 API 發生例外: {e}"
        })
        return ResultCode.task_api_failed, records


# ============================================================
# 新增：批次併發版（一次執行多筆名稱索引 API）
# ============================================================
async def send_batch_api_requests(
    context: dict,
    role: str,
    api_group: str,
    path_key: str,
    payload_sources: list[tuple[str, dict]],
    method: str = "POST",
    use_header: bool = True,
    header_type: str = "Sid",
    timeout: int = 10,
) -> list[tuple[str, int, list]]:
    """
    批次併發 API 發送器
    Args:
        payload_sources: [(name, payload_source), ...]
    Returns:
        [(name, code, records), ...]
    """
    async def _run_single(name, payload_source):
        code, records = await send_api_request_async(
            context=context,
            role=role,
            api_group=api_group,
            path_key=path_key,
            payload_source=payload_source,
            method=method,
            use_header=use_header,
            header_type=header_type,
            timeout=timeout,
        )
        return name, code, records

    tasks = [_run_single(name, src) for name, src in payload_sources]
    results = await asyncio.gather(*tasks)
    return results
