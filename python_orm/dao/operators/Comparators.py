def __encapsulate(value: str):
    if isinstance(value, int) or isinstance(value, bool) or isinstance(value, float):
        return value
    else:
        return f"'{value}'"

def eq(a: str, b: str) -> str:
    """
    Do not work for FloatObject due to floating-point precision!
    """
    return f"{a}={__encapsulate(b)}"

def gt(a: str, b: str) -> str:
    return f"{a}>{__encapsulate(b)}"

def lt(a: str, b: str) -> str:
    return f"{a}<{__encapsulate(b)}"

def gteq(a: str, b: str) -> str:
    return f"{a}>={__encapsulate(b)}"

def lteq(a: str, b: str) -> str:
    return f"{a}<={__encapsulate(b)}"

def noteq(a: str, b: str) -> str:
    return f"{a}!={__encapsulate(b)}"
