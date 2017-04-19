from Memory import Memory

INSTRUCTION_INDEX = 0
LENGTH_INDEX = 1
CYCLES_INDEX = 2
DEBUG_INDEX = 3

class CPU:

	def __init__(self, memory):

		# Instruction Set
		# [function, length in bytes of opcode + arguments, clock cycles, assembly string]
		# Opcodes: http://pastraiser.com/cpu/gameboy/gameboy_opcodes.html
		# Gameboy CPU Manual: http://marc.rawer.de/Gameboy/Docs/GBCPUman.pdf
		self.instructions = {
			0x00:	[self.NOP, 1, 4, "NOP"],
			0x01:	[self.LD_BC_d16, 3, 12, "LD BC,d16"],
			0x02:	[self.LD_M_BC_A, 1, 8, "LD (BC),A"],
			0x03:	[self.INC_BC, 1, 8, "INC BC"],
			0x04:	[self.INC_B, 1, 4, "INC B"],
			0x05:	[self.DEC_B, 1, 4, "DEC B"],
			0x06:	[self.LD_B, 2, 8, "LD B,d8"],
			0x07:	[self.RLCA, 1, 4, "RLCA"],
			0x08:	[self.LD_M_d16_SP, 3, 20, "LD (a16),SP"],
			0x09:	[self.ADD_HL_BC, 1, 8, "ADD HL,BC"],
			0x0A:	[self.LD_A_M_BC, 1, 8, "LD A,(BC)"],
			0x0B:	[self.DEC_BC, 1, 8, "DEC BC"],
			0x0C:	[self.INC_C, 1, 4, "INC C"],
			0x0D:	[self.DEC_C, 1, 4, "DEC C"],
			0x0E:	[self.LD_C, 2, 8, "LD C,d8"],
			0x0F:	[self.RRCA, 1, 4, "RRCA"],

			0x10:	[self.STOP, 2, 4, "STOP 0"],
			0x11:	[self.LD_DE_d16, 3, 12, "LD DE,d16"],
			0x12:	[self.LD_M_DE_A, 1, 8, "LD (DE),A"],
			0x13:	[self.INC_DE, 1, 8, "INC DE"],
			0x14:	[self.INC_D, 1, 4, "INC D"],
			0x15:	[self.DEC_D, 1, 4, "DEC D"],
			0x16:	[self.LD_D, 2, 8, "LD D,d8"],
			0x17:	[self.RLA, 1, 4, "RLA"],
			0x18:	[self.JR_r8, 2, 12, "JR r8"],
			0x19:	[self.ADD_HL_DE, 1, 8, "ADD HL,DE"],
			0x1A:	[self.LD_A_M_DE, 1, 8, "LD A,(DE)"],
			0x1B:	[self.DEC_DE, 1, 8, "DEC DE"],
			0x1C:	[self.INC_E, 1, 4, "INC E"],
			0x1D:	[self.DEC_E, 1, 4, "DEC E"],
			0x1E:	[self.LD_E, 2, 8, "LD E"],
			0x1F:	[self.RRA, 1, 4, "RRA"],

			0x20:	[self.JR_NZ_r8, 2, 8, "JR NZ,r8"],
			0x21:	[self.LD_HL_d16, 3, 12, "LD HL,d16"],
			0x22:	[self.LD_M_HLP_A, 1, 8, "LD (HL+),A"],
			0x23:	[self.INC_HL, 1, 8, "INC HL"],
			0x24:	[self.INC_H, 1, 4, "INC H"],
			0x25:	[self.DEC_H, 1, 4, "DEC H"],
			0x26:	[self.LD_H, 2, 8, "LD H,d8"],
			0x27:	[self.DAA, 1, 4, "DAA"],
			0x28:	[self.JR_Z_r8, 2, 8, "JR Z,r8"],
			0x29:	[self.ADD_HL_HL, 1, 8, "ADD HL,HL"],
			0x2A:	[self.LD_A_M_HLP, 1, 8, "LD A,(HL+)"],
			0x2B:	[self.DEC_HL, 1, 8, "DEC HL"],
			0x2C:	[self.INC_L, 1, 4, "INC L"],
			0x2D:	[self.DEC_L, 1, 4, "DEC L"],
			0x2E:	[self.LD_L, 2, 8, "LD L,d8"],
			0x2F:	[self.CPL, 1, 4, "CPL"],

			0x30:	[self.JR_NC_r8, 2, 8, "JR NC,r8"],
			0x31:	[self.LD_SP_d16, 3, 12, "LD SP,d16"],
			0x32:	[self.LD_M_HLM_A, 1, 8, "LD (HL-),A"],
			0x33:	[self.INC_SP, 1, 8, "INC SP"],
			0x34:	[self.INC_M_HL, 1, 12, "INC (HL)"],
			0x35:	[self.DEC_M_HL, 1, 12, "DEC (HL)"],
			0x36:	[self.LD_M_HL_d8, 2, 12, "LD (HL),d8"],
			0x37:	[self.SCF, 1, 4, "SCF"],
			0x38:	[self.JR_C_r8, 2, 8, "JR C,r8"],
			0x39:	[self.ADD_HL_SP, 1, 8, "ADD HL,SP"],
			0x3A:	[self.LD_A_M_HLM, 1, 8, "LD A,(HL-)"],
			0x3B:	[self.DEC_SP, 1, 8, "DEC SP"],
			0x3C:	[self.INC_A, 1, 4, "INC A"],
			0x3D:	[self.DEC_A, 1, 4, "DEC A"],
			0x3E:	[self.LD_A, 2, 8, "LD A,d8"],
			0x3F:	[self.CCF, 1, 4, "CCF"],

			0x40:	[self.LD_B_B, 1, 4, "LD B,B"],
			0x41:	[self.LD_B_C, 1, 4, "LD B,C"],
			0x42:	[self.LD_B_D, 1, 4, "LD B,D"],
			0x43:	[self.LD_B_E, 1, 4, "LD B,E"],
			0x44:	[self.LD_B_H, 1, 4, "LD B,H"],
			0x45:	[self.LD_B_L, 1, 4, "LD B,L"],
			0x46:	[self.LD_B_M_HL, 1, 8, "LD B,(HL)"],
			0x47:	[self.LD_B_A, 1, 4, "LD B,A"],
			0x48:	[self.LD_C_B, 1, 4, "LD C,B"],
			0x49:	[self.LD_C_C, 1, 4, "LD C,C"],
			0x4A:	[self.LD_C_D, 1, 4, "LD C,D"],
			0x4B:	[self.LD_C_E, 1, 4, "LD C,E"],
			0x4C:	[self.LD_C_H, 1, 4, "LD C,H"],
			0x4D:	[self.LD_C_L, 1, 4, "LD C,L"],
			0x4E:	[self.LD_C_M_HL, 1, 8, "LD C,(HL)"],
			0x4F:	[self.LD_C_A, 1, 4, "LD C,A"],

			0x50:	[self.LD_D_B, 1, 4, "LD D,B"],
			0x51:	[self.LD_D_C, 1, 4, "LD D,C"],
			0x52:	[self.LD_D_D, 1, 4, "LD D,D"],
			0x53:	[self.LD_D_E, 1, 4, "LD D,E"],
			0x54:	[self.LD_D_H, 1, 4, "LD D,H"],
			0x55:	[self.LD_D_L, 1, 4, "LD D,L"],
			0x56:	[self.LD_D_M_HL, 1, 8, "LD D,(HL)"],
			0x57:	[self.LD_D_A, 1, 4, "LD D,A"],
			0x58:	[self.LD_E_B, 1, 4, "LD E,B"],
			0x59:	[self.LD_E_C, 1, 4, "LD E,C"],
			0x5A:	[self.LD_E_D, 1, 4, "LD E,D"],
			0x5B:	[self.LD_E_E, 1, 4, "LD E,E"],
			0x5C:	[self.LD_E_H, 1, 4, "LD E,H"],
			0x5D:	[self.LD_E_L, 1, 4, "LD E,L"],
			0x5E:	[self.LD_E_M_HL, 1, 8, "LD E,(HL)"],
			0x5F:	[self.LD_E_A, 1, 4, "LD C,A"],

			0x60:	[self.LD_H_B, 1, 4, "LD H,B"],
			0x61:	[self.LD_H_C, 1, 4, "LD H,C"],
			0x62:	[self.LD_H_D, 1, 4, "LD H,D"],
			0x63:	[self.LD_H_E, 1, 4, "LD H,E"],
			0x64:	[self.LD_H_H, 1, 4, "LD H,H"],
			0x65:	[self.LD_H_L, 1, 4, "LD H,L"],
			0x66:	[self.LD_H_M_HL, 1, 8, "LD H,(HL)"],
			0x67:	[self.LD_H_A, 1, 4, "LD H,A"],
			0x68:	[self.LD_L_B, 1, 4, "LD L,B"],
			0x69:	[self.LD_L_C, 1, 4, "LD L,C"],
			0x6A:	[self.LD_L_D, 1, 4, "LD L,D"],
			0x6B:	[self.LD_L_E, 1, 4, "LD L,E"],
			0x6C:	[self.LD_L_H, 1, 4, "LD L,H"],
			0x6D:	[self.LD_L_L, 1, 4, "LD L,L"],
			0x6E:	[self.LD_L_M_HL, 1, 8, "LD L,(HL)"],
			0x6F:	[self.LD_L_A, 1, 4, "LD C,A"],

			0x70:	[self.LD_M_HL_B, 1, 8, "LD (HL),B"],
			0x71:	[self.LD_M_HL_C, 1, 8, "LD (HL),C"],
			0x72:	[self.LD_M_HL_D, 1, 8, "LD (HL),D"],
			0x73:	[self.LD_M_HL_E, 1, 8, "LD (HL),E"],
			0x74:	[self.LD_M_HL_H, 1, 8, "LD (HL),H"],
			0x75:	[self.LD_M_HL_L, 1, 8, "LD (HL),L"],
			0x76:	[self.HALT, 1, 8, "HALT"],
			0x77:	[self.LD_M_HL_A, 1, 8, "LD (HL),A"],
			0x78:	[self.LD_A_B, 1, 4, "LD A,B"],
			0x79:	[self.LD_A_C, 1, 4, "LD A,C"],
			0x7A:	[self.LD_A_D, 1, 4, "LD A,D"],
			0x7B:	[self.LD_A_E, 1, 4, "LD A,E"],
			0x7C:	[self.LD_A_H, 1, 4, "LD A,H"],
			0x7D:	[self.LD_A_L, 1, 4, "LD A,L"],
			0x7E:	[self.LD_A_M_HL, 1, 8, "LD A,(HL)"],
			0x7F:	[self.LD_A_A, 1, 4, "LD A,A"],

			0x80:	[self.ADD_A_B, 1, 4, "ADD A,B"],
			0x81:	[self.ADD_A_C, 1, 4, "ADD A,C"],
			0x82:	[self.ADD_A_D, 1, 4, "ADD A,D"],
			0x83:	[self.ADD_A_E, 1, 4, "ADD A,E"],
			0x84:	[self.ADD_A_H, 1, 4, "ADD A,H"],
			0x85:	[self.ADD_A_L, 1, 4, "ADD A,L"],
			0x86:	[self.ADD_A_M_HL, 1, 8, "ADD A,(HL)"],
			0x87:	[self.ADD_A_A, 1, 4, "ADD A,A"],
			0x88:	[self.ADC_A_B, 1, 4, "ADC A,B"],
			0x89:	[self.ADC_A_C, 1, 4, "ADD A,C"],
			0x8A:	[self.ADC_A_D, 1, 4, "ADD A,D"],
			0x8B:	[self.ADC_A_E, 1, 4, "ADD A,E"],
			0x8C:	[self.ADC_A_H, 1, 4, "ADD A,H"],
			0x8D:	[self.ADC_A_L, 1, 4, "ADD A,L"],
			0x8E:	[self.ADC_A_M_HL, 1, 8, "ADD A,(HL)"],
			0x8F:	[self.ADC_A_A, 1, 4, "ADC A,A"],

			0x90:	[self.SUB_B, 1, 4, "SUB B"],
			0x91:	[self.SUB_C, 1, 4, "SUB C"],
			0x92:	[self.SUB_D, 1, 4, "SUB D"],
			0x93:	[self.SUB_E, 1, 4, "SUB E"],
			0x94:	[self.SUB_H, 1, 4, "SUB H"],
			0x95:	[self.SUB_L, 1, 4, "SUB L"],
			0x96:	[self.SUB_M_HL, 1, 8, "SUB (HL)"],
			0x97:	[self.SUB_A, 1, 4, "SUB A"],
			0x98:	[self.SBC_A_B, 1, 4, "SBC A,B"],
			0x99:	[self.SBC_A_C, 1, 4, "SBC A,C"],
			0x9A:	[self.SBC_A_D, 1, 4, "SBC A,D"],
			0x9B:	[self.SBC_A_E, 1, 4, "SBC A,E"],
			0x9C:	[self.SBC_A_H, 1, 4, "SBC A,H"],
			0x9D:	[self.SBC_A_L, 1, 4, "SBC A,L"],
			0x9E:	[self.SBC_A_M_HL, 1, 8, "SBC A,(HL)"],
			0x9F:	[self.SBC_A_A, 1, 4, "SBC A,A"],

			0xA0:	[self.AND_B, 1, 4, "AND B"],
			0xA1:	[self.AND_C, 1, 4, "AND C"],
			0xA2:	[self.AND_D, 1, 4, "AND D"],
			0xA3:	[self.AND_E, 1, 4, "AND E"],
			0xA4:	[self.AND_H, 1, 4, "AND H"],
			0xA5:	[self.AND_L, 1, 4, "AND L"],
			0xA6:	[self.AND_M_HL, 1, 8, "AND (HL)"],
			0xA7:	[self.AND_A, 1, 4, "AND A"],
			0xA8:	[self.XOR_B, 1, 4, "XOR B"],
			0xA9:	[self.XOR_C, 1, 4, "XOR C"],
			0xAA:	[self.XOR_D, 1, 4, "XOR D"],
			0xAB:	[self.XOR_E, 1, 4, "XOR E"],
			0xAC:	[self.XOR_H, 1, 4, "XOR H"],
			0xAD:	[self.XOR_L, 1, 4, "XOR L"],
			0xAE:	[self.XOR_M_HL, 1, 8, "XOR (HL)"],
			0xAF:	[self.XOR_A, 1, 4, "XOR A"],

			0xB0:	[self.OR_B, 1, 4, "OR B"],
			0xB1:	[self.OR_C, 1, 4, "OR C"],
			0xB2:	[self.OR_D, 1, 4, "OR D"],
			0xB3:	[self.OR_E, 1, 4, "OR E"],
			0xB4:	[self.OR_H, 1, 4, "OR H"],
			0xB5:	[self.OR_L, 1, 4, "OR L"],
			0xB6:	[self.OR_M_HL, 1, 8, "OR (HL)"],
			0xB7:	[self.OR_A, 1, 4, "OR A"],
			0xB8:	[self.CP_B, 1, 4, "CP B"],
			0xB9:	[self.CP_C, 1, 4, "CP C"],
			0xBA:	[self.CP_D, 1, 4, "CP D"],
			0xBB:	[self.CP_E, 1, 4, "CP E"],
			0xBC:	[self.CP_H, 1, 4, "CP H"],
			0xBD:	[self.CP_L, 1, 4, "CP L"],
			0xBE:	[self.CP_M_HL, 1, 8, "CP (HL)"],
			0xBF:	[self.CP_A, 1, 4, "CP A"],

			0xC0:	[self.RET_NZ, 1, 8, "RET NZ"],
			0xC1:	[self.POP_BC, 1, 12, "POP BC"],
			0xC2:	[self.JP_NZ_a16, 3, 12, "JP NZ,a16"],
			0xC3:	[self.JP_a16, 3, 16, "JP a16"],
			0xC4:	[self.CALL_NZ_a16, 3, 12, "CALL NZ,a16"],
			0xC5:	[self.PUSH_BC, 1, 16, "PUSH BC"],
			0xC6:	[self.ADD_A_d8, 2, 8, "ADD A,d8"],
			0xC7:	[self.RST_00H, 1, 16, "RST 00H"],
			0xC8:	[self.RET_Z, 1, 8, "RET Z"],
			0xC9:	[self.RET, 1, 16, "RET"],
			0xCA:	[self.JP_Z_a16, 3, 12, "JP Z,a16"],
			0xCB:	[self.PREFIX_CB, 1, 4, "PREFIX CB"],
			0xCC:	[self.CALL_Z_a16, 3, 12, "CALL Z,a16"],
			0xCD:	[self.CALL_a16, 3, 24, "CALL a16"],
			0xCE:	[self.ADC_A_d8, 2, 8, "ADC A,d8"],
			0xCF:	[self.RST_08H, 1, 16, "RST 08H"],

			0xD0:	[self.RET_NC, 1, 8, "RET NC"],
			0xD1:	[self.POP_DE, 1, 12, "POP DE"],
			0xD2:	[self.JP_NC_a16, 3, 12, "JP NC,a16"],
			0xD3:	[self.KILL, 1, 4, "KILL"],
			0xD4:	[self.CALL_NC_a16, 3, 12, "CALL NC,a16"],
			0xD5:	[self.PUSH_DE, 1, 16, "PUSH DE"],
			0xD6:	[self.SUB_d8, 2, 8, "SUB d8"],
			0xD7:	[self.RST_10H, 1, 16, "RST 10H"],
			0xD8:	[self.RET_C, 1, 8, "RET C"],
			0xD9:	[self.RETI, 1, 16, "RETI"],
			0xDA:	[self.JP_C_a16, 3, 12, "JP C,a16"],
			0xDB:	[self.KILL, 1, 4, "KILL"],
			0xDC:	[self.CALL_C_a16, 3, 12, "CALL C,a16"],
			0xDD:	[self.KILL, 1, 4, "KILL"],
			0xDE:	[self.SBC_A_d8, 2, 8, "SBC A,d8"],
			0xDF:	[self.RST_18H, 1, 16, "RST 18H"],

			0xE0:	[self.LDH_M_a8_A, 2, 12, "LDH (a8),A"],
			0xE1:	[self.POP_HL, 1, 12, "POP HL"],
			0xE2:	[self.LD_M_C_A, 1, 8, "LD (C),A"], #
			0xE3:	[self.KILL, 1, 4, "KILL"],
			0xE4:	[self.KILL, 1, 4, "KILL"],
			0xE5:	[self.PUSH_HL, 1, 16, "PUSH HL"],
			0xE6:	[self.AND_d8, 2, 8, "AND d8"],
			0xE7:	[self.RST_20H, 1, 16, "RST 20H"],
			0xE8:	[self.ADD_SP_r8, 2, 16, "ADD SP,r8"],
			0xE9:	[self.JP_M_HL, 1, 4, "JP (HL)"],
			0xEA:	[self.LD_M_a16_A, 3, 16, "LD (a16),A"],
			0xEB:	[self.KILL, 1, 4, "KILL"],
			0xEC:	[self.KILL, 1, 4, "KILL"],
			0xED:	[self.KILL, 1, 4, "KILL"],
			0xEE:	[self.XOR_d8, 2, 8, "XOR d8"],
			0xEF:	[self.RST_28H, 1, 16, "RST 28H"],

			0xF0:	[self.LDH_A_M_a8, 2, 12, "LDH A,(a8)"],
			0xF1:	[self.POP_AF, 1, 12, "POP AF"],
			0xF2:	[self.LD_A_M_C, 1, 8, "LD A,(C)"], #
			0xF3:	[self.DI, 1, 4, "DI"],
			0xF4:	[self.KILL, 1, 4, "KILL"],
			0xF5:	[self.PUSH_AF, 1, 16, "PUSH AF"],
			0xF6:	[self.OR_d8, 2, 8, "OR d8"],
			0xF7:	[self.RST_30H, 1, 16, "RST 30H"],
			0xF8:	[self.LD_HL_SP_r8, 2, 12, "LD HL,SP+r8"],
			0xF9:	[self.LD_SP_HL, 1, 8, "LD SP,HL"],
			0xFA:	[self.LD_A_M_a16, 3, 16, "LD A,(a16)"],
			0xFB:	[self.EI, 1, 4, "EI"],
			0xFC:	[self.KILL, 1, 4, "KILL"],
			0xFD:	[self.KILL, 1, 4, "KILL"],
			0xFE:	[self.CP_d8, 2, 8, "CP d8"],
			0xFF:	[self.RST_38H, 1, 16, "RST 38H"]
		}

		# 8-bit registers
		self.A = 0x00
		self.B = 0x00
		self.C = 0x00
		self.D = 0x00
		self.E = 0x00
		self.F = 0x00
		self.H = 0x00
		self.L = 0x00

		# 16-bit registers
		self.PC = 0x0000
		self.SP = 0xFFFE

		# Flags
		self.flags = {
			"Z": 0,
			"N": 0,
			"H": 0,
			"C": 0
		}

		# Keep track of cycles
		self.cycles = 0

		# Interupts
		self.INT_ENABLE = True

		# The current operational code
		self.opcode = 0x00

		# Default instruction
		self.instruction_params = [self.NOP, 1, 4]
		self.instruction_function = self.NOP
		self.instruction_length = 1
		self.instruction_cycles = 4
		self.debug_string = "NOP"
		self.args = [0x00, 0x00, 0x00]

		# Initialize the memory (loads ROM into memory map)
		self.memory = memory

		self.DEBUG = True

		self.PREFIX_CB = False

	def print_registers(self):
		A = "A=" + hex(self.A)[2:].zfill(2).upper()
		B = "B=" + hex(self.B)[2:].zfill(2).upper()
		C = "C=" + hex(self.C)[2:].zfill(2).upper()
		D = "D=" + hex(self.D)[2:].zfill(2).upper()
		E = "E=" + hex(self.E)[2:].zfill(2).upper()
		H = "H=" + hex(self.H)[2:].zfill(2).upper()
		L = "L=" + hex(self.L)[2:].zfill(2).upper()
		SP = "SP=" + hex(self.SP)[2:].zfill(4).upper()
		PC = "PC=" + hex(self.PC)[2:].zfill(4).upper()
		Fl = "Z N H C"
		F = str(self.flags["Z"]) + " " + str(self.flags["N"]) + " " + str(self.flags["H"]) + " " + str(self.flags["C"])
		print("    " + A + " " + B + " " +  C + " " + D + " " +  E + " " +  H + " " +  L)
		print("    " + SP)
		print("    " + PC)
		print("    " + Fl)
		print("    " + F)
	# Get 16-bit AF
	def get_AF(self):

		return ((self.A << 8) | (self.F)) & 0xFFFF

	# Get 16-bit BC
	def get_BC(self):

		return ((self.B << 8) | (self.C)) & 0xFFFF

	# Get 16-bit DE
	def get_DE(self):

		return ((self.D << 8) | (self.E)) & 0xFFFF

	# Get 16-bit HL
	def get_HL(self):

		return ((self.H << 8) | (self.L)) & 0xFFFF

	# Increment 8-bit register
	def INC_REGISTER_8(self, register=""):

		if register == "A": reg = self.A
		if register == "B": reg = self.B
		if register == "C": reg = self.C
		if register == "D": reg = self.D
		if register == "E": reg = self.E
		if register == "H": reg = self.H
		if register == "L": reg = self.L

		# H - Set if carry from bit 3
		if reg & 0x0F == 0x0F:
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		reg = (reg + 1) & 0xFF

		# Z - Set if result is zero
		if reg == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

		if register == "A": self.A = reg
		if register == "B": self.B = reg
		if register == "C": self.C = reg
		if register == "D": self.D = reg
		if register == "E": self.E = reg
		if register == "H": self.H = reg
		if register == "L": self.L = reg

	# Decrement 8-bit register
	def DEC_REGISTER_8(self, register=""):

		if register == "A": reg = self.A
		if register == "B": reg = self.B
		if register == "C": reg = self.C
		if register == "D": reg = self.D
		if register == "E": reg = self.E
		if register == "H": reg = self.H
		if register == "L": reg = self.L

		# H - Set if not borrow from bit 4
		if (reg & 0x0F) > 0x01:
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		reg = (reg - 1) & 0xFF

		# Z - Set if result is zero
		if reg == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Set
		self.flags["N"] = 1

		if register == "A": self.A = reg
		if register == "B": self.B = reg
		if register == "C": self.C = reg
		if register == "D": self.D = reg
		if register == "E": self.E = reg
		if register == "H": self.H = reg
		if register == "L": self.L = reg

	# Increment 16-bit registers
	def INC_REGISTER_16(self, register=""):

		if register == "BC": reg = self.get_BC()
		if register == "DE": reg = self.get_DE()
		if register == "HL": reg = self.get_HL()
		if register == "SP": reg = self.SP

		reg = (reg + 1) & 0xFFFF

		if register == "BC":
			self.C = reg & 0x00FF
			self.B = (reg & 0xFF00) >> 8
		if register == "DE":
			self.E = reg & 0x00FF
			self.D = (reg & 0xFF00) >> 8
		if register == "HL":
			self.L = reg & 0x00FF
			self.H = (reg & 0xFF00) >> 8
		if register == "SP":
			self.SP = reg

	# Decrement 16-bit registers
	def DEC_REGISTER_16(self, register = ""):

		if register == "BC": reg = self.get_BC()
		if register == "DE": reg = self.get_DE()
		if register == "HL": reg = self.get_HL()
		if register == "SP": reg = self.SP

		reg = (reg - 1) & 0xFFFF

		if register == "BC":
			self.C = reg & 0x00FF
			self.B = (reg & 0xFF00) >> 8
		if register == "DE":
			self.E = reg & 0x00FF
			self.D = (reg & 0xFF00) >> 8
		if register == "HL":
			self.L = reg & 0x00FF
			self.H = (reg & 0xFF00) >> 8
		if register == "SP":
			self.SP = reg

	# Pop a byte from the stack
	def POP(self):

		self.SP += 1
		val = self.memory.read(self.SP)
		return val

	# Push a byte to the stack
	def PUSH(self, byte):

		self.memory.write(self.SP, byte)
		self.SP -= 1

	# Fetch the next opcode
	def fetch(self):

		self.opcode = self.memory.read(self.PC)

	# Decode and acquire the arguments
	def decode(self):

		# Attempt to get the instruction
		try:
			self.instruction_params = self.instructions[self.opcode]
		except:
			print("***NOT IN INSTRUCTION SET***")
			print("Opcode : 0x" + hex(self.opcode)[2:].zfill(2).upper())

		# Get the parameters of the instruction
		self.instruction_function = self.instruction_params[INSTRUCTION_INDEX]
		self.instruction_length = self.instruction_params[LENGTH_INDEX]
		self.instruction_cycles = self.instruction_params[CYCLES_INDEX]
		self.debug_string = self.instruction_params[DEBUG_INDEX]

		# Get the arguments of the instruction and increment PC
		for i in range(0, self.instruction_length-1):
			self.args[i] = self.memory.read(self.PC + 1 + i)

		# Increment the PC accordingly
		self.PC += self.instruction_length

	# Execute the next instruction
	def execute(self):

		# Execute the desired instruction with the arguments obtained
		self.instruction_function()

		# Increment the cycle counter
		# Will increment more other places for opcodes with variant cycle counts
		self.cycles += self.instruction_cycles

		if self.PREFIX_CB == True:
			self.fetch()
			self.CB_execute()

			if self.DEBUG:
				print("CB OPCODE : " + hex(self.opcode)[2:].zfill(2).upper())

			# The last two bytes read were Prefix CB and the special opcode
			# With this, we are pointing to the next instruction
			self.PC += 1

			# Cycles handled within CB_execute()

			self.PREFIX_CB = False

	# 0xXX - Kill operation
	# - - - -
	def KILL(self):

		print("***KILL***")
		while True: pass

	# 0x00 - No operation
	# - - - -
	def NOP(self):

		pass

	# 0x01 - Load into registers BC immediate 16-bit data
	# - - - -
	def LD_BC_d16(self):

		self.C = self.args[0]
		self.B = self.args[1]

	# 0x02 - Load into memory address (BC) register A
	# - - - -
	def LD_M_BC_A(self):

		self.memory.write(self.get_BC(), self.A)

	# 0x03 - Increment registers BC
	# - - - -
	def INC_BC(self):

		self.INC_REGISTER_16("BC")

	# 0x04 - Increment register B
	# Z 0 H -
	def INC_B(self):

		self.INC_REGISTER_8("B")

	# 0x05 - Decrement register B
	# Z 1 H -
	def DEC_B(self):

		self.DEC_REGISTER_8("B")

	# 0x06 - Load register B immediate 8-bit data
	# - - - -
	def LD_B(self):

		self.B = self.args[0]

	# 0x07 - Rotate A left, old bit 7 to carry flag
	# Z 0 0 C
	def RLCA(self):

		# C - Contains old bit 7 data
		self.flags["C"] = (self.A & 0x80) >> 8

		self.A = (self.A << 1) & 0xFF
		self.A |= self.flags["C"]

		# Z - Set if result is zero
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

		# H - Reset
		self.flags["H"] = 0

	# 0x08 - Load into memory address (16-bit data) register SP
	# - - - -
	def LD_M_d16_SP(self):

		self.memory.write((self.args[1] << 8) | self.args[0], self.SP & 0x00FF)
		self.memory.write(((self.args[1] << 8) | self.args[0]) + 1, (self.SP & 0xFF00) >> 8)
	# 0x09 - Add into registers HL, HL+BC
	# - 0 H C
	def ADD_HL_BC(self):

		# H - Set if carry from bit 11
		if (((self.get_HL() & 0xFFFF) + (self.get_BC() & 0xFFFF)) & 0x1000) == 0x1000:
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# C - Set if carry from bit 15
		if (((self.get_HL() & 0xFFFF) + (self.get_BC() & 0xFFFF)) & 0x8000) == 0x8000:
			self.flags["C"] = 1
		else:
			self.flags["H"] = 0

		HL = self.get_HL()
		HL = (HL + self.get_BC()) & 0xFFFF
		self.L = HL & 0x00FF;
		self.H = (HL & 0xFF00) >> 8

		# N - Reset
		self.flags["N"] = 0

	# 0x0A - Load register A data at memory address (BC)
	# - - - -
	def LD_A_M_BC(self):

		self.A = self.memory.read(self.get_BC())

	# 0x0B - Decrement registers BC
	# - - - -
	def DEC_BC(self):

		self.DEC_REGISTER_16("BC")

	# 0x0C - Increment register C
	# Z 0 H -
	def INC_C(self):

		self.INC_REGISTER_8("C")

	# 0x0D - Decrement register C
	# Z 1 H -
	def DEC_C(self):

		self.DEC_REGISTER_8("C")

	# 0x0E - Load register C immediate 8-bit data
	# - - - -
	def LD_C(self):

		self.C = self.args[0]

	# 0x0F - Rotate A right, old bit 0 to carry flag
	# 0 0 0 C
	def RRCA(self):

		# C - Contains old bit 0 data
		self.flags["C"] = self.A & 0x01

		self.A = (self.A >> 1)
		self.A |= (self.flags["C"] << 8)

		# Z - Set if result is zero
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

		# H - Reset
		self.flags["H"] = 0

	# 0x10 - Halt CPU & LCD display until button pressed
	# - - - -
	def STOP():

		print("***STOP***")
		while True: pass

	# 0x11 - Load into registers DE immediate 16-bit data
	# - - - -
	def LD_DE_d16(self):

		self.E = self.args[0]
		self.D = self.args[1]

	# 0x12 - Load into memory address (DE) register A
	# - - - -
	def LD_M_DE_A(self):

		self.memory.write(self.get_DE(), self.A)

	# 0x13 - Increment registers DE
	# - - - -
	def INC_DE(self):

		self.INC_REGISTER_16("DE")

	# 0x14 - Increment register D
	# Z 0 H -
	def INC_D(self):

		self.INC_REGISTER_8("D")

	# 0x15 - Decrement register B
	# Z 1 H -
	def DEC_D(self):

		self.DEC_REGISTER_8("D")

	# 0x16 - Load register D immediate 8-bit data
	# - - - -
	def LD_D(self):

		self.D = self.args[0]

	# 0x17 - Rotate A left through carry flag
	# 0 0 0 C
	def RLA(self):

		C = self.flags["C"]

		# C - Contains old bit 7 data
		self.flags["C"] = (self.A & 0x80) >> 7

		self.A = (self.A << 1) & 0xFF
		self.A |= C

		# Z - Set if result is zero
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

		# H - Reset
		self.flags["H"] = 0

	# 0x18 - Add signed data to current address and jump to it
	# - - - -
	def JR_r8(self):

		if self.args[0] & 0x80:
			val = -0x100 + self.args[0]
			self.PC += val
		else:
			self.PC += self.args[0]

	# 0x19 - Add into registers HL, HL+DE
	# - 0 H C
	def ADD_HL_DE(self):

		# H - Set if carry from bit 11
		if (((self.get_HL() & 0xFFFF) + (self.get_DE() & 0xFFFF)) & 0x1000) == 0x1000:
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# H - Set if carry from bit 15
		if (((self.get_HL() & 0xFFFF) + (self.get_DE() & 0xFFFF)) & 0x8000) == 0x8000:
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		HL = self.get_HL()
		HL = (HL + self.get_DE()) & 0xFFFF
		self.L = HL & 0x00FF;
		self.H = (HL & 0xFF00) >> 8

		# N - Reset
		self.flags["N"] = 0

	# 0x1A - Load register A data at memory address (DE)
	# - - - -
	def LD_A_M_DE(self):

		self.A = self.memory.read(self.get_DE())

	# 0x1B - Decrement registers DE
	# - - - -
	def DEC_DE(self):

		self.DEC_REGISTER_16("DE")

	# 0x1C - Increment register E
	# Z 0 H -
	def INC_E(self):

		self.INC_REGISTER_8("E")

	# 0x1D - Decrement register E
	# Z 1 H -
	def DEC_E(self):

		self.DEC_REGISTER_8("E")

	# 0x1E - Load register E immediate 8-bit data
	# - - - -
	def LD_E(self):

		self.E = self.args[0]

	# 0x1F - Rotate A right through carry flag
	# 0 0 0 C
	def RRA(self):

		C = self.flags["C"]

		# C - Contains old bit 0 data
		self.flags["C"] = self.A & 0x01

		self.A = (self.A >> 1) & 0xFF
		self.A |= (C << 8)

		# Z - Set if result is zero
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

		# H - Reset
		self.flags["H"] = 0

	# 0x20 - Jump if Z flag is 0
	# - - - -
	def JR_NZ_r8(self):

		if self.flags["Z"] == 0:
			if self.args[0] & 0x80:
				val = -0x100 + self.args[0]
				self.PC += val
			else:
				self.PC += self.args[0]

	# 0x21 - Load into registers HL immediate 16-bit data
	# - - - -
	def LD_HL_d16(self):

		self.L = self.args[0]
		self.H = self.args[1]

	# 0x22 - Load into memory address HL, increment HL
	# - - - -
	def LD_M_HLP_A(self):

		self.memory.write(self.get_HL(), self.A)
		self.INC_REGISTER_16("HL")

	# 0x23 - Increment registers HL
	# - - - -
	def INC_HL(self):

		self.INC_REGISTER_16("HL")

	# 0x24 - Increment register H
	# Z 0 H -
	def INC_H(self):

		self.INC_REGISTER_8("H")

	# 0x25 - Decrement register H
	# Z 1 H -
	def DEC_H(self):

		self.DEC_REGISTER_8("H")

	# 0x26 - Load register H immediate 8-bit data
	#  - - - -
	def LD_H(self):

		self.H = self.args[0]

	# 0x27 - Decimal adjust register A
	# Z - 0 C
	def DAA(self):

		# http://forums.nesdev.com/viewtopic.php?t=9088

		A = self.A

		if self.flags["N"]:
			if self.flags["H"] or ((A & 0x0F) > 9):
				A += 0x06
			if self.flags["C"] or (A > 0x9F):
				A += 0x60
		else:
			if self.flags["H"]:
				A = (A - 6) & 0xFF
			if self.flags["C"]:
				A -= 0x60

		self.flags["H"] = 0
		self.flags["Z"] = 0

		if ((A & 0x100) == 0x100):
			self.flags["C"] = 1

		self.A = A & 0xFF

		if self.A == 0:
			self.flags["Z"] = 1

	# 0x28 - Jump if Z flag is 1
	# - - - -
	def JR_Z_r8(self):

		if self.flags["Z"] == 1:
			if self.args[0] & 0x80:
				val = -0x100 + args[0]
				self.PC += val
			else:
				self.PC += self.args[0]

	# 0x29 - Add into registers HL, HL+HL
	#- 0 H C
	def ADD_HL_HL(self):

		# H - Set if carry from bit 11
		if (((self.get_HL() & 0xFFFF) + (self.get_HL() & 0xFFFF)) & 0x1000) == 0x1000:
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# H - Set if carry from bit 15
		if (((self.get_HL() & 0xFFFF) + (self.get_HL() & 0xFFFF)) & 0x8000) == 0x8000:
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		HL = self.get_HL()
		HL = (HL + HL) & 0xFFFF
		self.L = HL & 0x00FF;
		self.H = (HL & 0xFF00) >> 8

		# N - Reset
		self.flags["N"] = 0

	# 0x2A - Load register A data at memory address (HL), increment HL
	# - - - -
	def LD_A_M_HLP(self):

		self.A = self.memory.read(self.get_HL())
		self.INC_REGISTER_16("HL")

	# 0x2B - Decrement registers HL
	# - - - -
	def DEC_HL(self):

		self.DEC_REGISTER_16("HL")

	# 0x2C - Increment register L
	# Z 0 H -
	def INC_L(self):

		self.INC_REGISTER_8("L")

	# 0x2D - Decrement register L
	# Z 1 H -
	def DEC_L(self):

		self.DEC_REGISTER_8("L")

	# 0x2E - Load register L immediate 8-bit data
	# - - - -
	def LD_L(self):

		self.L = self.args[0]

	# 0x2F - Complement A register (flip all bits)
	# - 1 1 -
	def CPL(self):

		self.A = ~self.A
		self.A &= 0xFF

		# N - Set
		self.flags["N"] = 1

		# H - Set
		self.flags["H"] = 1

	# 0x30 -
	# - - - -
	def JR_NC_r8(self):

		if self.flags["C"] == 0:
			if self.args[0] & 0x80:
				val = -0x100 + args[0]
				self.PC += val
			else:
				self.PC += self.args[0]

	# 0x31 -
	# - - - -
	def LD_SP_d16(self):

		self.SP = (self.args[1] << 8) | self.args[0]

	# 0x32 -
	# - - - -
	def LD_M_HLM_A(self):

		self.memory.write(self.get_HL(), self.A)
		HL = self.get_HL()
		HL = (HL - 1) & 0xFFFF
		self.L = HL & 0x00FF
		self.H = (HL & 0xFF00) >> 8

	# 0x33 -
	# - - - -
	def INC_SP(self):

		self.SP += 1

	# 0x34 -
	# Z 0 H -
	def INC_M_HL(self):

		val = self.memory.read(self.get_HL())

		# H - Set if carry from bit 3
		if (((val & 0xFF) + (0x01 & 0xFF)) & 0x10) == 0x10:
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		val = (val + 1) & 0xFF
		self.memory.write(self.get_HL(), val)

		# Z - Set if result is 0
		if val == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

	# 0x35 -
	# Z 1 H -
	def DEC_M_HL(self):

		val = self.memory.read(self.get_HL())

		# H - Set if no borrow from bit 4
		if (val & 0x0F) > 1:
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0


		val = (val - 1) & 0xFF
		self.memory.write(self.get_HL(), val)

		# Z - Set if result is 0
		if val == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Set
		self.flags["N"] = 1

	# 0x36 -
	# - - - -
	def LD_M_HL_d8(self):

		self.memory.write(self.get_HL(), self.args[0])

	# 0x37 - Set carry flag
	# - 0 0 1
	def SCF(self):

		self.flags["C"] = 1
		self.flags["N"] = 0
		self.flags["H"] = 0

	# 0x38 -
	# - - - -
	def JR_C_r8(self):

		if self.flags["C"] == 1:
			if self.args[0] & 0x80:
				val = -0x100 + args[0]
				self.PC += val
			else:
				self.PC += self.args[0]

	# 0x39 -
	# - 0 H C
	def ADD_HL_SP(self):

		HL = self.get_HL()
		SP = self.get_SP()

		# H - Set if carry from bit 11
		if (((HL & 0xFFFF) + (SP & 0xFFFF)) & 0x1000) == 0x1000:
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# H - Set if carry from bit 15
		if (((HL & 0xFFFF) + (SP & 0xFFFF)) & 0x8000) == 0x8000:
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		HL = (HL + SP) & 0xFFFF

		# N - Reset
		self.flags["N"] = 0

	# 0x3A -
	# - - - -
	def LD_A_M_HLM(self):

		self.A = self.memory.read(self.get_HL())
		HL = self.get_HL()
		HL = (HL - 1) & 0xFFFF
		self.L = HL & 0x00FF
		self.H = (HL & 0xFF00) >> 8

	# 0x3B -
	# - - - -
	def DEC_SP(self):

		self.SP -= 1

	# 0x3C -
	# Z 0 H -
	def INC_A(self):

		self.INC_REGISTER_8("A")

	# 0x3D -
	# Z 1 H -
	def DEC_A(self):

		self.DEC_REGISTER_8("A")

	# 0x3E -
	# - - - -
	def LD_A(self):

		self.A = self.args[0]

	# 0x3F - Carry complement flag
	# - 0 0 C
	def CCF(self):

		if self.flags["C"] == 1:
			self.flags["C"] = 0
		else:
			self.flags["C"] = 1

		# N - Reset
		self.flags["N"] = 0

		# H - Reset
		self.flags["H"] = 0

	# 0x40 -
	# - - - -
	def LD_B_B(self):

		self.B = self.B

	# 0x41 -
	# - - - -
	def LD_B_C(self):

		self.B = self.C

	# 0x42 -
	# - - - -
	def LD_B_D(self):

		self.B = self.D

	# 0x43 -
	# - - - -
	def LD_B_E(self):

		self.B = self.E

	# 0x44 -
	# - - - -
	def LD_B_H(self):

		self.B = self.H

	# 0x45 -
	# - - - -
	def LD_B_L(self):

		self.B = self.L

	# 0x46 -
	# - - - -
	def LD_B_M_HL(self):

		self.B = self.memory.read(self.get_HL())

	# 0x47 -
	# - - - -
	def LD_B_A(self):

		self.B = self.A

	# 0x48 -
	# - - - -
	def LD_C_B(self):

		self.C = self.B

	# 0x49 -
	# - - - -
	def LD_C_C(self):

		self.C = self.C

	# 0x4A -
	# - - - -
	def LD_C_D(self):

		self.C = self.D

	# 0x4B -
	# - - - -
	def LD_C_E(self):

		self.C = self.E

	# 0x4C -
	# - - - -
	def LD_C_H(self):

		self.C = self.H

	# 0x4D -
	# - - - -
	def LD_C_L(self):

		self.C = self.L

	# 0x4E -
	# - - - -
	def LD_C_M_HL(self):

		self.C = self.memory.read(self.get_HL())

	# 0x4F -
	# - - - -
	def LD_C_A(self):

		self.C = self.A

	# 0x50 -
	# - - - -
	def LD_D_B(self):

		self.D = self.B

	# 0x51 -
	# - - - -
	def LD_D_C(self):

		self.D = self.C

	# 0x52 -
	# - - - -
	def LD_D_D(self):

		self.D = self.D

	# 0x53 -
	# - - - -
	def LD_D_E(self):

		self.D = self.E

	# 0x54 -
	# - - - -
	def LD_D_H(self):

		self.D = self.H

	# 0x55 -
	# - - - -
	def LD_D_L(self):

		self.D = self.L

	# 0x56 -
	# - - - -
	def LD_D_M_HL(self):

		self.D = self.memory.read(self.get_HL())

	# 0x57 -
	# - - - -
	def LD_D_A(self):

		self.D = self.A

	# 0x58 -
	# - - - -
	def LD_E_B(self):

		self.E = self.B

	# 0x59 -
	# - - - -
	def LD_E_C(self):

		self.E = self.C

	# 0x5A -
	# - - - -
	def LD_E_D(self):

		self.E = self.D

	# 0x5B -
	# - - - -
	def LD_E_E(self):

		self.E = self.E

	# 0x5C -
	# - - - -
	def LD_E_H(self):

		self.E = self.H

	# 0x5D -
	# - - - -
	def LD_E_L(self):

		self.E = self.L

	# 0x5E -
	# - - - -
	def LD_E_M_HL(self):

		self.E = self.memory.read(self.get_HL())

	# 0x5F -
	# - - - -
	def LD_E_A(self):

		self.E = self.A

	# 0x60 -
	# - - - -
	def LD_H_B(self):

		self.H = self.B

	# 0x61 -
	# - - - -
	def LD_H_C(self):

		self.H = self.C

	# 0x62 -
	# - - - -
	def LD_H_D(self):

		self.H = self.D

	# 0x63 -
	# - - - -
	def LD_H_E(self):

		self.H = self.E

	# 0x64 -
	# - - - -
	def LD_H_H(self):

		self.H = self.H

	# 0x65 -
	# - - - -
	def LD_H_L(self):

		self.H = self.L

	# 0x66 -
	# - - - -
	def LD_H_M_HL(self):

		self.H = self.memory.read(self.get_HL())

	# 0x67 -
	# - - - -
	def LD_H_A(self):

		self.H = self.A

	# 0x68 -
	# - - - -
	def LD_L_B(self):

		self.L = self.B

	# 0x69 -
	# - - - -
	def LD_L_C(self):

		self.L = self.C

	# 0x6A -
	# - - - -
	def LD_L_D(self):

		self.L = self.D

	# 0x6B -
	# - - - -
	def LD_L_E(self):

		self.L = self.E

	# 0x6C -
	# - - - -
	def LD_L_H(self):

		self.L = self.H

	# 0x6D -
	# - - - -
	def LD_L_L(self):

		self.L = self.L

	# 0x6E -
	# - - - -
	def LD_L_M_HL(self):

		self.L = self.memory.read(self.get_HL())

	# 0x6F -
	# 		- - - -
	def LD_L_A(self):

		self.L = self.A

	# 0x70 -
	# - - - -
	def LD_M_HL_B(self):

		self.memory.write(self.get_HL(), self.B)

	# 0x71 -
	# - - - -
	def LD_M_HL_C(self):

		self.memory.write(self.get_HL(), self.C)

	# 0x72 -
	# - - - -
	def LD_M_HL_D(self):

		self.memory.write(self.get_HL(), self.D)

	# 0x73 -
	# - - - -
	def LD_M_HL_E(self):

		self.memory.write(self.get_HL(), self.E)

	# 0x74 -
	# - - - -
	def LD_M_HL_H(self):

		self.memory.write(self.get_HL(), self.H)

	# 0x75 -
	# - - - -
	def LD_M_HL_L(self):

		self.memory.write(self.get_HL(), self.L)

	# 0x76 -
	# - - - -
	def HALT(self):

		print("***HALT***")
		while True: pass

	# 0x77 -
	# - - - -
	def LD_M_HL_A(self):

		self.memory.write(self.get_HL(), self.A)

	# 0x78 -
	# - - - -
	def LD_A_B(self):

		self.A = self.B

	# 0x79 -
	# - - - -
	def LD_A_C(self):

		self.A = self.C

	# 0x7A -
	# - - - -
	def LD_A_D(self):

		self.A = self.D

	# 0x7B -
	# - - - -
	def LD_A_E(self):

		self.A = self.E

	# 0x7C -
	# - - - -
	def LD_A_H(self):

		self.A = self.H

	# 0x7D -
	# - - - -
	def LD_A_L(self):

		self.A = self.L

	# 0x7E -
	# - - - -
	def LD_A_M_HL(self):

		self.A = self.memory.read(self.get_HL())

	# 0x7F -
	# - - - -
	def LD_A_A(self):

		self.A = self.A

	# 0x80 -
	# Z 0 H C
	def ADD_A_B(self):

		A = self.A
		B = self.B

		# H - Set if carry from bit 3
		if (((A & 0xFF) + (B & 0xFF)) & 0x10) == 0x10:
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# C - Set if carry from bit 7
		if (((A & 0xFF) + (B & 0xFF)) & 0x80) == 0x80:
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		A = (A + B) & 0xFF
		self.A = A

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

	# 0x81 -
	# Z 0 H C
	def ADD_A_C(self):

		A = self.A
		C = self.C

		# H - Set if carry from bit 3
		if (((A & 0xFF) + (C & 0xFF)) & 0x10) == 0x10:
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# C - Set if carry from bit 7
		if (((A & 0xFF) + (C & 0xFF)) & 0x80) == 0x80:
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		A = (A + C) & 0xFF
		self.A = A

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

	# 0x82 -
	# Z 0 H C
	def ADD_A_D(self):

		A = self.A
		D = self.D

		# H - Set if carry from bit 3
		if (((A & 0xFF) + (D & 0xFF)) & 0x10) == 0x10:
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# C - Set if carry from bit 7
		if (((A & 0xFF) + (D & 0xFF)) & 0x80) == 0x80:
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		A = (A + D) & 0xFF
		self.A = A

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

	# 0x83 -
	# Z 0 H C
	def ADD_A_E(self):

		A = self.A
		E = self.E

		# H - Set if carry from bit 3
		if (((A & 0xFF) + (E & 0xFF)) & 0x10) == 0x10:
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# C - Set if carry from bit 7
		if (((A & 0xFF) + (E & 0xFF)) & 0x80) == 0x80:
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		A = (A + E) & 0xFF
		self.A = A

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

	# 0x84 -
	# Z 0 H C
	def ADD_A_H(self):

		A = self.A
		H = self.H

		# H - Set if carry from bit 3
		if (((A & 0xFF) + (H & 0xFF)) & 0x10) == 0x10:
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# C - Set if carry from bit 7
		if (((A & 0xFF) + (H & 0xFF)) & 0x80) == 0x80:
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		A = (A + H) & 0xFF
		self.A = A

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

	# 0x85 -
	# Z 0 H C
	def ADD_A_L(self):

		A = self.A
		L = self.L

		# H - Set if carry from bit 3
		if (((A & 0xFF) + (L & 0xFF)) & 0x10) == 0x10:
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# C - Set if carry from bit 7
		if (((A & 0xFF) + (L & 0xFF)) & 0x80) == 0x80:
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		A = (A + L) & 0xFF
		self.A = A

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

	# 0x86 -
	# Z 0 H C
	def ADD_A_M_HL(self):

		A = self.A
		HL = self.memory.read(self.get_HL())

		# H - Set if carry from bit 3
		if (((A & 0xFF) + (HL & 0xFF)) & 0x10) == 0x10:
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# C - Set if carry from bit 7
		if (((A & 0xFF) + (HL & 0xFF)) & 0x80) == 0x80:
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		A = (A + HL) & 0xFF
		self.A = A

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

	# 0x87 -
	# Z 0 H C
	def ADD_A_A(self):

		A = self.A
		A2 = self.A

		# H - Set if carry from bit 3
		if (((A & 0xFF) + (A2 & 0xFF)) & 0x10) == 0x10:
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# C - Set if carry from bit 7
		if (((A & 0xFF) + (A2 & 0xFF)) & 0x80) == 0x80:
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		A = (A + A2) & 0xFF
		self.A = A

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

	# 0x88 -
	# Z 0 H C
	def ADC_A_B(self):

		A = self.A
		B = self.B

		# H - Set if carry from bit 3
		if (((A & 0xFF) + ((B+self.flags["C"]) & 0xFF)) & 0x10) == 0x10:
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# C - Set if carry from bit 7
		if (((A & 0xFF) + ((B+self.flags["C"]) & 0xFF)) & 0x80) == 0x80:
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		A = (A + B + self.flags["C"]) & 0xFF
		self.A = A

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

	# 0x89 -
	# Z 0 H C
	def ADC_A_C(self):

		A = self.A
		C = self.C

		# H - Set if carry from bit 3
		if (((A & 0xFF) + ((C+self.flags["C"]) & 0xFF)) & 0x10) == 0x10:
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# C - Set if carry from bit 7
		if (((A & 0xFF) + ((C+self.flags["C"]) & 0xFF)) & 0x80) == 0x80:
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		A = (A + C + self.flags["C"]) & 0xFF
		self.A = A

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

	# 0x8A -
	# Z 0 H C
	def ADC_A_D(self):

		A = self.A
		D = self.D

		# H - Set if carry from bit 3
		if (((A & 0xFF) + ((D+self.flags["C"]) & 0xFF)) & 0x10) == 0x10:
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# C - Set if carry from bit 7
		if (((A & 0xFF) + ((D+self.flags["C"]) & 0xFF)) & 0x80) == 0x80:
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		A = (A + D + self.flags["C"]) & 0xFF
		self.A = A

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

	# 0x8B -
	# Z 0 H C
	def ADC_A_E(self):

		A = self.A
		E = self.E

		# H - Set if carry from bit 3
		if (((A & 0xFF) + ((E+self.flags["C"]) & 0xFF)) & 0x10) == 0x10:
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# C - Set if carry from bit 7
		if (((A & 0xFF) + ((E+self.flags["C"]) & 0xFF)) & 0x80) == 0x80:
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		A = (A + E + self.flags["C"]) & 0xFF
		self.A = A

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

	# 0x8C -
	# Z 0 H C
	def ADC_A_H(self):

		A = self.A
		H = self.H

		# H - Set if carry from bit 3
		if (((A & 0xFF) + ((H+self.flags["C"]) & 0xFF)) & 0x10) == 0x10:
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# C - Set if carry from bit 7
		if (((A & 0xFF) + ((H+self.flags["C"]) & 0xFF)) & 0x80) == 0x80:
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		A = (A + H + self.flags["C"]) & 0xFF
		self.A = A

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

	# 0x8D -
	# Z 0 H C
	def ADC_A_L(self):

		A = self.A
		L = self.L

		# H - Set if carry from bit 3
		if (((A & 0xFF) + ((L+self.flags["C"]) & 0xFF)) & 0x10) == 0x10:
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# C - Set if carry from bit 7
		if (((A & 0xFF) + ((L+self.flags["C"]) & 0xFF)) & 0x80) == 0x80:
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		A = (A + L + self.flags["C"]) & 0xFF
		self.A = A

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

	# 0x8E -
	# Z 0 H C
	def ADC_A_M_HL(self):

		A = self.A
		HL = self.memory.read(self.get_HL())

		# H - Set if carry from bit 3
		if (((A & 0xFF) + ((HL+self.flags["C"]) & 0xFF)) & 0x10) == 0x10:
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# C - Set if carry from bit 7
		if (((A & 0xFF) + ((HL+self.flags["C"]) & 0xFF)) & 0x80) == 0x80:
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		A = (A + HL + self.flags["C"]) & 0xFF
		self.A = A

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

	# 0x8F -
	# Z 0 H C
	def ADC_A_A(self):

		A = self.A
		A2 = self.A

		# H - Set if carry from bit 3
		if (((A & 0xFF) + ((A2+self.flags["C"]) & 0xFF)) & 0x10) == 0x10:
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# C - Set if carry from bit 7
		if (((A & 0xFF) + ((A2+self.flags["C"]) & 0xFF)) & 0x80) == 0x80:
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		A = (A + A2 + self.flags["C"]) & 0xFF
		self.A = A

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

	# 0x90 -
	# Z 1 H C
	def SUB_B(self):

		result = self.A - self.B

		# C - Set if no borrow
		if self.A > self.B:
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		# H - Set if no borrow from bit 4
		if ((self.A & 0xF) > (self.B & 0xF)):
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# N - Set
		self.flags["N"] = 1

		self.A = result & 0xFF

		# Z - Set if result is zero
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0


	# 0x91 -
	# Z 1 H C
	def SUB_C(self):

		result = self.A - self.C

		# C - Set if no borrow
		if self.A > self.C:
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		# H - Set if no borrow from bit 4
		if ((self.A & 0xF) > (self.C & 0xF)):
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# N - Set
		self.flags["N"] = 1

		self.A = result & 0xFF

		# Z - Set if result is zero
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

	# 0x92 -
	# Z 1 H C
	def SUB_D(self):

		result = self.A - self.D

		# C - Set if no borrow
		if self.A > self.D:
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		# H - Set if no borrow from bit 4
		if ((self.A & 0xF) > (self.D & 0xF)):
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# N - Set
		self.flags["N"] = 1

		self.A = result & 0xFF

		# Z - Set if result is zero
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

	# 0x93 -
	# Z 1 H C
	def SUB_E(self):

		result = self.A - self.E

		# C - Set if no borrow
		if self.A > self.E:
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		# H - Set if no borrow from bit 4
		if ((self.A & 0xF) > (self.E & 0xF)):
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# N - Set
		self.flags["N"] = 1

		self.A = result & 0xFF

		# Z - Set if result is zero
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

	# 0x94 -
	# Z 1 H C
	def SUB_H(self):

		result = self.A - self.H

		# C - Set if no borrow
		if self.A > self.H:
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		# H - Set if no borrow from bit 4
		if ((self.A & 0xF) > (self.H & 0xF)):
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# N - Set
		self.flags["N"] = 1

		self.A = result & 0xFF

		# Z - Set if result is zero
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

	# 0x95 -
	# Z 1 H C
	def SUB_L(self):

		result = self.A - self.L

		# C - Set if no borrow
		if self.A > self.L:
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		# H - Set if no borrow from bit 4
		if ((self.A & 0xF) > (self.L & 0xF)):
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# N - Set
		self.flags["N"] = 1

		self.A = result & 0xFF

		# Z - Set if result is zero
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

	# 0x96 -
	# Z 1 H C
	def SUB_M_HL(self):

		val = self.memory.read(self.get_HL())
		result = self.A - val

		# C - Set if no borrow
		if self.A > val:
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		# H - Set if no borrow from bit 4
		if ((self.A & 0xF) > (val & 0xF)):
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# N - Set
		self.flags["N"] = 1

		self.A = result & 0xFF

		# Z - Set if result is zero
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

	# 0x97 -
	# Z 1 H C
	def SUB_A(self):

		result = self.A - self.A

		# C - Set if no borrow
		if self.A > self.A:
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		# H - Set if no borrow from bit 4
		if ((self.A & 0xF) > (self.A & 0xF)):
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# N - Set
		self.flags["N"] = 1

		self.A = result & 0xFF

		# Z - Set if result is zero
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

	# 0x98 -
	# Z 1 H C
	def SBC_A_B(self):

		result = self.A - self.B - self.flags["C"]

		# C - Set if no borrow
		if self.A > (self.B + self.flags["C"]):
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		# H - Set if no borrow from bit 4
		if ((self.A & 0xF) > ((self.B + self.flags["C"]) & 0xF)):
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# N - Set
		self.flags["N"] = 1

		self.A = result & 0xFF

		# Z - Set if result is zero
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0


	# 0x99 -
	# Z 1 H C
	def SBC_A_C(self):

		result = self.A - self.C - self.flags["C"]

		# C - Set if no borrow
		if self.A > (self.C + self.flags["C"]):
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		# H - Set if no borrow from bit 4
		if ((self.A & 0xF) > ((self.C + self.flags["C"]) & 0xF)):
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# N - Set
		self.flags["N"] = 1

		self.A = result & 0xFF

		# Z - Set if result is zero
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

	# 0x9A -
	# Z 1 H C
	def SBC_A_D(self):

		result = self.A - self.D - self.flags["C"]

		# C - Set if no borrow
		if self.A > (self.D + self.flags["C"]):
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		# H - Set if no borrow from bit 4
		if ((self.A & 0xF) > ((self.D + self.flags["C"]) & 0xF)):
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# N - Set
		self.flags["N"] = 1

		self.A = result & 0xFF

		# Z - Set if result is zero
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

	# 0x9B -
	# Z 1 H C
	def SBC_A_E(self):

		result = self.A - self.E - self.flags["C"]

		# C - Set if no borrow
		if self.A > (self.E + self.flags["C"]):
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		# H - Set if no borrow from bit 4
		if ((self.A & 0xF) > ((self.E + self.flags["C"]) & 0xF)):
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# N - Set
		self.flags["N"] = 1

		self.A = result & 0xFF

		# Z - Set if result is zero
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

	# 0x9C -
	# Z 1 H C
	def SBC_A_H(self):

		result = self.A - self.H - self.flags["C"]

		# C - Set if no borrow
		if self.A > (self.H + self.flags["C"]):
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		# H - Set if no borrow from bit 4
		if ((self.A & 0xF) > ((self.H + self.flags["C"]) & 0xF)):
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# N - Set
		self.flags["N"] = 1

		self.A = result & 0xFF

		# Z - Set if result is zero
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

	# 0x9D -
	# Z 1 H C
	def SBC_A_L(self):

		result = self.A - self.L - self.flags["C"]

		# C - Set if no borrow
		if self.A > (self.L + self.flags["C"]):
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		# H - Set if no borrow from bit 4
		if ((self.A & 0xF) > ((self.L + self.flags["C"]) & 0xF)):
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# N - Set
		self.flags["N"] = 1

		self.A = result & 0xFF

		# Z - Set if result is zero
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

	# 0x9E -
	# Z 1 H C
	def SBC_A_M_HL(self):

		val = self.memory.read(self.get_HL())
		result = self.A - val - self.flags["C"]

		# C - Set if no borrow
		if self.A > (val + self.flags["C"]):
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		# H - Set if no borrow from bit 4
		if ((self.A & 0xF) > ((val + self.flags["C"]) & 0xF)):
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# N - Set
		self.flags["N"] = 1

		self.A = result & 0xFF

		# Z - Set if result is zero
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

	# 0x9F -
	# Z 1 H C
	def SBC_A_A(self):

		result = self.A - self.A - self.flags["C"]

		# C - Set if no borrow
		if self.A > (self.A + self.flags["C"]):
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		# H - Set if no borrow from bit 4
		if ((self.A & 0xF) > ((self.A + self.flags["C"]) & 0xF)):
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# N - Set
		self.flags["N"] = 1

		self.A = result & 0xFF

		# Z - Set if result is zero
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

	# 0xA0 -
	# Z 0 1 0
	def AND_B(self):

		self.A = self.A & self.B

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

		# H - Set
		self.flags["H"] = 1

		# C - Reset
		self.flags["C"] = 0

	# 0xA1 -
	# Z 0 1 0
	def AND_C(self):

		self.A = self.A & self.C

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

		# H - Set
		self.flags["H"] = 1

		# C - Reset
		self.flags["C"] = 0

	# 0xA2 -
	# Z 0 1 0
	def AND_D(self):

		self.A = self.A & self.D

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

		# H - Set
		self.flags["H"] = 1

		# C - Reset
		self.flags["C"] = 0

	# 0xA3 -
	# Z 0 1 0
	def AND_E(self):

		self.A = self.A & self.E

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

		# H - Set
		self.flags["H"] = 1

		# C - Reset
		self.flags["C"] = 0

	# 0xA4 -
	# Z 0 1 0
	def AND_H(self):

		self.A = self.A & self.H

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

		# H - Set
		self.flags["H"] = 1

		# C - Reset
		self.flags["C"] = 0

	# 0xA5 -
	# Z 0 1 0
	def AND_L(self):

		self.A = self.A & self.L

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

		# H - Set
		self.flags["H"] = 1

		# C - Reset
		self.flags["C"] = 0

	# 0xA6 -
	# Z 0 1 0
	def AND_M_HL(self):

		val = self.memory.read(self.get_HL())
		self.A = self.A & val

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

		# H - Set
		self.flags["H"] = 1

		# C - Reset
		self.flags["C"] = 0

	# 0xA7 -
	# Z 0 1 0
	def AND_A(self):

		self.A = self.A & self.A

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

		# H - Set
		self.flags["H"] = 1

		# C - Reset
		self.flags["C"] = 0

	# 0xA8 -
	# Z 0 0 0
	def XOR_B(self):

		self.A = (self.A ^ self.B) & 0xFF

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

		# H - Reset
		self.flags["H"] = 0

		# C - Reset
		self.flags["C"] = 0

	# 0xA9 -
	# Z 0 0 0
	def XOR_C(self):

		self.A = (self.A ^ self.C) & 0xFF

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

		# H - Reset
		self.flags["H"] = 0

		# C - Reset
		self.flags["C"] = 0

	# 0xAA -
	# Z 0 0 0
	def XOR_D(self):

		self.A = (self.A ^ self.D) & 0xFF

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

		# H - Reset
		self.flags["H"] = 0

		# C - Reset
		self.flags["C"] = 0

	# 0xAB -
	# Z 0 0 0
	def XOR_E(self):

		self.A = (self.A ^ self.E) & 0xFF

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

		# H - Reset
		self.flags["H"] = 0

		# C - Reset
		self.flags["C"] = 0

	# 0xAC -
	# Z 0 0 0
	def XOR_H(self):

		self.A = (self.A ^ self.H) & 0xFF

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

		# H - Reset
		self.flags["H"] = 0

		# C - Reset
		self.flags["C"] = 0

	# 0xAD -
	# Z 0 0 0
	def XOR_L(self):

		self.A = (self.A ^ self.L) & 0xFF

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

		# H - Reset
		self.flags["H"] = 0

		# C - Reset
		self.flags["C"] = 0

	# 0xAE -
	# Z 0 0 0
	def XOR_M_HL(self):

		val = self.memory.read(self.get_HL())
		self.A = (self.A ^ val) & 0xFF

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

		# H - Reset
		self.flags["H"] = 0

		# C - Reset
		self.flags["C"] = 0

	# 0xAF -
	# Z 0 0 0
	def XOR_A(self):

		self.A = (self.A ^ self.A) & 0xFF

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

		# H - Reset
		self.flags["H"] = 0

		# C - Reset
		self.flags["C"] = 0

	# 0xB0 -
	# Z 0 0 0
	def OR_B(self):

		self.A = (self.A | self.B) & 0xFF

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

		# H - Reset
		self.flags["H"] = 0

		# C - Reset
		self.flags["C"] = 0

	# 0xB1 -
	# Z 0 0 0
	def OR_C(self):

		self.A = (self.A | self.C) & 0xFF

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

		# H - Reset
		self.flags["H"] = 0

		# C - Reset
		self.flags["C"] = 0

	# 0xB2 -
	# Z 0 0 0
	def OR_D(self):

		self.A = (self.A | self.D) & 0xFF

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

		# H - Reset
		self.flags["H"] = 0

		# C - Reset
		self.flags["C"] = 0

	# 0xB3 -
	# Z 0 0 0
	def OR_E(self):

		self.A = (self.A | self.E) & 0xFF

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

		# H - Reset
		self.flags["H"] = 0

		# C - Reset
		self.flags["C"] = 0

	# 0xB4 -
	# Z 0 0 0
	def OR_H(self):

		self.A = (self.A | self.H) & 0xFF

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

		# H - Reset
		self.flags["H"] = 0

		# C - Reset
		self.flags["C"] = 0

	# 0xB5 -
	# Z 0 0 0
	def OR_L(self):

		self.A = (self.A | self.L) & 0xFF

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

		# H - Reset
		self.flags["H"] = 0

		# C - Reset
		self.flags["C"] = 0

	# 0xB6 -
	# Z 0 0 0
	def OR_M_HL(self):

		val = self.memory.read(self.get_HL())
		self.A = (self.A | val) & 0xFF

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

		# H - Reset
		self.flags["H"] = 0

		# C - Reset
		self.flags["C"] = 0

	# 0xB7 -
	# Z 0 0 0
	def OR_A(self):

		self.A = (self.A | self.A) & 0xFF

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

		# H - Reset
		self.flags["H"] = 0

		# C - Reset
		self.flags["C"] = 0

	# 0xB8 -
	# Z 1 H C
	def CP_B(self):

		result = self.A - self.B

		# C - Set for no borrow (A < n)
		if self.A < self.B:
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		# H - Set if no borrow from bit 4
		if ((self.A & 0xF) > (self.B & 0xF)):
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# N - Set
		self.flags["N"] = 1

		# Z - Set if result is zero (A == n)
		if self.A == self.B:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

	# 0xB9 -
	# Z 1 H C
	def CP_C(self):

		result = self.A - self.C

		# C - Set for no borrow (A < n)
		if self.A < self.C:
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		# H - Set if no borrow from bit 4
		if ((self.A & 0xF) > (self.C & 0xF)):
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# N - Set
		self.flags["N"] = 1

		# Z - Set if result is zero (A == n)
		if self.A == self.C:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

	# 0xBA -
	# Z 1 H C
	def CP_D(self):

		result = self.A - self.D

		# C - Set for no borrow (A < n)
		if self.A < self.D:
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		# H - Set if no borrow from bit 4
		if ((self.A & 0xF) > (self.D & 0xF)):
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# N - Set
		self.flags["N"] = 1

		# Z - Set if result is zero (A == n)
		if self.A == self.D:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

	# 0xBB -
	# Z 1 H C
	def CP_E(self):

		result = self.A - self.E

		# C - Set for no borrow (A < n)
		if self.A < self.E:
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		# H - Set if no borrow from bit 4
		if ((self.A & 0xF) > (self.E & 0xF)):
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# N - Set
		self.flags["N"] = 1

		# Z - Set if result is zero (A == n)
		if self.A == self.E:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

	# 0xBC -
	# Z 1 H C
	def CP_H(self):

		result = self.A - self.H

		# C - Set for no borrow (A < n)
		if self.A < self.H:
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		# H - Set if no borrow from bit 4
		if ((self.A & 0xF) > (self.H & 0xF)):
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# N - Set
		self.flags["N"] = 1

		# Z - Set if result is zero (A == n)
		if self.A == self.H:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

	# 0xBD -
	# Z 1 H C
	def CP_L(self):

		result = self.A - self.L

		# C - Set for no borrow (A < n)
		if self.A < self.L:
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		# H - Set if no borrow from bit 4
		if ((self.A & 0xF) > (self.L & 0xF)):
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# N - Set
		self.flags["N"] = 1

		# Z - Set if result is zero (A == n)
		if self.A == self.L:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

	# 0xBE -
	# Z 1 H C
	def CP_M_HL(self):

		val = self.memory.read(self.get_HL())
		result = self.A - val

		# C - Set for no borrow (A < n)
		if self.A < val:
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		# H - Set if no borrow from bit 4
		if ((self.A & 0xF) > (val & 0xF)):
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# N - Set
		self.flags["N"] = 1

		# Z - Set if result is zero (A == n)
		if self.A == val:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

	# 0xBF -
	# Z 1 H C
	def CP_A(self):

		result = self.A - self.A

		# C - Set for no borrow (A < n)
		if self.A < self.A:
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		# H - Set if no borrow from bit 4
		if ((self.A & 0xF) > (self.A & 0xF)):
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# N - Set
		self.flags["N"] = 1

		# Z - Set if result is zero (A == n)
		if self.A == self.A:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

	# 0xC0 - Return if not zero
	# - - - -
	def RET_NZ(self):

		if self.flags["Z"] == 0:
			address_low = self.POP()
			address_high = self.POP()
			self.PC = (address_high << 8) | address_low

	# 0xC1 -
	# - - - -
	def POP_BC(self):

		self.C = self.POP()
		self.B = self.POP()

	# 0xC2 -
	# - - - -
	def JP_NZ_a16(self):

		if self.flags["Z"] == 0:
			self.PC = (self.args[1] << 8) | self.args[0]

	# 0xC3 -
	# - - - -
	def JP_a16(self):

		self.PC = (self.args[1] << 8) | self.args[0]

	# 0xC4 -
	# - - - -
	def CALL_NZ_a16(self):

		if self.flags["Z"] == 0:
			self.PUSH((self.PC & 0xFF00) >> 8)
			self.PUSH(self.PC & 0x00FF)
			self.PC = (self.args[1] << 8) | self.args[0]

	# 0xC5 -
	# - - - -
	def PUSH_BC(self):

		self.PUSH(self.B)
		self.PUSH(self.C)

	# 0xC6 -
	# Z 0 H C
	def ADD_A_d8(self):

		A = self.A
		d8 = self.args[0]

		# H - Set if carry from bit 3
		if (((A & 0xFF) + (d8 & 0xFF)) & 0x10) == 0x10:
			self.flags["H"] = 1

		# C - Set if carry from bit 7
		if (((A & 0xFF) + (d8 & 0xFF)) & 0x80) == 0x80:
			self.flags["C"] = 1

		A = (A + d8) & 0xFF
		self.A = A

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1

		# N - Reset
		self.flags["N"] = 0

	# 0xC7 -
	# - - - -
	def RST_00H(self):

		self.PUSH((self.PC & 0xFF00) >> 8)
		self.PUSH(self.PC & 0x00FF)
		self.PC = 0x0000 + 0x00

	# 0xC8 -
	# - - - -
	def RET_Z(self):

		if self.flags["Z"] == 1:
			address_low = self.POP()
			address_high = self.POP()
			self.PC = (address_high << 8) | address_low

	# 0xC9 -
	# - - - -
	def RET(self):

		address_low = self.POP()
		address_high = self.POP()
		self.PC = (address_high << 8) | address_low

	# 0xCA -
	# - - - -
	def JP_Z_a16(self):

		if self.flags["Z"] == 1:
			self.PC = (args[1] << 8) | self.args[0]

	# 0xCB -
	# - - - -
	def PREFIX_CB(self):

		self.PREFIX_CB = True

	# 0xCC -
	# - - - -
	def CALL_Z_a16(self):

		if self.flags["Z"] == 1:
			self.PUSH((self.PC & 0xFF00) >> 8)
			self.PUSH(self.PC & 0x00FF)
			self.PC = (self.args[1] << 8) | self.args[0]

	# 0xCD -
	# - - - -
	def CALL_a16(self):

		self.PUSH((self.PC & 0xFF00) >> 8)
		self.PUSH(self.PC & 0x00FF)
		self.PC = (self.args[1] << 8) | self.args[0]

	# 0xCE -
	# Z 0 H C
	def ADC_A_d8(self):

		A = self.A
		d8 = self.args[0]

		# H - Set if carry from bit 3
		if (((A & 0xFF) + ((d8+self.flags["C"]) & 0xFF)) & 0x10) == 0x10:
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# C - Set if carry from bit 7
		if (((A & 0xFF) + ((d8+self.flags["C"]) & 0xFF)) & 0x80) == 0x80:
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		A = (A + d8 + self.flags["C"]) & 0xFF
		self.A = A

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

	# 0xCF -
	# - - - -
	def RST_08H(self):

		self.PUSH((self.PC & 0xFF00) >> 8)
		self.PUSH(self.PC & 0x00FF)
		self.PC = 0x0000 + 0x08

	# 0xD0 -
	# - - - -
	def RET_NC(self):

		if self.flags["C"] == 0:
			address_low = self.POP()
			address_high = self.POP()
			self.PC = (address_high << 8) | address_low

	# 0xD1 -
	# - - - -
	def POP_DE(self):

		self.E = self.POP()
		self.D = self.POP()

	# 0xD2 -
	# - - - -
	def JP_NC_a16(self):

		if self.flags["C"] == 0:
			self.PC = (args[1] << 8) | self.args[0]

	# 0xD3 -
	# - - - -
	# NO OPCODE

	# 0xD4 -
	# - - - -
	def CALL_NC_a16(self):

		if self.flags["C"] == 0:
			self.PUSH((self.PC & 0xFF00) >> 8)
			self.PUSH(self.PC & 0x00FF)
			self.PC = (self.args[1] << 8) | self.args[0]

	# 0xD5 -
	# - - - -
	def PUSH_DE(self):

		self.PUSH(self.D)
		self.PUSH(self.E)

	# 0xD6 -
	# Z 1 H C
	def SUB_d8(self):

		d8 = self.args[0]
		result = self.A - d8

		# C - Set if no borrow
		if self.A > d8:
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		# H - Set if no borrow from bit 4
		if ((self.A & 0xF) > (d8 & 0xF)):
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# N - Set
		self.flags["N"] = 1

		self.A = result & 0xFF

		# Z - Set if result is zero
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

	# 0xD7 -
	# - - - -
	def RST_10H(self):

		self.PUSH((self.PC & 0xFF00) >> 8)
		self.PUSH(self.PC & 0x00FF)
		self.PC = 0x0000 + 0x10

	# 0xD8 -
	# - - - -
	def RET_C(self):

		if self.flags["C"] == 1:
			address_low = self.POP()
			address_high = self.POP()
			self.PC = (address_high << 8) | address_low

	# 0xD9 -
	# - - - -
	def RETI(self):

		address_low = self.POP()
		address_high = self.POP()
		self.PC = (address_high << 8) | address_low
		self.INT_ENABLE = True

	# 0xDA -
	# - - - -
	def JP_C_a16(self):

		if self.flags["C"] == 1:
			self.PC = (self.args[1] << 8) | self.args[0]

	# 0xDB -
	# - - - -
	# NO OPCODE

	# 0xDC -
	# - - - -
	def CALL_C_a16(self):

		if self.flags["C"] == 1:
			self.PUSH((self.PC & 0xFF00) >> 8)
			self.PUSH(self.PC & 0x00FF)
			self.PC = (self.args[1] << 8) | self.args[0]

	# 0xDD -
	# - - - -
	# NO OPCODE

	# 0xDE -
	# Z 1 H C
	def SBC_A_d8(self):

		d8 = self.args[0]
		result = self.A - d8 - self.flags["C"]

		# C - Set if no borrow
		if self.A > (d8 + self.flags["C"]):
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		# H - Set if no borrow from bit 4
		if ((self.A & 0xF) > ((d8 + self.flags["C"]) & 0xF)):
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# N - Set
		self.flags["N"] = 1

		self.A = result & 0xFF

		# Z - Set if result is zero
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

	# 0xDF -
	# - - - -
	def RST_18H(self):

		self.PUSH((self.PC & 0xFF00) >> 8)
		self.PUSH(self.PC & 0x00FF)
		self.PC = 0x0000 + 0x18

	# 0xE0 -
	# - - - -
	def LDH_M_a8_A(self):

		self.memory.write(0xFF00 + self.args[0], self.A)

	# 0xE1 -
	# - - - -
	def POP_HL(self):

		self.L = self.POP()
		self.H = self.POP()

	# 0xE2 -
	# - - - -
	def LD_M_C_A(self):

		self.memory.write(0xFF00 + self.C, self.A)

	# 0xE3 -
	# - - - -
	# NO OPCODE

	# 0xE4 -
	# - - - -
	# NO OPCODE

	# 0xE5 -
	# - - - -
	def PUSH_HL(self):

		self.PUSH(self.H)
		self.PUSH(self.L)

	# 0xE6 -
	# Z 0 1 0
	def AND_d8(self):

		d8 = self.args[0]
		self.A = self.A & d8

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

		# H - Set
		self.flags["H"] = 1

		# C - Reset
		self.flags["C"] = 0

	# 0xE7 -
	# - - - -
	def RST_20H(self):

		self.PUSH((self.PC & 0xFF00) >> 8)
		self.PUSH(self.PC & 0x00FF)
		self.PC = 0x0000 + 0x20

	# 0xE8 -
	# 0 0 H C
	def ADD_SP_r8(self):

		# H - Set if carry from bit 11
		if (((self.SP & 0xFFFF) + (self.args[0] & 0xFFFF)) & 0x1000) == 0x1000:
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# H - Set if carry from bit 15
		if (((self.SP & 0xFFFF) + (self.args[0] & 0xFFFF)) & 0x8000) == 0x8000:
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		self.SP = (self.SP + self.args[0]) & 0xFFFF

		# Z - Reset
		self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

	# 0xE9 -
	# - - - -
	def JP_M_HL(self):

		self.PC = (self.H << 8) | self.L

	# 0xEA -
	# - - - -
	def LD_M_a16_A(self):

		self.memory.write((self.args[1] << 8) | self.args[0], self.A)

	# 0xEB -
	# - - - -
	# NO OPCODE

	# 0xEC -
	# - - - -
	# NO OPCODE

	# 0xED -
	# - - - -
	# NO OPCODE

	# 0xEE -
	# Z 0 0 0
	def XOR_d8(self):

		d8 = self.args[0]
		self.A = self.A ^ d8

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

		# H - Reset
		self.flags["H"] = 0

		# C - Reset
		self.flags["C"] = 0

	# 0xEF -
	# - - - -
	def RST_28H(self):

		self.PUSH((self.PC & 0xFF00) >> 8)
		self.PUSH(self.PC & 0x00FF)
		self.PC = 0x0000 + 0x28

	# 0xF0 -
	# - - - -
	def LDH_A_M_a8(self):

		self.A = self.memory.read(0xFF00 + self.args[0])

	# 0xF1 -
	# - - - -
	def POP_AF(self):

		self.F = self.POP()
		self.A = self.POP()

	# 0xF2 -
	# - - - -
	def LD_A_M_C(self):

		self.A = self.memory.read(0xFF00 + self.C)

	# 0xF3 -
	# - - - -
	def DI(self):

		self.INT_ENABLE = False

	# 0xF4 -
	# - - - -
	# NO OPCODE

	# 0xF5 -
	# - - - -
	def PUSH_AF(self):

		self.PUSH(self.A)
		self.PUSH(self.F)

	# 0xF6 -
	# Z 0 0 0
	def OR_d8(self):

		d8 = self.args[0]
		self.A = self.A | d8

		# Z - Set if result is 0
		if self.A == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

		# H - Reset
		self.flags["H"] = 0

		# C - Reset
		self.flags["C"] = 0

	# 0xF7 -
	#  - - - -
	def RST_30H(self):

		self.PUSH((self.PC & 0xFF00) >> 8)
		self.PUSH(self.PC & 0x00FF)
		self.PC = 0x0000 + 0x30

	# 0xF8 -
	# 0 0 H C
	def LD_HL_SP_r8(self):

		if self.args[0] & 0x80:
			r8 = -0x100 + self.args[0]
		else:
			r8 = self.args[0]

		result = self.SP + r8

		# H - Set if carry from bit 11
		if (((self.SP & 0xFFFF) + (r8 & 0xFFFF)) & 0x1000) == 0x1000:
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# C - Set if carry from bit 15
		if (((self.SP & 0xFFFF) + (r8 & 0xFFFF)) & 0x8000) == 0x8000:
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		# Z - Reset
		self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

		self.L = result & 0x00FF
		self.H = (result & 0xFF00) >> 8

	# 0xF9 -
	# - - - -
	def LD_SP_HL(self):

		self.SP = (self.H << 8) | self.L

	# 0xFA -
	# - - - -
	def LD_A_M_a16(self):

		self.A = self.memory.read((self.args[1] << 8) | self.args[0])

	# 0xFB -
	# - - - -
	def EI(self):

		self.INT_ENABLE = True

	# 0xFC -
	# - - - -
	# NO OPCODE

	# 0xFD -
	# - - - -
	# NO OPCODE

	# 0xFE -
	# Z 1 H C
	def CP_d8(self):

		d8 = self.args[0]
		result = self.A - d8

		# C - Set for no borrow (A < n)
		if self.A < d8:
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		# H - Set if no borrow from bit 4
		if ((self.A & 0xF) > (d8 & 0xF)):
			self.flags["H"] = 1
		else:
			self.flags["H"] = 0

		# N - Set
		self.flags["N"] = 1

		# Z - Set if result is zero (A == n)
		if self.A == d8:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

	# 0xFF -
	# 	- - - -
	def RST_38H(self):

		self.PUSH((self.PC & 0xFF00) >> 8)
		self.PUSH(self.PC & 0x00FF)
		self.PC = 0x0000 + 0x38

