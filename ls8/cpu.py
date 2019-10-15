"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0b0] * 255    # 256 bytes of Memory
        self.reg = [0b0] * 8      # 8 general-purpose registers

        # Interal registers
        self.pc = 0

        # _opcode_
        self._opcode_ = { 
            0b10000010: 'LDI',
            0b01000111: 'PRN',
            0b00000001: 'HLT',

            # PC mutators
            0b01010000: 'CALL',
            0b00010001: 'RET',
            0b01010100: 'JMP',

            # ALU ops
            0b10100000: 'ADD',
            0b10100001: 'SUB',
            0b10100010: 'MUL',
            0b10100011: 'DIV',
            0b10100100: 'MOD',
            0b01100101: 'INC',
            0b01100110: 'DEC',
        }

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
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        
        running = True

        while running:
            command = self.ram[self.pc]

            # print(command)

            if self._opcode_[command] == 'LDI':
                address = self.ram[self.pc + 1]
                value = self.ram[self.pc + 2]
                self.reg[address] = value
                self.pc += 3
            
            elif self._opcode_[command] == 'PRN':
                address = self.ram[self.pc + 1]
                print(self.reg[address])
                self.pc += 2

            elif self._opcode_[command] == 'HLT':
                running = False

            else:
                print(f"Unknown instruction: {command}")
                sys.exit(1)

        pass

    """
    Ram helper functions

    MAR = _Memory Address Register_ -> Address to store to
    MDR = _Memory Data Register_    -> Data to read or write
    """
    def ram_read(self, MAR):
        """ 
        Accepts the address to read and return the value stored
        there.
        """
        return self.reg[MAR]

    def ram_write(self, MAR, MDR):
        """
        Accepts a value to write, and the address to write it to
        """
        self.reg[MAR] = MDR
        pass
