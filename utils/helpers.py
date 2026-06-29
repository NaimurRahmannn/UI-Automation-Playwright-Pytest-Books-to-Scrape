

from decimal import Decimal


def normalize_price(price: str) -> Decimal:
    """Convert a displayed price string into a numeric Decimal.
    """
    cleaned_price = price.replace("£", "").strip()
    return Decimal(cleaned_price)