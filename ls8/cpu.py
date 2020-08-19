"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.RAM = [0] * 256
        self.REG = [0, 0, 0, 0, 0, 0, 0, 0]
        self.PC = 0
        self.IR = 0
        self.MAR = 0
        self.MDR = 0
        self.FL = 0
        self.running = False
        

    def ram_read(self):
        self.MDR = self.RAM[self.MAR]

    def ram_write(self):
        self.RAM[self.MAR] = self.MDR

    def run(self):
        """Run the CPU."""
        self.running = True

        # command list (assuming this will change)
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010

        while self.running:

            self.IR = self.RAM[self.PC]
            self.MAR = self.PC

            # update operand a
            self.MAR = self.PC + 1
            self.ram_read() # MDR Becomes the thing at ram[MAR]
            operand_a = self.MDR

            # update operand b
            self.MAR = self.PC + 2
            self.ram_read()
            operand_b = self.MDR

            if self.IR == HLT:
                self.running = False
            elif self.IR == PRN:
                print(self.REG[operand_a])
                self.PC += 2
            elif self.IR == LDI:
                self.REG[operand_a] = operand_b
                self.PC += 3
            elif self.IR == MUL:
                self.alu("MUL", operand_a, operand_b) 
                self.PC += 3
            else:
                print("Ended due to unknown command: self.IR == ?")
                self.running = False


    def load(self, filename):
        """Load a program into memory."""

        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
            
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

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
        else:
            raise Exception("Unsupported ALU operation")

    # def trace(self):
    #     """
    #     Handy function to print out the CPU state. You might want to call this
    #     from run() if you need help debugging.
    #     """

    #     print(f"TRACE: %02X | %02X %02X %02X |" % (
    #         self.PC,
    #         #self.fl,
    #         #self.ie,
    #         self.ram_read(self.PC),
    #         self.ram_read(self.PC + 1),
    #         self.ram_read(self.PC + 2)
    #     ), end='')

        # for i in range(8):
        #     print(" %02X" % self.REG[i], end='')

        # print()

