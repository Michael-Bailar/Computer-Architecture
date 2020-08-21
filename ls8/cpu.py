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
        self.SP = self.REG[7]
        # FL 00000LGE L:LessThan, G: GreaterThan, E: Equal
        self.FL = [0] * 8
        #Initialize branch table
        self.BT = {
            0b10000010: self.handle_LDI,
            0b01000111: self.handle_PRN,
            0b00000001: self.handle_HLT,
            0b10100000: self.handle_ADD,
            0b10100001: self.handle_SUB,
            0b10100010: self.handle_MUL,
            0b10100011: self.handle_DIV,
            0b01100101: self.handle_INC,
            0b01100110: self.handle_DEC,
            0b10101000: self.handle_AND,
            0b10100111: self.handle_CMP,
            0b01000101: self.handle_PUSH,
            0b01000110: self.handle_POP,
            0b01010000: self.handle_CALL,
            0b00010001: self.handle_RET,
            0b10000100: self.handle_ST,
            0b01010100: self.handle_JMP,
            0b01010111: self.handle_JGT,
            0b01011000: self.handle_JLT,
            0b01011001: self.handle_JLE,
            0b01011010: self.handle_JEQ,
            0b01010110: self.handle_JNE
        }

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
        elif op == "INC":
            self.REG[reg_a] += 1
        elif op == "DEC":
            self.REG[reg_a] -= 1
        elif op == "AND":
            self.REG[reg_a] = self.REG[reg_a] & self.REG[reg_b]
        elif op == "CMP":
            if self.REG[reg_a] == self.REG[reg_b]:
                #Equal Flag
                self.FL[7] = 1
            elif self.REG[reg_a] > self.REG[reg_b]:
                #Greater Flag
                self.FL[6] = 1
            elif self.REG[reg_a] < self.REG[reg_b]:
                #Less Flag
                self.FL[5] = 1

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
            if IR == 0b00010001 or IR == 0b01010000:
                instruction_length = 0
            self.BT[IR]() #grab the appropriate function from the branch table
            self.PC += instruction_length

    ## ALL INSTRUCTION COMMANDS ##
    def handle_LDI(self):
        operand_a = self.ram_read(self.PC + 1)
        operand_b = self.ram_read(self.PC + 2)
        self.REG[operand_a] = operand_b
    def handle_PRN(self):
        operand_a = self.ram_read(self.PC + 1)
        print(self.REG[operand_a])
    def handle_HLT(self):
        self.HALTED = True
    def handle_ADD(self):
        operand_a = self.ram_read(self.PC + 1)
        operand_b = self.ram_read(self.PC + 2)
        self.alu("ADD", operand_a, operand_b)
    def handle_SUB(self):
        operand_a = self.ram_read(self.PC + 1)
        operand_b = self.ram_read(self.PC + 2)
        self.alu("SUB", operand_a, operand_b)
    def handle_MUL(self):
        operand_a = self.ram_read(self.PC + 1)
        operand_b = self.ram_read(self.PC + 2)
        self.alu("MUL", operand_a, operand_b)
    def handle_DIV(self):
        operand_a = self.ram_read(self.PC + 1)
        operand_b = self.ram_read(self.PC + 2)
        self.alu("DIV", operand_a, operand_b)
    def handle_INC(self):
        operand_a = self.ram_read(self.PC + 1)
        operand_b = self.ram_read(self.PC + 2)
        self.alu("INC", operand_a, operand_b)
    def handle_DEC(self):
        operand_a = self.ram_read(self.PC + 1)
        operand_b = self.ram_read(self.PC + 2)
        self.alu("DEC", operand_a, operand_b)
    def handle_AND(self):
        operand_a = self.ram_read(self.PC + 1)
        operand_b = self.ram_read(self.PC + 2)
        self.alu("AND", operand_a, operand_b)
    def handle_CMP(self):
        operand_a = self.ram_read(self.PC + 1)
        operand_b = self.ram_read(self.PC + 2)
        self.alu("CMP", operand_a, operand_b)
    def handle_PUSH(self):
        operand_a = self.ram_read(self.PC + 1)
        self.REG[7] -= 1
        self.RAM[self.REG[7]] = self.REG[operand_a]
        self.REG[operand_a] = 0
    def handle_POP(self):
        operand_a = self.ram_read(self.PC + 1)
        self.REG[operand_a] = self.RAM[self.REG[7]]
        self.REG[7] += 1
    def handle_CALL(self):
        operand_a = self.ram_read(self.PC + 1)
        #put return location on the stack
        self.REG[7] -= 1
        self.RAM[self.REG[7]] = self.PC + 2
        #move to location stored in reg
        self.PC = self.REG[operand_a]
    def handle_RET(self):
        self.PC = self.RAM[self.REG[7]]
        self.REG[7] += 1
    def handle_ST(self):
        operand_a = self.ram_read(self.PC + 1)
        operand_b = self.ram_read(self.PC + 2)
        self.REG[operand_b] = self.REG[operand_a]
    def handle_JMP(self):
        operand_a = self.ram_read(self.PC + 1)
        self.PC = self.REG[operand_a]


    def handle_JGT(self):
        operand_a = self.ram_read(self.PC + 1)
            # LessThan Flag
            if self.FL[6] == 1:
                self.PC = self.REG[operand_a]    
    def handle_JLT(self):
        operand_a = self.ram_read(self.PC + 1)
        # LessThan Flag
        if self.FL[5] == 1:
            self.PC = self.REG[operand_a]
    def handle_JLE(self):
        operand_a = self.ram_read(self.PC + 1)
        #Equals flag or LessThan
        if self.FL[5] == 1 or self.FL[7] == 1:
            self.PC = self.REG[operand_a]
    def handle_JEQ(self):
        operand_a = self.ram_read(self.PC + 1)
        #Equals flag
        if self.FL[7] == 1:
            self.PC = self.REG[operand_a]
    def handle_JNE(self):
        operand_a = self.ram_read(self.PC + 1)
        #Equals flag
        if self.FL[7] == 0:
            self.PC = self.REG[operand_a]
        
    
