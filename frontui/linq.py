"""
LINQ functions
"""


def first_or_default(iterable, expression):
    return next((x for x in iterable if expression(x)), None)


def count(iterable, expression):
    return sum(1 for x in iterable if expression(x))


def select(iterable, expression):
    return list(map(expression, iterable))


def where(iterable, expression):
    return list(filter(expression, iterable))


def has_any(iterable, expression):
    return first_or_default(iterable, expression) is not None


def order_by_desc(iterable, expression):
    return sorted(iterable, expression, True)


def order_by(iterable, expression):
    return sorted(iterable, expression, False)
