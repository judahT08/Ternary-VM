# =================
#       ALU
# =================

from ternary_utils import *

# =================
# monadic operators
# =================

def BUF(t): #=
    return t

def NEG(t): #¬
    if t == "-":
        return "+"
    elif t == "+":
        return "-"
    return "0"

def INC(t): #+1
    if t == "-":
        return "0"
    elif t == "0":
        return "+"
    return "-"

def DEC(t): #-1
    if t == "-":
        return "+"
    elif t == "0":
        return "-"
    return "0"

def ISF(t): #=1
    if t == "-": return "+"
    return "-"

def ISX(t): #=0
    if t == "0": return "+"
    return "-"

def IST(t): #=-1
    if t == "+": return "+"
    return "-"

# =================
# diadic operators
# =================

def AND(a, b): # MIN
    if a == "-":
        return "-"
    
    elif a == "0":
        if b == "-":
            return "-"
        elif b == "0":
            return "0"
        else: # b == "+"
            return "0"
        
    else: # a == "+"
        if b == "-":
            return "-"
        elif b == "0":
            return "0"
        else: # b == "+"
            return "+"

def OR(a, b): # MAX
    if a == "-":
        if b == "-":
            return "-"
        elif b == "0":
            return "0"
        else: # b == "+"
            return "+"
        
    elif a == "0":
        if b == "-":
            return "0"
        elif b == "0":
            return "0"
        else: # b == "+"
            return "+"
        
    else: # a == "+"
        return "+"

def NAND(a, b): #¬(a∧b)
    return(NEG(AND(a, b)))

def NOR(a, b): #¬(a∨b)
    return(NEG(OR(a, b)))

def XOR(a, b): #((a∧–b)∨(b∧–a))
    return OR((AND(a, NEG(b))), (AND(NEG(a), b)))

def XNOR(a, b): #¬((a∧–b)∨(b∧–a))
    return NEG(OR((AND(a, NEG(b))), (AND(NEG(a), b))))

def SUM(a, b):#((a=–1)∧(b–1))∨((a=0)∧(b))∨((a=+1)∧(b+1))
    return OR(OR(AND(ISF(a), DEC(b)), AND(ISX(a), b)), AND(IST(a), INC(b)))
    
def CONS(a, b): #compact later
    return OR(
        OR(
            OR(
                OR(
                    OR(
                        OR(
                            OR(
                                OR(
                                    AND(AND(ISF(a), ISF(b)), "-"),
                                    AND(AND(ISF(a), ISX(b)), "0")
                                ),
                                AND(AND(ISF(a), IST(b)), "0")
                            ),
                            AND(AND(ISX(a), ISF(b)), "0")
                        ),
                        AND(AND(ISX(a), ISX(b)), "0")
                    ),
                    AND(AND(ISX(a), IST(b)), "0")
                ),
                AND(AND(IST(a), ISF(b)), "0")
            ),
            AND(AND(IST(a), ISX(b)), "0")
        ),
        AND(AND(IST(a), IST(b)), "+")
    )

def ANY(a, b): #compact later
    return OR(
        OR(
            OR(
                AND(AND(ISF(a), ISF(b)), "-"),
                AND(AND(ISF(a), ISX(b)), "-")
            ),
            OR(
                AND(AND(ISF(a), IST(b)), "0"),
                AND(AND(ISX(a), ISF(b)), "-")
            )
        ),
        OR(
            OR(
                AND(AND(ISX(a), ISX(b)), "0"),
                AND(AND(ISX(a), IST(b)), "1")
            ),
            OR(
                AND(AND(IST(a), ISF(b)), "0"),
                OR(
                    AND(AND(IST(a), ISX(b)), "+"),
                    AND(AND(IST(a), IST(b)), "+")
                )
            )
        )
    )

def COMP(a, b): #a=b
    return OR(OR(AND(ISF(a), ISF(b)), AND(ISX(a), ISX(b))), AND(IST(a), IST(b)))

# =================
#      adders
# =================

def halfAdder(a, b):
    s = SUM(a, b)
    co = CONS(a, b)
    return s, co

def fullAdder(a, b, ci):
    s  = SUM(SUM(a, b), ci)
    co = ANY(CONS(a, b), CONS(ci, SUM(a, b)))
    return s, co

def ADD(A, B): # includes 2 flags
    n = max(len(A), len(B))
    A = A.rjust(n, '0')
    B = B.rjust(n, '0')


    ci = "0"
    out = ""

    for i in range(n - 1, -1, -1):
        s, ci = fullAdder(A[i], B[i], ci)
        out = s + out
        
    # FLAG LOGIC
    cFlag = IST(ci)
    
    return out, cFlag

def SUB(A, B):
    # negate each trit of B
    neg_B = "".join(NEG(t) for t in B)
    return ADD(A, neg_B)

# =========================
# The Arithmetic Logic Unit
# =========================

def ALU(A="", B="", setting="BUF"):
    n = max(len(A), len(B))
    A = A.rjust(n, '0')
    B = B.rjust(n, '0')


    # diadic settings
    if setting == "ADD":
        out, cFlag = ADD(A, B) # carry flag
        ALU.result = out
        ALU.carry = cFlag
    if setting == "SUB": ALU.result = SUB(A, B)
    if setting == "AND": ALU.result = "".join(AND(A[i], B[i]) for i in range(n))
    if setting == "OR": ALU.result = "".join(OR(A[i], B[i]) for i in range(n))
    if setting == "NAND": ALU.result = "".join(NAND(A[i], B[i]) for i in range(n))
    if setting == "NOR": ALU.result = "".join(NOR(A[i], B[i]) for i in range(n))
    if setting == "XOR": ALU.result = "".join(XOR(A[i], B[i]) for i in range(n))
    if setting == "XNOR": ALU.result = "".join(XNOR(A[i], B[i]) for i in range(n))
    if setting == "SUM": ALU.result = "".join(SUM(A[i], B[i]) for i in range(n))
    if setting == "ANY": ALU.result = "".join(ANY(A[i], B[i]) for i in range(n))
    if setting == "CONS": ALU.result = "".join(CONS(A[i], B[i]) for i in range(n))
    
    zFlag = "+" if "".join(ISX(ALU.result[i]) for i in range(len(ALU.result))) == "+" * len(ALU.result) else "-"
    ALU.zero = zFlag

    if setting == "ZERO":
        return ALU.zero
    if setting == "CRRY":
        return ALU.carry
    
    return ALU.result

# =========================
#     ALU CONTROL ROM
# =========================

# ALU settings ONLY
ALU_ROM = {
    "0+-": "ADD",   # 2
    "0+0": "SUB",   # 3
    "0++": "NOR",   # 4
    "+--": "AND",   # 5
    "+-0": "XOR",   # 6
    "+0+": "CONS",  # 10
    "++-": "ANY",   # 11
    "++0": "ZERO",  # 12
    "+++": "NZERO",  # 13
    "---": "BRH",   # -13
}

# all valid ALU settings
VALID_SETTINGS = set(ALU_ROM.values())

def decode_alu_setting(control):

    control = control.upper()

    if control in VALID_SETTINGS:
        return control

    # ROM lookup
    if all(c in "-0+" for c in control):
        if control in ALU_ROM:
            return ALU_ROM[control]
        raise ValueError(f"Unknown ALU opcode: {control}")

    raise ValueError(f"Invalid ALU control input: {control}")
