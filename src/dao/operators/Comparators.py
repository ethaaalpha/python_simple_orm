class Comparators:
    @staticmethod
    def eq(a: str, b: str) -> str:
        return f"{a}='{b}'"
    
    @staticmethod
    def gt(a: str, b: str) -> str:
        return f"{a}>'{b}'"
    
    @staticmethod
    def lt(a: str, b: str) -> str:
        return f"{a}<'{b}'"
    
    @staticmethod
    def gteq(a: str, b: str) -> str:
        return f"{a}>='{b}'"
    
    @staticmethod
    def lteq(a: str, b: str) -> str:
        return f"{a}<='{b}'"

    @staticmethod
    def noteq(a: str, b: str) -> str:
        return f"{a}!='{b}'"
