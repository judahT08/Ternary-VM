# =================
#      memory
# =================

from ternary_utils import toDecimal

# 3 trits provide exactly 27 states (3^3), covering the range -13 to 13.
REGISTERS = ["000000"] * 27  

# Correctly mapped 3-trit strings in numerical order from -13 to 13
r_address = [
    "---", "--0", "--+", "-0-", "-00", "-0+", "-+-", "-+0", "-++",  # -13 to -5
    "0--", "0-0", "0-+", "00-", "000", "00+", "0+-", "0+0", "0++",  # -4 to 4
    "+--", "+-0", "+-+", "+0-", "+00", "+0+", "++-", "++0", "+++"   # 5 to 13
]

def write(r, data):
    """Writes data to the register addressed by ternary string 'r'."""
    if r not in r_address:
        raise ValueError(f"Address '{r}' out of range. Use 3-trit strings from '---' (-13) to '+++' (13).")
    index = r_address.index(r)
    REGISTERS[index] = data

def read(r):
    """Reads data from the register addressed by ternary string 'r'."""
    if r not in r_address:
        raise ValueError(f"Address '{r}' out of range. Use 3-trit strings from '---' (-13) to '+++' (13).")
    index = r_address.index(r)
    return REGISTERS[index]