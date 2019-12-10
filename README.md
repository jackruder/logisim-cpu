# 16-bit CPU in Logisim
Implementation of a CPU in Logisim

### Supported Instructions
Currently, 16 instructions are supported:
- and
- or
- add
- sub
- slt
- nor
- j
- jal
- beq
- addi
- lw
- sw
- jr

#### R-Type Instructions
R-Type instructions have an opcode of 000. They are broken up as such:

- opcode : bits 18-16 (000 for R-type)
- rs	: bits 15-12
- rt	: bits 11-8
- rd	: bits 7-4
- func	: bits 3-0

The supported R-type instructions are listed below with their respective func fields:

- and	: 0000
- or	: 0001
- add	: 0010
- sub	: 0110
- slt	: 0111
- nor	: 1100

#### I-Type Instructions
I-type instructions are broken up as such

- opcode : bits 18-16
- rs	: bits 15-12
- rt	: bits 11-8
- immed  : bits 7-0

The supported I-type instructions are listed below with their respective opcodes:

- beq	: 010
- addi	: 011
- lw	: 100
- sw	: 101

#### J-Type Instructions
J-type instructions are broken up as such

- opcode : bits 18-16
- address: bits 15-0

The supported J-type instructions are listed below with their respective opcodes:

- j	: 001
- jal	: 110
- jr	: 111
