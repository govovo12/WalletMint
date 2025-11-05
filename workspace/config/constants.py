"""
constants.py
專門存放後端協議相關的常量 (enums)。
這些值是後端定義的，屬於固定協議，不應該放進 .env。
"""

class TradeStatus:
    """交易狀態 (後端協議枚舉)"""
    PENDING = 1       # 待審核
    PROCESSING = 2    # 處理中
    SUCCESS = 3       # 成功
    FAIL = 4          # 失敗
    CANCEL = 5        # 取消
