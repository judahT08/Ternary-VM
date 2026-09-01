This is an experimental balanced ternary machine.
Currently, the ALU is strictly ternary logic.

This machine can perform:
Read, write, dual-register operations, conditional branching, and loop.

How to use the Assembly Language (main.py):

-  Syntax is NOT Case Sensitive
-  Call on 27 registers from R[-13,13]
-  "Rn" = call a register to read / write (n represents integer [-13,13])
-  ALU operates on one or two values depending on specified operation
    
Single Instruction Syntax:

Loading a register:
-    "LDI" = (load immediate)
-    LDI | Destination Register | Data
-    ex. "LDI r0 12"
-    R0 := 12

ALU Operations:
- see opCode.txt for all operations
- ADD, AND, NOR...
- Operation | Operand1 | Operand2 | Write
- ex. ADD r2 r3 r5
- R5 := R2 + R3

ADI:
- Add a value directly to a register
- ADI | Target | Data
- ex. ADI r2 5
- R2 := R2 + 5

JMP:
- Jump to a specific line of code
- WILL loop forever without branching logic (keep reading)
- JMP | Line (first line = 0)

NOP:
- Nothing happens, skip over line
- NOP

HLT:
- Halts the code
- HLT

BRH:
- Branching operation
- BRH | Condition | Direct JMP if
- Conditions are based off most recent register
- Condition List:
  - zero: Rn = 0
  - nzero: Rn not= 0
  - crry: Rn carry beyond 6th trit
  - ncrry: No Rn carry beyond 6th trit
- ex. BRH zero 6

      
