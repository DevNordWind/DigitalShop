from decimal import Decimal, DecimalException


def map_decimal(value: str) -> Decimal:
    value = value.strip().replace(" ", "").replace(",", ".")

    try:
        return Decimal(value)
    except DecimalException as e:
        raise ValueError from e
