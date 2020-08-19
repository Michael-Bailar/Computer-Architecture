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



        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001

        while self.running:

            self.IR = self.RAM[self.PC]
            self.MAR = self.PC
            self.MAR = self.PC + 1
            self.ram_read() # MDR Becomes the thing at ram[MAR]
            operand_a = self.MDR
            self.MAR = self.PC + 2
            self.ram_read() # MDR Becomes the thing at ram[MAR]
            operand_b = self.MDR
            if self.IR == HLT:
                self.running = False
            elif self.IR == PRN:
                print(self.REG[operand_a])
                self.PC += 2
            elif self.IR == LDI:
                self.REG[operand_a] = operand_b
                self.PC += 3
            else:
                print("I don't know that command")


    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.RAM[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.REG[reg_a] += self.REG[reg_b]
        #elif op == "SUB": etc
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

