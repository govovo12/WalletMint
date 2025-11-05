def calc_fee_and_realquant(quant: int, fee_percent: int, fee_gold: float) -> tuple[float, float]:
    """
    根據交易數量、費率百分比、固定手續費計算
    回傳 (fee, real_quant)
    """
    fee = quant * (fee_percent / 100.0) + fee_gold
    real_quant = quant - fee
    return round(fee, 8), round(real_quant, 8)
