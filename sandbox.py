TAX = 11
DISCOUNT = 15
SHIPPING = 18000


def calculate_subtotal(price, quantity):
    return price * quantity


def calculate_discount(subtotal):
    if subtotal >= 500000:
        return subtotal * DISCOUNT // 100
    return 0


def calculate_tax(subtotal):
    return subtotal * TAX // 100


def calculate_shipping(weight):
    if weight <= 1:
        return SHIPPING
    return SHIPPING + ((weight - 1) * 4000)


def calculate_total(price, quantity, weight):
    subtotal = calculate_subtotal(price, quantity)
    discount = calculate_discount(subtotal)
    taxable = subtotal - discount
    tax = calculate_tax(taxable)
    shipping = calculate_shipping(weight)
    return taxable + tax + shipping


total = calculate_total(
    125000,
    3,
    4,
)
print(total)