###### CB PREFIX CODES ######

	def CB_execute(self):

		op = self.opcode

		if op == 0x00:
			self.RLC("B")
		elif op == 0x01:
			self.RLC("C")
		elif op == 0x02:
			self.RLC("D")
		elif op == 0x03:
			self.RLC("E")
		elif op == 0x04:
			self.RLC("H")
		elif op == 0x05:
			self.RLC("L")
		elif op == 0x06:
			self.RLC("M_HL")
		elif op == 0x07:
			self.RLC("A")
		elif op == 0x08:
			self.RRC("B")
		elif op == 0x09:
			self.RRC("C")
		elif op == 0x0A:
			self.RRC("D")
		elif op == 0x0B:
			self.RRC("E")
		elif op == 0x0C:
			self.RRC("H")
		elif op == 0x0D:
			self.RRC("L")
		elif op == 0x0E:
			self.RRC("M_HL")
		elif op == 0x0F:
			self.RRC("A")
		elif op == 0x10:
			self.RL("B")
		elif op == 0x11:
			self.RL("C")
		elif op == 0x12:
			self.RL("D")
		elif op == 0x13:
			self.RL("E")
		elif op == 0x14:
			self.RL("H")
		elif op == 0x15:
			self.RL("L")
		elif op == 0x16:
			self.RL("M_HL")
		elif op == 0x17:
			self.RL("A")
		elif op == 0x18:
			self.RR("B")
		elif op == 0x19:
			self.RR("C")
		elif op == 0x1A:
			self.RR("D")
		elif op == 0x1B:
			self.RR("E")
		elif op == 0x1C:
			self.RR("H")
		elif op == 0x1D:
			self.RR("L")
		elif op == 0x1E:
			self.RR("M_HL")
		elif op == 0x1F:
			self.RR("A")
		elif op == 0x20:
			self.SLA("B")
		elif op == 0x21:
			self.SLA("C")
		elif op == 0x22:
			self.SLA("D")
		elif op == 0x23:
			self.SLA("E")
		elif op == 0x24:
			self.SLA("H")
		elif op == 0x25:
			self.SLA("L")
		elif op == 0x26:
			self.SLA("M_HL")
		elif op == 0x27:
			self.SLA("A")
		elif op == 0x28:
			self.SRA("B")
		elif op == 0x29:
			self.SRA("C")
		elif op == 0x2A:
			self.SRA("D")
		elif op == 0x2B:
			self.SRA("E")
		elif op == 0x2C:
			self.SRA("H")
		elif op == 0x2D:
			self.SRA("L")
		elif op == 0x2E:
			self.SRA("M_HL")
		elif op == 0x2F:
			self.SRA("A")
		elif op == 0x30:
			self.SWAP("B")
		elif op == 0x31:
			self.SWAP("C")
		elif op == 0x32:
			self.SWAP("D")
		elif op == 0x33:
			self.SWAP("E")
		elif op == 0x34:
			self.SWAP("H")
		elif op == 0x35:
			self.SWAP("L")
		elif op == 0x36:
			self.SWAP("M_HL")
		elif op == 0x37:
			self.SWAP("A")
		elif op == 0x38:
			self.SRL("B")
		elif op == 0x39:
			self.SRL("C")
		elif op == 0x3A:
			self.SRL("D")
		elif op == 0x3B:
			self.SRL("E")
		elif op == 0x3C:
			self.SRL("H")
		elif op == 0x3D:
			self.SRL("L")
		elif op == 0x3E:
			self.SRL("M_HL")
		elif op == 0x3F:
			self.SRL("A")
		elif op == 0x40:
			self.BIT(0, "B")
		elif op == 0x41:
			self.BIT(0, "C")
		elif op == 0x42:
			self.BIT(0, "D")
		elif op == 0x43:
			self.BIT(0, "E")
		elif op == 0x44:
			self.BIT(0, "H")
		elif op == 0x45:
			self.BIT(0, "L")
		elif op == 0x46:
			self.BIT(0, "M_HL")
		elif op == 0x47:
			self.BIT(0, "A")
		elif op == 0x48:
			self.BIT(1, "B")
		elif op == 0x49:
			self.BIT(1, "C")
		elif op == 0x4A:
			self.BIT(1, "D")
		elif op == 0x4B:
			self.BIT(1, "E")
		elif op == 0x4C:
			self.BIT(1, "H")
		elif op == 0x4D:
			self.BIT(1, "L")
		elif op == 0x4E:
			self.BIT(1, "M_HL")
		elif op == 0x4F:
			self.BIT(1, "A")
		elif op == 0x50:
			self.BIT(2, "B")
		elif op == 0x51:
			self.BIT(2, "C")
		elif op == 0x52:
			self.BIT(2, "D")
		elif op == 0x53:
			self.BIT(2, "E")
		elif op == 0x54:
			self.BIT(2, "H")
		elif op == 0x55:
			self.BIT(2, "L")
		elif op == 0x56:
			self.BIT(2, "M_HL")
		elif op == 0x57:
			self.BIT(2, "A")
		elif op == 0x58:
			self.BIT(3, "B")
		elif op == 0x59:
			self.BIT(3, "C")
		elif op == 0x5A:
			self.BIT(3, "D")
		elif op == 0x5B:
			self.BIT(3, "E")
		elif op == 0x5C:
			self.BIT(3, "H")
		elif op == 0x5D:
			self.BIT(3, "L")
		elif op == 0x5E:
			self.BIT(3, "M_HL")
		elif op == 0x5F:
			self.BIT(3, "A")
		elif op == 0x60:
			self.BIT(4, "B")
		elif op == 0x61:
			self.BIT(4, "C")
		elif op == 0x62:
			self.BIT(4, "D")
		elif op == 0x63:
			self.BIT(4, "E")
		elif op == 0x64:
			self.BIT(4, "H")
		elif op == 0x65:
			self.BIT(4, "L")
		elif op == 0x66:
			self.BIT(4, "M_HL")
		elif op == 0x67:
			self.BIT(4, "A")
		elif op == 0x68:
			self.BIT(5, "B")
		elif op == 0x69:
			self.BIT(5, "C")
		elif op == 0x6A:
			self.BIT(5, "D")
		elif op == 0x6B:
			self.BIT(5, "E")
		elif op == 0x6C:
			self.BIT(5, "H")
		elif op == 0x6D:
			self.BIT(5, "L")
		elif op == 0x6E:
			self.BIT(5, "M_HL")
		elif op == 0x6F:
			self.BIT(5, "A")
		elif op == 0x70:
			self.BIT(6, "B")
		elif op == 0x71:
			self.BIT(6, "C")
		elif op == 0x72:
			self.BIT(6, "D")
		elif op == 0x73:
			self.BIT(6, "E")
		elif op == 0x74:
			self.BIT6("H")
		elif op == 0x75:
			self.BIT(6, "L")
		elif op == 0x76:
			self.BIT(6, "M_HL")
		elif op == 0x77:
			self.BIT(6, "A")
		elif op == 0x78:
			self.BIT(7, "B")
		elif op == 0x79:
			self.BIT(7, "C")
		elif op == 0x7A:
			self.BIT(7, "D")
		elif op == 0x7B:
			self.BIT(7, "E")
		elif op == 0x7C:
			self.BIT(7, "H")
		elif op == 0x7D:
			self.BIT(7, "L")
		elif op == 0x7E:
			self.BIT(7, "M_HL")
		elif op == 0x7F:
			self.BIT(7, "A")
		elif op == 0x80:
			self.RES(0, "B")
		elif op == 0x81:
			self.RES(0, "C")
		elif op == 0x82:
			self.RES(0, "D")
		elif op == 0x83:
			self.RES(0, "E")
		elif op == 0x84:
			self.RES(0, "H")
		elif op == 0x85:
			self.RES(0, "L")
		elif op == 0x86:
			self.RES(0, "M_HL")
		elif op == 0x87:
			self.RES(0, "A")
		elif op == 0x88:
			self.RES(1, "B")
		elif op == 0x89:
			self.RES(1, "C")
		elif op == 0x8A:
			self.RES(1, "D")
		elif op == 0x8B:
			self.RES(1, "E")
		elif op == 0x8C:
			self.RES(1, "H")
		elif op == 0x8D:
			self.RES(1, "L")
		elif op == 0x8E:
			self.RES(1, "M_HL")
		elif op == 0x8F:
			self.RES(1, "A")
		elif op == 0x90:
			self.RES(2, "B")
		elif op == 0x91:
			self.RES(2, "C")
		elif op == 0x92:
			self.RES(2, "D")
		elif op == 0x93:
			self.RES(2, "E")
		elif op == 0x94:
			self.RES(2, "H")
		elif op == 0x95:
			self.RES(2, "L")
		elif op == 0x96:
			self.RES(2, "M_HL")
		elif op == 0x97:
			self.RES(2, "A")
		elif op == 0x98:
			self.RES(3, "B")
		elif op == 0x99:
			self.RES(3, "C")
		elif op == 0x9A:
			self.RES(3, "D")
		elif op == 0x9B:
			self.RES(3, "E")
		elif op == 0x9C:
			self.RES(3, "H")
		elif op == 0x9D:
			self.RES(3, "L")
		elif op == 0x9E:
			self.RES(3, "M_HL")
		elif op == 0x9F:
			self.RES(3, "A")
		elif op == 0xA0:
			self.RES(4, "B")
		elif op == 0xA1:
			self.RES(4, "C")
		elif op == 0xA2:
			self.RES(4, "D")
		elif op == 0xA3:
			self.RES(4, "E")
		elif op == 0xA4:
			self.RES(4, "H")
		elif op == 0xA5:
			self.RES(4, "L")
		elif op == 0xA6:
			self.RES(4, "M_HL")
		elif op == 0xA7:
			self.RES(4, "A")
		elif op == 0xA8:
			self.RES(5, "B")
		elif op == 0xA9:
			self.RES(5, "C")
		elif op == 0xAA:
			self.RES(5, "D")
		elif op == 0xAB:
			self.RES(5, "E")
		elif op == 0xAC:
			self.RES(5, "H")
		elif op == 0xAD:
			self.RES(5, "L")
		elif op == 0xAE:
			self.RES(5, "M_HL")
		elif op == 0xAF:
			self.RES(5, "A")
		elif op == 0xB0:
			self.RES(6, "B")
		elif op == 0xB1:
			self.RES(6, "C")
		elif op == 0xB2:
			self.RES(6, "D")
		elif op == 0xB3:
			self.RES(6, "E")
		elif op == 0xB4:
			self.RES(6, "H")
		elif op == 0xB5:
			self.RES(6, "L")
		elif op == 0xB6:
			self.RES(6, "M_HL")
		elif op == 0xB7:
			self.RES(6, "A")
		elif op == 0xB8:
			self.RES(7, "B")
		elif op == 0xB9:
			self.RES(7, "C")
		elif op == 0xBA:
			self.RES(7, "D")
		elif op == 0xBB:
			self.RES(7, "E")
		elif op == 0xBC:
			self.RES(7, "H")
		elif op == 0xBD:
			self.RES(7, "L")
		elif op == 0xBE:
			self.RES(7, "M_HL")
		elif op == 0xBF:
			self.RES(7, "A")
		elif op == 0xC0:
			self.SET(0, "B")
		elif op == 0xC1:
			self.SET(0, "C")
		elif op == 0xC2:
			self.SET(0, "D")
		elif op == 0xC3:
			self.SET(0, "E")
		elif op == 0xC4:
			self.SET(0, "H")
		elif op == 0xC5:
			self.SET(0, "L")
		elif op == 0xC6:
			self.SET(0, "M_HL")
		elif op == 0xC7:
			self.SET(0, "A")
		elif op == 0xC8:
			self.SET(1, "B")
		elif op == 0xC9:
			self.SET(1, "C")
		elif op == 0xCA:
			self.SET(1, "D")
		elif op == 0xCB:
			self.SET(1, "E")
		elif op == 0xCC:
			self.SET(1, "H")
		elif op == 0xCD:
			self.SET(1, "L")
		elif op == 0xCE:
			self.SET(1, "M_HL")
		elif op == 0xCF:
			self.SET(1, "A")
		elif op == 0xD0:
			self.SET(2, "B")
		elif op == 0xD1:
			self.SET(2, "C")
		elif op == 0xD2:
			self.SET(2, "D")
		elif op == 0xD3:
			self.SET(2, "E")
		elif op == 0xD4:
			self.SET(2, "H")
		elif op == 0xD5:
			self.SET(2, "L")
		elif op == 0xD6:
			self.SET(2, "M_HL")
		elif op == 0xD7:
			self.SET(2, "A")
		elif op == 0xD8:
			self.SET(3, "B")
		elif op == 0xD9:
			self.SET(3, "C")
		elif op == 0xDA:
			self.SET(3, "D")
		elif op == 0xDB:
			self.SET(3, "E")
		elif op == 0xDC:
			self.SET(3, "H")
		elif op == 0xDD:
			self.SET(3, "L")
		elif op == 0xDE:
			self.SET(3, "M_HL")
		elif op == 0xDF:
			self.SET(3, "A")
		elif op == 0xE0:
			self.SET(4, "B")
		elif op == 0xE1:
			self.SET(4, "C")
		elif op == 0xE2:
			self.SET(4, "D")
		elif op == 0xE3:
			self.SET(4, "E")
		elif op == 0xE4:
			self.SET(4, "H")
		elif op == 0xE5:
			self.SET(4, "L")
		elif op == 0xE6:
			self.SET(4, "M_HL")
		elif op == 0xE7:
			self.SET(4, "A")
		elif op == 0xE8:
			self.SET(5, "B")
		elif op == 0xE9:
			self.SET(5, "C")
		elif op == 0xEA:
			self.SET(5, "D")
		elif op == 0xEB:
			self.SET(5, "E")
		elif op == 0xEC:
			self.SET(5, "H")
		elif op == 0xED:
			self.SET(5, "L")
		elif op == 0xEE:
			self.SET(5, "M_HL")
		elif op == 0xEF:
			self.SET(5, "A")
		elif op == 0xF0:
			self.SET(6, "B")
		elif op == 0xF1:
			self.SET(6, "C")
		elif op == 0xF2:
			self.SET(6, "D")
		elif op == 0xF3:
			self.SET(6, "E")
		elif op == 0xF4:
			self.SET(6, "H")
		elif op == 0xF5:
			self.SET(6, "L")
		elif op == 0xF6:
			self.SET(6, "M_HL")
		elif op == 0xF7:
			self.SET(6, "A")
		elif op == 0xF8:
			self.SET(7, "B")
		elif op == 0xF9:
			self.SET(7, "C")
		elif op == 0xFA:
			self.SET(7, "D")
		elif op == 0xFB:
			self.SET(7, "E")
		elif op == 0xFC:
			self.SET(7, "H")
		elif op == 0xFD:
			self.SET(7, "L")
		elif op == 0xFE:
			self.SET(7, "M_HL")
		elif op == 0xFF:
			self.SET(7, "A")

	def RLC(self,reg=""):

		if reg == "A": val = self.A
		if reg == "B": val = self.B
		if reg == "C": val = self.C
		if reg == "D": val = self.D
		if reg == "E": val = self.E
		if reg == "H": val = self.H
		if reg == "L": val = self.L
		if reg == "M_HL": val = self.memory.read(self.get_HL())

		# C - Contains old bit 7 data
		self.flags["C"] = (val & 0x80) >> 7

		val = (val << 1) & 0xFF

		# Z - Set if result is zero
		if val == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

		# H - Reset
		self.flags["H"] = 0

		if reg == "A": self.A = val
		if reg == "B": self.B = val
		if reg == "C": self.C = val
		if reg == "D": self.D = val
		if reg == "E": self.E = val
		if reg == "H": self.H = val
		if reg == "L": self.L = val
		if reg == "M_HL": self.memory.write(self.get_HL(), val)

		if reg != "M_HL":
			self.cycles += 8
		else:
			self.cycles += 16

	def RRC(self,reg=""):

		if reg == "A": val = self.A
		if reg == "B": val = self.B
		if reg == "C": val = self.C
		if reg == "D": val = self.D
		if reg == "E": val = self.E
		if reg == "H": val = self.H
		if reg == "L": val = self.L
		if reg == "M_HL": val = self.memory.read(self.get_HL())

		# C - Contains old bit 0 data
		self.flags["C"] = val & 0x01

		val = (val >> 1) & 0xFF

		# Z - Set if result is zero
		if val == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

		# H - Reset
		self.flags["H"] = 0

		if reg == "A": self.A = val
		if reg == "B": self.B = val
		if reg == "C": self.C = val
		if reg == "D": self.D = val
		if reg == "E": self.E = val
		if reg == "H": self.H = val
		if reg == "L": self.L = val
		if reg == "M_HL": self.memory.write(self.get_HL(), val)

		if reg != "M_HL":
			self.cycles += 8
		else:
			self.cycles += 16

	def RL(self, reg=""):

		if reg == "A": val = self.A
		if reg == "B": val = self.B
		if reg == "C": val = self.C
		if reg == "D": val = self.D
		if reg == "E": val = self.E
		if reg == "H": val = self.H
		if reg == "L": val = self.L
		if reg == "M_HL": val = self.memory.read(self.get_HL())

		C = self.flags["C"]

		# C - Contains old bit 7 data
		self.flags["C"] = (val & 0x80) >> 7

		val = (val << 1) & 0xFF
		val |= C

		# Z - Set if result is zero
		if val == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

		# H - Reset
		self.flags["H"] = 0

		if reg == "A": self.A = val
		if reg == "B": self.B = val
		if reg == "C": self.C = val
		if reg == "D": self.D = val
		if reg == "E": self.E = val
		if reg == "H": self.H = val
		if reg == "L": self.L = val
		if reg == "M_HL": self.memory.write(self.get_HL(), val)

		if reg != "M_HL":
			self.cycles += 8
		else:
			self.cycles += 16

	def RR(self, reg=""):

		if reg == "A": val = self.A
		if reg == "B": val = self.B
		if reg == "C": val = self.C
		if reg == "D": val = self.D
		if reg == "E": val = self.E
		if reg == "H": val = self.H
		if reg == "L": val = self.L
		if reg == "M_HL": val = self.memory.read(self.get_HL())

		C = self.flags["C"]

		# C - Contains old bit 0 data
		self.flags["C"] = val & 0x01

		val = (val << 1) & 0xFF
		val |= C

		# Z - Set if result is zero
		if val == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

		# H - Reset
		self.flags["H"] = 0

		if reg == "A": self.A = val
		if reg == "B": self.B = val
		if reg == "C": self.C = val
		if reg == "D": self.D = val
		if reg == "E": self.E = val
		if reg == "H": self.H = val
		if reg == "L": self.L = val
		if reg == "M_HL": self.memory.write(self.get_HL(), val)

		if reg != "M_HL":
			self.cycles += 8
		else:
			self.cycles += 16

	def SLA(self, reg=""):

		if reg == "A": val = self.A
		if reg == "B": val = self.B
		if reg == "C": val = self.C
		if reg == "D": val = self.D
		if reg == "E": val = self.E
		if reg == "H": val = self.H
		if reg == "L": val = self.L
		if reg == "M_HL": val = self.memory.read(self.get_HL())

		if val & 0x80:
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		val = (val << 1) & 0xFF
		val &= 0xFE

		# Z - Set if result is zero
		if val == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

		# H - Reset
		self.flags["H"] = 0

		if reg == "A": self.A = val
		if reg == "B": self.B = val
		if reg == "C": self.C = val
		if reg == "D": self.D = val
		if reg == "E": self.E = val
		if reg == "H": self.H = val
		if reg == "L": self.L = val
		if reg == "M_HL": self.memory.write(self.get_HL(), val)

		if reg != "M_HL":
			self.cycles += 8
		else:
			self.cycles += 16

	def SRA(self, reg=""):

		if reg == "A": val = self.A
		if reg == "B": val = self.B
		if reg == "C": val = self.C
		if reg == "D": val = self.D
		if reg == "E": val = self.E
		if reg == "H": val = self.H
		if reg == "L": val = self.L
		if reg == "M_HL": val = self.memory.read(self.get_HL())

		if val & 0x01:
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		val = (val >> 1) & 0xFF

		# Z - Set if result is zero
		if val == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

		# H - Reset
		self.flags["H"] = 0

		if reg == "A": self.A = val
		if reg == "B": self.B = val
		if reg == "C": self.C = val
		if reg == "D": self.D = val
		if reg == "E": self.E = val
		if reg == "H": self.H = val
		if reg == "L": self.L = val
		if reg == "M_HL": self.memory.write(self.get_HL(), val)

		if reg != "M_HL":
			self.cycles += 8
		else:
			self.cycles += 16

	def SWAP(self, reg=""):

		if reg == "A": val = self.A
		if reg == "B": val = self.B
		if reg == "C": val = self.C
		if reg == "D": val = self.D
		if reg == "E": val = self.E
		if reg == "H": val = self.H
		if reg == "L": val = self.L
		if reg == "M_HL": val = self.memory.read(self.get_HL())

		high = (val & 0xFF00) >> 8
		low = val & 0x00FF
		val = (low << 8) | high

		# Z - Set if result is zero
		if val == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

		# H - Reset
		self.flags["H"] = 0

		# C - Reset
		self.flags["C"] = 0

		if reg == "A": self.A = val
		if reg == "B": self.B = val
		if reg == "C": self.C = val
		if reg == "D": self.D = val
		if reg == "E": self.E = val
		if reg == "H": self.H = val
		if reg == "L": self.L = val
		if reg == "M_HL": self.memory.write(self.get_HL(), val)

		if reg != "M_HL":
			self.cycles += 8
		else:
			self.cycles += 16

	def SRL(self, reg=""):

		if reg == "A": val = self.A
		if reg == "B": val = self.B
		if reg == "C": val = self.C
		if reg == "D": val = self.D
		if reg == "E": val = self.E
		if reg == "H": val = self.H
		if reg == "L": val = self.L
		if reg == "M_HL": val = self.memory.read(self.get_HL())

		if val & 0x01:
			self.flags["C"] = 1
		else:
			self.flags["C"] = 0

		val = (val >> 1) & 0xFF
		val &= 0x7F

		# Z - Set if result is zero
		if val == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

		# H - Reset
		self.flags["H"] = 0

		if reg == "A": self.A = val
		if reg == "B": self.B = val
		if reg == "C": self.C = val
		if reg == "D": self.D = val
		if reg == "E": self.E = val
		if reg == "H": self.H = val
		if reg == "L": self.L = val
		if reg == "M_HL": self.memory.write(self.get_HL(), val)

		if reg != "M_HL":
			self.cycles += 8
		else:
			self.cycles += 16

	def BIT(self, b=0, reg=""):

		if reg == "A": val = self.A
		if reg == "B": val = self.B
		if reg == "C": val = self.C
		if reg == "D": val = self.D
		if reg == "E": val = self.E
		if reg == "H": val = self.H
		if reg == "L": val = self.L
		if reg == "M_HL": val = self.memory.read(self.get_HL())

		# Z - Set if bit b of val is 0
		if val & (0x01 << b) == 0:
			self.flags["Z"] = 1
		else:
			self.flags["Z"] = 0

		# N - Reset
		self.flags["N"] = 0

		# H - Set
		self.flags["H"] = 1

		if reg == "A": self.A = val
		if reg == "B": self.B = val
		if reg == "C": self.C = val
		if reg == "D": self.D = val
		if reg == "E": self.E = val
		if reg == "H": self.H = val
		if reg == "L": self.L = val
		if reg == "M_HL": self.memory.write(self.get_HL(), val)

		if reg != "M_HL":
			self.cycles += 8
		else:
			self.cycles += 16

	def RES(self, b=0, reg=""):

		if reg == "A": val = self.A
		if reg == "B": val = self.B
		if reg == "C": val = self.C
		if reg == "D": val = self.D
		if reg == "E": val = self.E
		if reg == "H": val = self.H
		if reg == "L": val = self.L
		if reg == "M_HL": val = self.memory.read(self.get_HL())

		val &= ~(0x01 << b)

		if reg == "A": self.A = val
		if reg == "B": self.B = val
		if reg == "C": self.C = val
		if reg == "D": self.D = val
		if reg == "E": self.E = val
		if reg == "H": self.H = val
		if reg == "L": self.L = val
		if reg == "M_HL": self.memory.write(self.get_HL(), val)

		if reg != "M_HL":
			self.cycles += 8
		else:
			self.cycles += 16

	def SET(self, b=0, reg=""):

		if reg == "A": val = self.A
		if reg == "B": val = self.B
		if reg == "C": val = self.C
		if reg == "D": val = self.D
		if reg == "E": val = self.E
		if reg == "H": val = self.H
		if reg == "L": val = self.L
		if reg == "M_HL": val = self.memory.read(self.get_HL())

		val |= (0x01 << b)

		if reg == "A": self.A = val
		if reg == "B": self.B = val
		if reg == "C": self.C = val
		if reg == "D": self.D = val
		if reg == "E": self.E = val
		if reg == "H": self.H = val
		if reg == "L": self.L = val
		if reg == "M_HL": self.memory.write(self.get_HL(), val)

		if reg != "M_HL":
			self.cycles += 8
		else:
			self.cycles += 16
