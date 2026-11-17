"""Compare feasible selling options using netback, not quoted price alone."""
from .netback import MarketOption, calculate_netback

def compare_markets(options):
    """Rank options for the same produce lot and quantity. Caller checks feasibility."""
    options = list(options)
    if not options:
        raise ValueError("At least one market option is required.")
    if not all(isinstance(item, MarketOption) for item in options):
        raise TypeError("Every item must be a MarketOption.")
    quantity = options[0].quantity_quintals
    if any(item.quantity_quintals != quantity for item in options):
        raise ValueError("Compare markets using the same quantity in quintals.")
    return sorted((calculate_netback(item) for item in options), key=lambda item: item.netback_per_quintal, reverse=True)

def explain_recommendation(ranked_results):
    """Explain why the first ranked option leads, including that it is only an estimate."""
    ranked_results = list(ranked_results)
    if not ranked_results:
        raise ValueError("No market results available to explain.")
    best = ranked_results[0]
    message = (f"{best.market_name} has the highest estimated net realisation "
               f"({best.netback_per_quintal:.2f} INR per quintal) among the options compared. "
               f"Expected sale value: {best.expected_sale_value:.2f} INR; "
               f"listed costs: {best.total_costs:.2f} INR.")
    if len(ranked_results) > 1:
        second = ranked_results[1]
        difference = best.netback_per_quintal - second.netback_per_quintal
        if difference == 0:
            message += " It is tied with the next option; verify non-price factors before choosing."
        else:
            message += f" It is ahead of {second.market_name} by {difference:.2f} INR per quintal."
    return message + " This is an estimate based on entered inputs, not a guaranteed sale price."
