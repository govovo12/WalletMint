# workspace/config/api_paths.py
"""
後台 API 端點設定表
提供各後台共用的登入路徑與後續操作端點。
"""

LOGIN_PATHS = {
    "OPS": "/operator/login",
    "AGENT": "/agent/login",
    "MERCHANT": "/merchant/login",
}

ENDPOINTS = {
    # 新增代理商帳號
    "CREATE_AGENT_ACCOUNT": "/operator/agent",

    # 查詢代理商帳號
    "QUERY_AGENT_ACCOUNT": "/operator/agent/list",

    # 新增商戶帳號
    "CREATE_MERCHANT_ACCOUNT": "/operator/merchant",

    # 查詢商戶帳號
    "QUERY_MERCHANT_ACCOUNT": "/operator/merchant/list",
}
