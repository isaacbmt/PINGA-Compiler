# --------------------------------------
# ---------------Tokens-----------------
# --------------------------------------

types = [
    'INT',
    'REGISTER',
    'LABEL',
    'COMMENT'
]

delimiters = [
    'LBRACKET',
    'RBRACKET',
    'COMMA',
    'SEMI'
]

instructions_tokens = {
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
    'B'  : 'B',
    'BEQ': 'BEQ',
    'NAME': 'NAME'
}


def get_tokens():
    return types + list(instructions_tokens.values()) + delimiters
    # return types + list(instructions.values()) + list(registers.values())


# --------------------------------------
# ----------Regular expressions---------
# --------------------------------------

t_ignore = " "


# -------------Instructions-------------
# Format:  [ op , func , SFlag ]
instructions_data = {
    'ADD': ['00', '000', '0'],
    'SUB': ['00', '001', '1'],
    'DIV': ['00', '010', '0'],
    'MUL': ['00', '011', '0'],
    'LST': ['00', '100', '1'],   #Less than
    'LSL': ['00', '101', '0'],
    'LSR': ['00', '110', '0'],
    'MOD': ['00', '111', '0'],
    'MOV': ['00', '000', '0'],
    'CMP': ['00', '001', '1']
}

# Format:   op
instructions_mem = {
    'LDR': '10',
    'STR': '11'
}

# Format:  [ op  cond ]
instructions_branch = {
    'B'  : ['01', '0'],
    'BEQ': ['01', '1']
}


# --------------Labels--------------
labels = {

}

names = {

}

# --------------Registers--------------
registers_data = {
     'R0': '00000',
     'R1': '00001',
     'R2': '00010',
     'R3': '00011',
     'R4': '00100',
     'R5': '00101',
     'R6': '00110',
     'R7': '00111',
     'R8': '01000',
     'R9': '01001',
     'R10': '01010',
     'R11': '01011',
     'R12': '01100',
     'R13': '01101',
     'R14': '01110',
     'R15': '01111',
     'R16': '10000',
     'R17': '10001',
     'R18': '10010',
     'R19': '10011',
     'R20': '10100',
     'R21': '10101',
     'R22': '10110',
     'R23': '10111',
     'R24': '11000',
     'R25': '11001',
     'R26': '11010',
     'R27': '11011',
     'R28': '11100',
     'R29': '11101',
     'R30': '11110',
     'R31': '11111'
}
