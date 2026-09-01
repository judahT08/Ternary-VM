Sample Programs:

Simple Fibonacci Sequence:
- Uses dual-register operations (read/write)

LDI R0 1

LDI R1 1

ADD R0 r1 r2

ADD R1 r2 r3

ADD R2 r3 r4

HLT

Multiplication via Repeated Addition (R1 * R2):
- Uses branching logic and conditions:
- Output on R3

LDI R1 2

LDI R2 4

LDI R3 0

ADD R3 R2 R3

DEC R1

BRH NZERO 3

HLT

Nested-Loop Factorial Calculator (R1!):
- Output on R2
	
LDI R0 0

LDI R1 4

LDI R2 1

ADD R1 R0 R3

LDI R4 0

ADD R4 R2 R4

DEC R3

BRH NZERO 5

ADD R4 R0 R2

DEC R1

BRH NZERO 3

HLT

Square root (ceil(sqrt(R1))):
- Output on R3

LDI R0 0

LDI R1 36

LDI R2 1

LDI R3 0

ADD R2 R0 R4

DEC R1

BRH ZERO 12

DEC R4

BRH NZERO 5

INC R3

ADI R2 2

JMP 4

INC R3

HLT
