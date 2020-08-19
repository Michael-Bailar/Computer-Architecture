"""CPU functionality."""

# opcodes
LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
POP = 0b11111111 # update
PUSH = 0b11111111  # update

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.RAM = [0] * 256
        self.REG = [0]* 8
        self.PC = 0
        self.HALTED = False
        
    def ram_write(self, MDR, MAR):
        self.RAM[MAR] = MDR

    def ram_read(self, MAR):
        return self.RAM[MAR]

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

            if IR == HLT:
                self.HALTED = True
            elif IR == LDI:
                self.REG[operand_a] = operand_b
            elif IR == PRN:
                print(self.REG[operand_a])
            elif IR == MUL:
                self.alu("MUL", operand_a, operand_b) 
                
            elif IR == PUSH: ## to be fixed
                pass
                # reg_index_a = memory[pc + 1]
                # val = register[reg_index]
                # # decrement stack pointer
                # registers[SP] -= 1
                # # insert val into stack
                # memory[registers[SP]] = val

                # self.PC += 2

            elif IR == POP: ## to be fixed
                pass
                # #setup
                # reg_index_a = memory[pc + 1]
                # val = memory[registers[SP]]

                # # take val from  stack and put in reg
                # registers[reg_index] = val

                # # increment stack pointer
                # registers[SP] += 1

                # self.PC += 2

            else:
                print("Ended due to unknown command: self.IR == ?")
                self.running = False

            self.PC += instruction_length
