
def add(a, b):
    """Return the sum of a and b."""
    return a + b

def sub(a, b):
    """Return the difference of a and b."""
    return a - b

def mul(a, b):
    """Return the product of a and b."""
    return a * b

def div(a, b):
    """Return the quotient of a and b. Raise ValueError if dividing by zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
