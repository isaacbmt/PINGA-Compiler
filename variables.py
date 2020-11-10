# --------------------------------------
# ---------------Tokens-----------------
# --------------------------------------

types = [
    'INT',
    'LABEL'
]

registers = {
    'R0': 'R0',
    'R1': 'R1',
    'R2': 'R2',
    'R3': 'R3',
    'R4': 'R4',
    'R5': 'R5',
    'R6': 'R6',
    'R7': 'R7',
    'R8': 'R8',
    'R9': 'R9',
    'R10': 'R10',
    'R11': 'R11',
    'R12': 'R12',
    'R13': 'R13',
    'R14': 'R14',
    'R15': 'R15',
    'R16': 'R16',
    'R17': 'R17',
    'R18': 'R18',
    'R19': 'R19',
    'R20': 'R20',
    'R21': 'R21',
    'R22': 'R22',
    'R23': 'R23',
    'R24': 'R24',
    'R25': 'R25',
    'R26': 'R26',
    'R27': 'R27',
    'R28': 'R28',
    'R29': 'R29',
    'R30': 'R30',
    'R31': 'R31'
}

instructions = {
    'ADD': 'ADD',
    'SUB': 'SUB',
    'DIV': 'DIV',
    'MUL': 'MUL',
    'LST': 'LST',   #Less than
    'LSL': 'LSL',
    'LSR': 'LSR',
    'MOD': 'MOD',
    'LDR': 'LDR',
    'STR': 'STR',
    'MOV': 'MOV',
    'CMP': 'CMP',
    'B': 'B',
    'BEQ': 'BEQ'
}


def get_tokens():
    return types + list(instructions.values()) + list(registers.values())

# --------------------------------------
# ----------Regular expressions---------
# --------------------------------------


t_ignore = r' '

# -------------Instructions-------------


# --------------Registers--------------
