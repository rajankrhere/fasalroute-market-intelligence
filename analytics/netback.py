"""Net Realisable Price calculations. Money is INR; quantity is in quintals."""
from dataclasses import dataclass
import math

@dataclass(frozen=True)
class MarketOption:
    name: str
    price_per_quintal: float
    quantity_quintals: float
    transport_cost: float
    handling_packaging_cost: float
    commission_cost: float
    storage_cost: float
    spoilage_rate: float
    other_cost: float

    def __post_init__(self):
        if not self.name.strip():
            raise ValueError("Market name cannot be empty.")
        values = {
            "price_per_quintal": self.price_per_quintal,
            "quantity_quintals": self.quantity_quintals,
            "transport_cost": self.transport_cost,
            "handling_packaging_cost": self.handling_packaging_cost,
            "commission_cost": self.commission_cost,
            "storage_cost": self.storage_cost,
            "spoilage_rate": self.spoilage_rate,
            "other_cost": self.other_cost,
        }
        for field, value in values.items():
            if not isinstance(value, (int, float)) or not math.isfinite(value):
                raise ValueError(f"{field} must be a finite number.")
        if self.price_per_quintal < 0:
            raise ValueError("Price cannot be negative.")
        if self.quantity_quintals <= 0:
            raise ValueError("Quantity must be greater than zero.")
        for field in ("transport_cost", "handling_packaging_cost", "commission_cost", "storage_cost", "other_cost"):
            if getattr(self, field) < 0:
                raise ValueError(f"{field} cannot be negative.")
        if not 0 <= self.spoilage_rate <= 1:
            raise ValueError("spoilage_rate must be between 0 and 1.")

@dataclass(frozen=True)
class NetbackResult:
    market_name: str
    expected_sale_value: float
    total_costs: float
    net_realisation: float
    netback_per_quintal: float

def calculate_netback(option: MarketOption) -> NetbackResult:
    """Calculate net realisation. Every cost is explicit; use zero only if not applicable."""
    expected_sale_value = option.price_per_quintal * option.quantity_quintals * (1 - option.spoilage_rate)
    total_costs = (option.transport_cost + option.handling_packaging_cost + option.commission_cost + option.storage_cost + option.other_cost)
    net_realisation = expected_sale_value - total_costs
    return NetbackResult(
        market_name=option.name,
        expected_sale_value=expected_sale_value,
        total_costs=total_costs,
        net_realisation=net_realisation,
        netback_per_quintal=net_realisation / option.quantity_quintals,
    )
