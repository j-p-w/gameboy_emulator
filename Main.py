import time

from CPU import CPU
from GPU import GPU
from Memory import Memory

RUNNING = True
STEP = False

# Memory Init
Memory = Memory("TETRIS.gb")

# CPU Init
CPU = CPU(Memory)
CPU.DEBUG = False

# GPU Init, pass in the memory that has been initialized in the CPU
GPU = GPU(Memory)

time_display = time.clock()

while RUNNING:


    if CPU.PC > 0xFF:
        STEP = True
        print("REACHED THE ACTUAL GAME...")
    cycles_before = CPU.cycles
    CPU.fetch()
    if STEP:
        print("0x" + hex(CPU.PC)[2:].zfill(4).upper() + " : ", end="")
        CPU.decode()
        print(CPU.debug_string + "	",end="")
        for i in range(0,CPU.instruction_length-1):
            print(hex(CPU.args[i])[2:].zfill(2).upper() + " ", end="")
        print("")
        CPU.print_registers()
        input()
    else:
        CPU.decode()

    CPU.execute()
    cycles_after = CPU.cycles
    cycles_passed = cycles_after - cycles_before
    GPU.update(cycles_passed)











































#
