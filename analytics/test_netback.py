"""Run: python -m unittest discover -s . -p 'test_*.py' -v"""
import unittest
from analytics.netback import MarketOption, calculate_netback
from analytics.market_comparison import compare_markets, explain_recommendation
from analytics.forecast import moving_average_forecast, evaluate_moving_average_mae

def option(name="Market A", price=2000, quantity=10, transport=1000, handling=200, commission=100, storage=0, spoilage=0.0, other=0):
    return MarketOption(name, price, quantity, transport, handling, commission, storage, spoilage, other)

class NetbackTests(unittest.TestCase):
    def test_normal_calculation(self):
        result = calculate_netback(option())
        self.assertAlmostEqual(result.expected_sale_value, 20000)
        self.assertAlmostEqual(result.total_costs, 1300)
        self.assertAlmostEqual(result.net_realisation, 18700)
        self.assertAlmostEqual(result.netback_per_quintal, 1870)
    def test_higher_transport_reduces_netback(self):
        self.assertGreater(calculate_netback(option(transport=500)).netback_per_quintal, calculate_netback(option(transport=900)).netback_per_quintal)
    def test_higher_price_increases_netback(self):
        self.assertGreater(calculate_netback(option(price=2100)).netback_per_quintal, calculate_netback(option(price=1800)).netback_per_quintal)
    def test_spoilage_reduces_sale_value(self):
        self.assertLess(calculate_netback(option(spoilage=.1)).expected_sale_value, calculate_netback(option()).expected_sale_value)
    def test_zero_quantity_rejected(self):
        with self.assertRaises(ValueError): option(quantity=0)
    def test_negative_cost_rejected(self):
        with self.assertRaises(ValueError): option(transport=-1)
    def test_spoilage_out_of_range_rejected(self):
        with self.assertRaises(ValueError): option(spoilage=1.1)
    def test_comparison_ranks_by_netback(self):
        ranked = compare_markets([option("Distant", 2100, transport=2500), option("Nearby", 1900, transport=200)])
        self.assertEqual(ranked[0].market_name, "Nearby")
    def test_comparison_requires_same_quantity(self):
        with self.assertRaises(ValueError): compare_markets([option(quantity=5), option("B", quantity=10)])
    def test_explanation_mentions_estimate(self):
        explanation = explain_recommendation(compare_markets([option(), option("B", price=1900)]))
        self.assertIn("not a guaranteed", explanation)

class ForecastTests(unittest.TestCase):
    def test_moving_average(self):
        self.assertAlmostEqual(moving_average_forecast([100, 110, 120], 3), 110)
    def test_forecast_requires_enough_data(self):
        with self.assertRaises(ValueError): moving_average_forecast([100, 110], 3)
    def test_mae(self):
        self.assertAlmostEqual(evaluate_moving_average_mae([10, 20, 30, 40], 2), 15)
    def test_mae_requires_test_observation(self):
        with self.assertRaises(ValueError): evaluate_moving_average_mae([10, 20, 30], 3)

if __name__ == "__main__":
    unittest.main()
