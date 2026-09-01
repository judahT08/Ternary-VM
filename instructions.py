# =================
#   Machine Code
# =================

from time import sleep
from alu import ALU, decode_alu_setting
from memory import read, write
from ternary_utils import toDecimal

''' OPCODE ROM:
    ALU:
    Opcode | R2 | R1 | W
        0+- = ADD,   # 2
        0+0 = SUB,   # 3
        0++ = NOR,   # 4
        +-- = AND,   # 5
        +-0 = XOR,   # 6
    
    SPECIAL:
    
        NOP = 000, # 0
        HLT = 00+, # 1
    
    LDI:
    Opcode | W | Immediate
        LDI = +-+, # 7
    ADI:
    Opcode | R1 | Immediate
        ADI = +0-, # 8
    JMP:
    Opcode | 0 | Address(8 trits)
        JMP = +00, # 9
    INC / DEC
    Opcode | R1 | 000000
    INC = 00-, DEC = 0-+; -1, -2
'''

# ALU format: Opcode | R2 | R1 | W
# LDI format: Opcode | W  | Immediate
# ADI format: Opcode | R1 | Immediate
# JMP format: Opcode | 0  | Address(8 trits)

def run_machine(instructions):
    
    i = 0
    executed_lines = []  # track executed lines
    while True:
        
        instruction = instructions[i]
        opCode = instruction[0:3]

        # NOP
        if opCode == "000":
            i += 1
            continue
        # HALT
        elif opCode == "00+":
            break
        # LDI
        elif opCode == "+-+":
            r1 = instruction[3:6]
            immediate = instruction[6:12]
            write(r1, immediate)
        # ADI
        elif opCode == "+0-":
            r1 = instruction[3:6]
            immediate = instruction[6:12]
            result = ALU(read(r1), immediate, "ADD")
            write(r1, result)
        # JMP (direct jmp)
        elif opCode == "+00":
            address = instruction[6:12]
            i = toDecimal(address) - 1
        # INC
        elif opCode == "00-":
            r1 = instruction[3:6]
            data = ALU(read(r1), "00+", "ADD")
            write(r1, data)
        # DEC
        elif opCode == "0-+":
            r1 = instruction[3:6]
            data = ALU(read(r1), "00-", "ADD")
            write(r1, data)
        # BRH
        elif opCode == "---":
            condition = instruction[3:6]
            address = instruction[6:12]
            
            if condition == "++0":
                if ALU(setting="ZERO") == "+":
                    i = toDecimal(address) - 1

            elif condition == "+++":
                if ALU(setting="ZERO") == "-":
                    i = toDecimal(address) - 1
            
            elif condition == "--0":
                if ALU(setting="CRRY") == "+":
                    i = toDecimal(address) - 1
            
            elif condition == "--+":
                if ALU(setting="CRRY") != "+":
                    i = toDecimal(address) - 1
        # ALU
        else:
            r1 = read(instruction[3:6])
            r2 = read(instruction[6:9])
            w = instruction[9:12]
            write(w, ALU(r1, r2, decode_alu_setting(opCode)))
        
        executed_lines.append(instruction)
        
        i +=  1
        #sleep(0.05)
        
    return executed_lines
        
if __name__ == "__main__":
    print("MACHINE\n----IN----")
    lines = []
    line = input().strip().upper()

    while line != "00+000000000":
        if line:
            lines.append(line)
        line = input().strip().upper()
    lines.append("00+000000000")

    print("----OUT----")
    output = run_machine(lines)

    for l in output:
        print(l)
        
    print("\nFinal register state:")
    from memory import REGISTERS
    for i, val in enumerate(REGISTERS):
        print(f"R{i}: {val}")
