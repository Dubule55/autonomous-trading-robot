from dataclasses import dataclass


@dataclass
class StrategyConfig:
    fast_ema: int = 12
    slow_ema: int = 26
    rsi_window: int = 14
    atr_window: int = 14
    stop_loss_atr: float = 2.0
    max_position_percent: float = 0.25
