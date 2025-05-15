from api.schemas.product import ProductInOrderRead


def calculate_total_price(
        products: list[ProductInOrderRead],
        discount_value: float | None = None,
        delivery_fee: float | None = None
) -> float:
    total: float = 0

    if delivery_fee:
        total += delivery_fee
        round(total, 2)

    for product in products:
        total += (product.price * product.quantity)
        total = round(total, 2)

    if discount_value:
        total *= (1 - (discount_value / 100))
        total = round(total, 2)

    return total