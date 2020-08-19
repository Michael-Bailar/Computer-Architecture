# opcodes
LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
POP = 0b01000110 
PUSH = 0b01000101
"""CPU functionality."""



import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        #CAPS indicates a CPU Attribute
        self.RAM = [0] * 256
        self.REG = [0, 0, 0, 0, 0, 0, 0, 0xF3]
        self.PC = 0
        self.HALTED = False

        
    def ram_write(self, mdr, mar):
        self.RAM[mar] = mdr

    def ram_read(self, mar):
        return self.RAM[mar]

    def load(self, filename):
        """Load a program into memory."""
        try:
            address = 0
            with open(filename) as f:
                for line in f:
                    comment_split = line.split("#")
                    n = comment_split[0].strip()

                    if n == '':
                        continue

                    val = int(n, 2)
                    self.RAM[address] = val
                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {filename} not found")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.REG[reg_a] += self.REG[reg_b]
        elif op == "SUB":
            self.REG[reg_a] -= self.REG[reg_b]
        elif op == "MUL":
            self.REG[reg_a] = self.REG[reg_a] * self.REG[reg_b]
        elif op == "DIV":
            self.REG[reg_a] //= self.REG[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            #self.fl,
            #self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.REG[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while not self.HALTED:
            IR = self.RAM[self.PC]
            instruction_length = ((IR >> 6) & 0b11) + 1
            operand_a = self.ram_read(self.PC + 1)
            operand_b = self.ram_read(self.PC + 2)

            # self.branch_table.run(IR, operand_a, operand_b)

            if IR == HLT:
                self.HALTED = True
            elif IR == LDI:
                self.REG[operand_a] = operand_b
            elif IR == PRN:
                print(self.REG[operand_a])
            elif IR == MUL:
                self.alu("MUL", operand_a, operand_b)
            elif IR == PUSH:
                self.REG[7] -= 1
                self.RAM[self.REG[7]] = self.REG[operand_a]
                self.REG[operand_a] = 0
            elif IR == POP:
                self.REG[operand_a] = self.RAM[self.REG[7]]
                self.RAM[self.REG[7]] = 0
                self.REG[7] += 1
            else:
                print("Ended due to unknown command: self.IR == ?")
                self.running = False

            self.PC += instruction_length
