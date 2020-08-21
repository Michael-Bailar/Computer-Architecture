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
        self.instruction_length = 0
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
            0b10101010: self.handle_OR,
            0b10101011: self.handle_XOR,
            0b01101001: self.handle_NOT,
            0b10101100: self.handle_SHL,
            0b10101101: self.handle_SHR,
            0b10100100: self.handle_MOD,
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
            0b01010101: self.handle_JEQ,
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
        elif op == "OR":
            self.REG[reg_a] = self.REG[reg_a] | self.REG[reg_b] 
        elif op == "XOR":
            self.REG[reg_a] = self.REG[reg_a] ^ self.REG[reg_b]
        elif op == "NOT":
            self.REG[reg_a] = ~ self.REG[reg_a]
        elif op == "SHL":
            self.REG[reg_a] = self.REG[reg_a] << self.REG[reg_b]
        elif op == "SHR":
            self.REG[reg_a] = self.REG[reg_a] >> self.REG[reg_b]
        elif op == "MOD":
            if self.REG[reg_b] != 0:
                remainder = self.REG[reg_a] % self.REG[reg_b]
                self.REG[reg_a] = remainder
            else:
                print("Command -MOD- failed. Cannot divide by Zero")
                self.BT[0b00000001]()
        elif op == "CMP":
            # print("rega", self.REG[reg_a])
            # print("regb", self.REG[reg_b])
            if self.REG[reg_a] == self.REG[reg_b]:
                #Equal Flag
                self.FL[7] = 1
            else:
                self.FL[7] = 0
            if self.REG[reg_a] > self.REG[reg_b]:
                #Greater Flag
                self.FL[6] = 1
            else:
                self.FL[6] = 0
            if self.REG[reg_a] < self.REG[reg_b]:
                #Less Flag
                self.FL[5] = 1
            else:
                self.FL[5] = 0
            # print(self.FL)
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
        # counter = 0
        while not self.HALTED:
            IR = self.RAM[self.PC]
            self.instruction_length = ((IR >> 6) & 0b11) + 1
            # if IR == 0b00010001 or IR == 0b01010000 or IR == 0b01010110:
            #     instruction_length = 0
            self.BT[IR]() #grab the appropriate function from the branch table
            self.PC += self.instruction_length
            # print(self.PC)
            # counter += 1
            # print("Operation#", counter)
            # print("RAM:", self.RAM[:64])
            # print("END", self.RAM[200:])
            # print (self.REG)

    ## ALL INSTRUCTION COMMANDS ##
    def handle_LDI(self):
        # print("LDI")
        operand_a = self.ram_read(self.PC + 1)
        operand_b = self.ram_read(self.PC + 2)
        self.REG[operand_a] = operand_b
    def handle_PRN(self):
        # print("PRN")
        operand_a = self.ram_read(self.PC + 1)
        print(self.REG[operand_a])
    def handle_HLT(self):
        # print("HLT")
        self.HALTED = True
    def handle_ADD(self):
        # print("ADD")
        operand_a = self.ram_read(self.PC + 1)
        operand_b = self.ram_read(self.PC + 2)
        self.alu("ADD", operand_a, operand_b)
    def handle_SUB(self):
        # print("SUB")
        operand_a = self.ram_read(self.PC + 1)
        operand_b = self.ram_read(self.PC + 2)
        self.alu("SUB", operand_a, operand_b)
    def handle_MUL(self):
        # print("MUL")
        operand_a = self.ram_read(self.PC + 1)
        operand_b = self.ram_read(self.PC + 2)
        self.alu("MUL", operand_a, operand_b)
    def handle_DIV(self):
        # print("DIV")
        operand_a = self.ram_read(self.PC + 1)
        operand_b = self.ram_read(self.PC + 2)
        self.alu("DIV", operand_a, operand_b)
    def handle_INC(self):
        # print("INC")
        operand_a = self.ram_read(self.PC + 1)
        operand_b = self.ram_read(self.PC + 2)
        self.alu("INC", operand_a, operand_b)
    def handle_DEC(self):
        # print("DEC")
        operand_a = self.ram_read(self.PC + 1)
        operand_b = self.ram_read(self.PC + 2)
        self.alu("DEC", operand_a, operand_b)
    def handle_AND(self):
        # print("AND")
        operand_a = self.ram_read(self.PC + 1)
        operand_b = self.ram_read(self.PC + 2)
        self.alu("AND", operand_a, operand_b)
    def handle_OR(self):
        # print("AND")
        operand_a = self.ram_read(self.PC + 1)
        operand_b = self.ram_read(self.PC + 2)
        self.alu("OR", operand_a, operand_b)
    def handle_XOR(self):
        # print("AND")
        operand_a = self.ram_read(self.PC + 1)
        operand_b = self.ram_read(self.PC + 2)
        self.alu("XOR", operand_a, operand_b)
    def handle_NOT(self):
        # print("AND")
        operand_a = self.ram_read(self.PC + 1)
        operand_b = self.ram_read(self.PC + 2)
        self.alu("NOT", operand_a, operand_b)
    def handle_SHL(self):
        # print("AND")
        operand_a = self.ram_read(self.PC + 1)
        operand_b = self.ram_read(self.PC + 2)
        self.alu("SHL", operand_a, operand_b)
    def handle_SHR(self):
        # print("AND")
        operand_a = self.ram_read(self.PC + 1)
        operand_b = self.ram_read(self.PC + 2)
        self.alu("SHR", operand_a, operand_b)
    def handle_MOD(self):
        # print("AND")
        operand_a = self.ram_read(self.PC + 1)
        operand_b = self.ram_read(self.PC + 2)
        self.alu("MOD", operand_a, operand_b)
    def handle_CMP(self):
        # print("CMP")
        operand_a = self.ram_read(self.PC + 1)
        operand_b = self.ram_read(self.PC + 2)
        self.alu("CMP", operand_a, operand_b)
    def handle_PUSH(self):
        # print("PUSH")
        operand_a = self.ram_read(self.PC + 1)
        self.REG[7] -= 1
        self.RAM[self.REG[7]] = self.REG[operand_a]
        self.REG[operand_a] = 0
    def handle_POP(self):
        # print("POP")
        operand_a = self.ram_read(self.PC + 1)
        self.REG[operand_a] = self.RAM[self.REG[7]]
        self.REG[7] += 1
    def handle_CALL(self):
        # print("CALL")
        operand_a = self.ram_read(self.PC + 1)
        #put return location on the stack
        self.REG[7] -= 1
        self.RAM[self.REG[7]] = self.PC + 2
        #move to location stored in reg
        self.PC = self.REG[operand_a]
        self.instruction_length = 0
    def handle_RET(self):
        # print("RET")
        self.PC = self.RAM[self.REG[7]]
        self.REG[7] += 1
        self.instruction_length = 0
    def handle_ST(self):
        # print("ST")
        operand_a = self.ram_read(self.PC + 1)
        operand_b = self.ram_read(self.PC + 2)
        self.REG[operand_b] = self.REG[operand_a]
    def handle_JMP(self):
        # print("ST")
        operand_a = self.ram_read(self.PC + 1)
        self.PC = self.REG[operand_a]
        self.instruction_length = 0
    def handle_JGT(self):
        # print("JGT")
        operand_a = self.ram_read(self.PC + 1)
            # LessThan Flag
        if self.FL[6] == 1:
            self.PC = self.REG[operand_a]
            self.instruction_length = 0    
    def handle_JLT(self):
        # print("JLT")
        operand_a = self.ram_read(self.PC + 1)
        # LessThan Flag
        if self.FL[5] == 1:
            self.PC = self.REG[operand_a]
            self.instruction_length = 0
    def handle_JLE(self):
        # print("JLE")
        operand_a = self.ram_read(self.PC + 1)
        #Equals flag or LessThan
        if self.FL[5] == 1 or self.FL[7] == 1:
            self.PC = self.REG[operand_a]
            self.instruction_length = 0
    def handle_JEQ(self):
        # print("JEQ")
        operand_a = self.ram_read(self.PC + 1)
        #Equals flag
        if self.FL[7] == 1:
            self.PC = self.REG[operand_a]
            self.instruction_length = 0
    def handle_JNE(self):
        # print("JNE")
        operand_a = self.ram_read(self.PC + 1)
        # print('op_a', operand_a)
        # print('FL', self.FL)
        # print("reg", self.REG[operand_a])
        #Equals flag
        if self.FL[7] == 0:
            self.PC = self.REG[operand_a]
            self.instruction_length = 0
        # print("PC", self.PC)
        
    
