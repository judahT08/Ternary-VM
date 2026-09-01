# main.py
import assembler
import instructions
from memory import REGISTERS

print("===ASSEMBLY===")
asm_lines = []
line = input().strip().upper()
while line != "HLT":
    if line == "":
        line = "NOP"
    asm_lines.append(line)
    line = input().strip().upper()

# assemble
print("\n===MACHINE===")
machine_code = assembler.assemble(asm_lines)
for i in machine_code:
    print(i)

# run machine
instructions.run_machine(machine_code)

# read each register
print("\nREGISTER STATES:")
for i, val in enumerate(REGISTERS):
    logical_address = i - 13
    print(f"R{logical_address:>3} : {val}") 