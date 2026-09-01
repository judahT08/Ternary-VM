# =================
# convert to (debug)
# =================

def toTernary(num):
    if num[0] == "d":
        # decimal input
        n = int(num[1:])
        if n == 0:
            return "0"
        out = ""
        while n != 0:
            r = n % 3
            n //= 3
            if r == 2:
                r = -1
                n += 1
            elif r == -2:
                r = 1
                n -= 1
            out = { -1:"-", 0:"0", 1:"+" }[r] + out
        return out
    else:
        # ternary input, return full string as is
        for c in num:
            if c not in ("-", "0", "+"):
                raise ValueError(f"Invalid trit: {c}")
        return num

def toDecimal(num):
    symbol_to_value = {'-': -1, '0': 0, '+': 1}
    decimal = 0
    for d in num:
        decimal = decimal * 3 + symbol_to_value[d]
    return decimal