from dataclasses import dataclass

@dataclass
class ComparatorData:
    left: str
    right: None
    sign: str

def eq(a: str, b: str) -> ComparatorData:
    """
    Do not work for FloatObject due to floating-point precision!
    """
    return ComparatorData(a, b, "=")

def gt(a: str, b: str) -> ComparatorData:
    return ComparatorData(a, b, ">")

def lt(a: str, b: str) -> ComparatorData:
    return ComparatorData(a, b, "<")

def gteq(a: str, b: str) -> ComparatorData:
    return ComparatorData(a, b, ">=")

def lteq(a: str, b: str) -> ComparatorData:
    return ComparatorData(a, b, "<=")

def noteq(a: str, b: str) -> ComparatorData:
    return ComparatorData(a, b, "!=")
