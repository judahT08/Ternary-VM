# -----------------------------------------------------------------
# HOW TO USE
# User inputs a then b
# either enter "d" for decimal as the first char
# otherwise default to ternary syntax
# ex. d31 OR +--0+
# this ALU uses strictly balanced ternary logic; no boolean is used
# 1 = +, 2 = +-, 3 = +0, 4 = ++, 5 = +--, 6 = +-0...
# -----------------------------------------------------------------

from ternary_utils import toTernary, toDecimal
from alu import ALU, decode_alu_setting

def main():
    print("---BALANCED TERNARY ALU---\n")
    
    # get A
    a_input = input("").strip()
    trit1 = toTernary(a_input)
    
    # get B (optional for monadic operations)
    b_input = input("").strip()
    trit2 = toTernary(b_input) if b_input else ""
    
    # get operation
    control = input("")
    setting = decode_alu_setting(control)

    # pad shorter string if needed
    n = max(len(trit1), len(trit2))
    trit1 = trit1.rjust(n, '0')
    trit2 = trit2.rjust(n, '0')

    # compute
    result = ALU(trit1, trit2, setting)

    # output
    print(f"\nA = {trit1} = {toDecimal(trit1)}")
    if trit2:
        print(f"B = {trit2} = {toDecimal(trit2)}")
    print(f"Setting = {setting}")
    print(f"Result = {result} = {toDecimal(result)}\n")

if __name__ == "__main__":
    main()
