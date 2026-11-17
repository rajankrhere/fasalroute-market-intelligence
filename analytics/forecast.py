"""Simple moving-average baseline; inputs must be comparable INR/quintal observations."""
import math

def _validated(prices):
    values = list(prices)
    if any(not isinstance(x, (int, float)) or not math.isfinite(x) or x < 0 for x in values):
        raise ValueError("Prices must be finite, non-negative numbers.")
    return values

def moving_average_forecast(prices, window=3):
    """Forecast next observation using the mean of the latest window values."""
    values = _validated(prices)
    if not isinstance(window, int) or window < 2:
        raise ValueError("window must be an integer of at least 2.")
    if len(values) < window:
        raise ValueError(f"At least {window} observations are required.")
    return sum(values[-window:]) / window

def evaluate_moving_average_mae(prices, window=3):
    """Return rolling one-step mean absolute error for a historical series."""
    values = _validated(prices)
    if not isinstance(window, int) or window < 2:
        raise ValueError("window must be an integer of at least 2.")
    if len(values) <= window:
        raise ValueError("Need more than window observations to calculate MAE.")
    errors = []
    for index in range(window, len(values)):
        prediction = sum(values[index-window:index]) / window
        errors.append(abs(values[index] - prediction))
    return sum(errors) / len(errors)
