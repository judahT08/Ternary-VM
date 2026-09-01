# =================
#   Assembly Code
# =================

from ternary_utils import toTernary, toDecimal
# ASSEMBLY CODE IDE, not strictly ternary based
# ALU format: Opcode | R2 | R1 | W
# LDI format: Opcode | W  | Immediate
# ADI format: Opcode | R1 | Immediate
# JMP format: Opcode | 0  | Address(8 trits)
# INC format: Opcode | R1 | 000000
# DEC format: Opcode | R1 | 000000
# BRH format: Opcode |

# =====================
''' ---USER MANUAL---

    NOT Case Sensitive
    27 registers R-13 ... R13
    "Rn" = call a register to read / write
    ALU operates on two values
    
Syntax:
    Loading a register:
        "LDI" = (load immediate)
        LDI | Destination Register | Data
        ex. "LDI r0 12"
        R0 := 12
    ALU Operations:
        see ALU_ROM in alu.py for all operations
        ADD, AND, NOR...
        Operation | Operand1 | Operand2 | Write
        ex. ADD r2 r3 r5
        R5 := R2 + R3
    ADI:
        Add a value directly to a register
        ADI | Target | Data
        ex. ADI r2 5
        R2 := R2 + 5
    JMP:
        Jump to a specific line of code
        WILL loop forever
        JMP | Line (first is 0)
    NOP:
        Nothing happens, skip over line
        NOP
    HLT:
        Halts the code
        HLT
    BRH:
        Branching operation
        BRH | Condition | Direct JMP if
        Conditions are based off most recent register
        Condition List:
            zero: Rn = 0
            nzero: Rn not= 0
            crry: Rn carry beyond 6th trit
            ncrry: No Rn carry beyond 6th trit
        ex. BRH zero 6
            

'''
# =====================

OPCODES = {
    # ALU
    "ADD": "0+-",   # 2
    "SUB": "0+0",   # 3
    "NOR": "0++",   # 4
    "AND": "+--",   # 5
    "XOR": "+-0",   # 6
    "CONS": "+0+",  # 10
    "ANY": "++-",   # 11
    "ZERO": "++0",  # 12
    "NZERO": "+++", # 13
    "BRH": "---",   # -13

    # SPECIAL
    "DEC": "0-+", # -2
    "INC": "00-", # -1
    "NOP": "000", # 0
    "HLT": "00+", # 1
    "LDI": "+-+", # 7
    "ADI": "+0-", # 8
    "JMP": "+00", # 9
}

def assemble(lines):
    
    output_lines = []
    for line in lines:
        terms = line.strip().upper().split()
        opCode = OPCODES[terms[0]]

        # NOP
        if opCode == "000":
            output_lines.append("00000000000")
        # LDI FORMAT
        elif opCode == "+-+":
            if len(terms) > 3:
                raise ValueError("Too many args?")
            elif len(terms) < 3:
                raise ValueError("Missing args?")
            write_reg = "d" + terms[1].strip("R").strip(" ")
            immediate = "d" + terms[2].strip(" ")
            output_lines.append(f"{opCode}{toTernary(write_reg).rjust(3, '0')}{toTernary(immediate).rjust(6, '0')}")
        # ADI FORMAT
        elif opCode == "+0-":
            if len(terms) > 3:
                raise ValueError("Too many args?")
            elif len(terms) < 3:
                raise ValueError("Missing args?")
            write_reg = "d" + terms[1].strip("R").strip(" ")
            immediate = "d" + terms[2].strip(" ")
            output_lines.append(f"{opCode}{toTernary(write_reg).rjust(3, '0')}{toTernary(immediate).rjust(6, '0')}")
        # JMP FORMAT
        elif opCode == "+00":
            if len(terms) > 2:
                raise ValueError("Too many args?")
            elif len(terms) < 2:
                raise ValueError("Missing args?")
            address = "d" + terms[1]
            output_lines.append(f"{opCode}000{toTernary(address).rjust(6, '0')}")
        # INC / DEC
        elif opCode == "00-" or opCode == "0-+":
            reg = "d" + terms[1].strip("R").strip(" ")
            output_lines.append(f"{opCode}{toTernary(reg).rjust(3,'0')}000000")
        # BRH
        elif opCode == "---":
            adress = "d" + terms[2]
            if terms[1] == "ZERO":
                output_lines.append(f"{opCode}++0{toTernary(adress).rjust(6, '0')}")
            elif terms[1] == "NZERO":
                output_lines.append(f"{opCode}+++{toTernary(adress).rjust(6, '0')}")
            elif terms[1] == "CRRY":
                output_lines.append(f"{opCode}--0{toTernary(adress).rjust(6, '0')}")
            elif terms[1] == "NCRRY":
                output_lines.append(f"{opCode}--+{toTernary(adress).rjust(6, '0')}")
        # ALU FORMAT
        else:
            if not len(terms) == 4:
                raise ValueError("Missing args?")
            r2 = "d" + terms[1].strip("R").strip(" ")
            r1 = "d" + terms[2].strip("R").strip(" ")
            w = "d" + terms[3].strip("R").strip(" ")
            output_lines.append(f"{opCode}{toTernary(r2).rjust(3,'0')}{toTernary(r1).rjust(3,'0')}{toTernary(w).rjust(3,'0')}")
    
    # HLT
    output_lines.append("00+000000000")
    
    return output_lines

if __name__ == "__main__":
    print("ASSEMBLY\n----IN----")
    lines = []
    line = input().strip().upper()
    while line != "HLT":
        lines.append(line)
        line = input().strip().upper()

    print("----OUT----")
    assembled_lines = assemble(lines)
    for l in assembled_lines:
        print(l)

