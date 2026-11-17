"""Optional chart helper for verified historical mandi price observations."""
def plot_price_trend(records, output_path, market_label="Market", source_note=""):
    """Save a date-versus-price chart. Records need date and price_per_quintal keys."""
    records = list(records)
    if not records:
        raise ValueError("At least one price observation is required.")
    dates = [record["date"] for record in records]
    prices = [float(record["price_per_quintal"]) for record in records]
    if any(price < 0 for price in prices):
        raise ValueError("Prices cannot be negative.")
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise RuntimeError("Install chart dependency with: python -m pip install matplotlib") from exc
    figure, axis = plt.subplots(figsize=(9, 5))
    axis.plot(dates, prices, marker="o", linewidth=1.8)
    axis.set_title(f"Historical mandi price trend - {market_label}")
    axis.set_xlabel("Observation date")
    axis.set_ylabel("Reported price (INR per quintal)")
    axis.grid(True, alpha=0.3)
    if source_note:
        figure.text(0.01, 0.01, f"Source / data note: {source_note}", fontsize=8)
        figure.tight_layout(rect=(0, 0.05, 1, 1))
    else:
        figure.tight_layout()
    figure.savefig(output_path, dpi=150)
    plt.close(figure)
