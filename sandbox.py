def add(a, b):
    return a + b


def multiply(a, b):
    return a * b


def calculate(x, y):
    result = add(x, y)
    if result > 10:
        return multiply(result, 2)
    return result


print(calculate(3, 9))
