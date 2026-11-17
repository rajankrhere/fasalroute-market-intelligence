# FasalRoute - M5 Market Analytics

This folder contains the M5 implementation for Net Realisable Price (netback), market comparison, a cautious baseline forecast, charts and tests.

## Modules

- netback.py: validates inputs and calculates expected sale value, total costs, net realisation and netback per quintal.
- market_comparison.py: ranks comparable selling options and explains the result.
- forecast.py: simple moving-average baseline and rolling mean absolute error (MAE).
- price_chart.py: optional chart helper for real historical observations.
- test_netback.py: automated tests.

## Units and formula

Prices and netback are INR per quintal; quantity is in quintals; costs are INR; spoilage is a fraction from 0 to 1.

Expected sale value = quoted price per quintal x quantity x (1 - spoilage rate)

Net realisation = expected sale value - transport - handling/packaging - commission - storage - other costs

Netback per quintal = net realisation / quantity

Every cost must be supplied explicitly. Enter zero only when a cost is confirmed not to apply; missing costs must not silently become zero.

## Quick example

    from analytics.netback import MarketOption, calculate_netback
    option = MarketOption(
        name="Example market (illustrative inputs)",
        price_per_quintal=2000,
        quantity_quintals=10,
        transport_cost=1000,
        handling_packaging_cost=200,
        commission_cost=100,
        storage_cost=0,
        spoilage_rate=0.05,
        other_cost=0,
    )
    result = calculate_netback(option)
    print(result.net_realisation, result.netback_per_quintal)

These example values are illustrative only, not actual mandi data or a buyer offer.

## Run tests

From the repository root:

    python -m unittest discover -s . -p 'test_*.py' -v

No third-party package is needed for calculator, comparison, forecast or tests. Charts require Matplotlib:

    python -m pip install matplotlib

## Forecast and data integrity

Use ordered observations for the same crop, variety, market, grade and unit. The moving average is a simple baseline, not an assured prediction. Check MAE and show observation dates, source and data gaps. If history is too short or inconsistent, do not show a forecast.

Do not present illustrative values as live or verified mandi prices. Keep source, observation date/time, market, commodity, variety, grade and unit with every price record. Compare options for the same produce lot and quantity; pass only options already checked as feasible. Show estimated costs and spoilage assumptions to the farmer.

This module does not fetch AGMARKNET/e-NAM data, verify buyer offers, calculate route distances or confirm storage availability. Those inputs must come from the data/backend workflow. A highest-netback result is a decision aid, not a guarantee of sale, payment or future price.
