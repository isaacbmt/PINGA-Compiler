import ply.lex as lex
import ply.yacc as yacc
from colorama import Fore
from colorama import Style
from utils import *
from variables import *


tokens = get_tokens()

t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = r','


def t_LABEL(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*:'
    t.type = 'LABEL'
    label = labels.get(t.value, '')
    if label == '':
        labels[t.value] = decToBin(t.lexer.lineno - len(labels), 15)
    return t


def t_HEX(t):
    r'0x[0-9a-fA-F]*'
    t.type = 'INT'
    t.value = hexToDec(t.value)
    return t


def t_REGISTER(t):
    r'[Rr][0-9]*'
    if int(t.value[1:]) > 31:
        print(f'{Fore.LIGHTRED_EX}El registro {t.value} no existe.{Style.RESET_ALL}')
    t.type = 'REGISTER'
    return t


def t_NEWLINE(t):
    r'\n'
    if t.lexer.lineno < 0:
        t.lexer.lineno -= 1
    else:
        t.lexer.lineno += 1


def t_COMMENT(t):
    r'(//.*?\n)'
    if t.lexer.lineno < 0:
        t.lexer.lineno -= 1
    else:
        t.lexer.lineno += 1


def t_INSTRUCTION(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = instructions_tokens.get(t.value.upper(), 'default')  # Check for reserved words

    if t.type == 'default':
        # print(f'{Fore.LIGHTRED_EX}La instruccion {t.type} no existe.{Style.RESET_ALL}')
        name = names.get(t.value, '')
        if t.lexer.lineno > 0:
            if name == '':
                names[t.value] = [decToBin(t.lexer.lineno + 1 - len(labels), 15)]
            else:
                names[t.value] = names.get(t.value) + [decToBin(t.lexer.lineno + 1 - len(labels), 15)]
        t.type = 'NAME'
    return t


def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_SEMI(t):
    r';'
    t.type = 'SEMI'
    return t


def t_error(t):
    print(f"{Fore.LIGHTRED_EX} Illegal character {t.value[0]} at line {abs(t.lineno)} {Style.RESET_ALL}")
    t.lexer.skip(1)


lexer = lex.lex()

precedence = (
)


def p_instruction_group(p):
    '''
    linesGroup  : linesGroup line
                | line
    '''
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]


def p_instruction_line(p):
    '''
    line        : instr SEMI
                | label
    '''
    if isinstance(p[1], dict):
        p[0] = 'label'
    else:
        p[0] = p[1]


def p_expression_memory(p):
    '''
    instr       : memInstr register COMMA LBRACKET register COMMA register RBRACKET
                | memInstr register COMMA LBRACKET register COMMA expression RBRACKET
                | memInstr register COMMA LBRACKET register RBRACKET
    '''
    op = instructions_mem.get(p[1])
    rd, ra1 = registers_data.get(p[2]), registers_data.get(p[5])
    if p[6] == ']':
        p[0] = buildImmMemInstr(op, rd, ra1, decToBin(0, 15))
    elif isinstance(p[7], int):
        p[0] = buildImmMemInstr(op, rd, ra1, decToBin(p[7], 15))
    else:
        ra2 = registers_data.get(p[7])
        p[0] = buildRegMemInstr(op, rd, ra1, ra2)


def p_expression_branch(p):
    '''
    instr       : branchInstr name
    '''
    op, cond = instructions_branch.get(p[1])
    startAddress = names.get(p[2][:-1], '')
    endAddress = labels.get(p[2], '')
    if endAddress == '' or startAddress == '':
        print(f'{Fore.LIGHTRED_EX}La dirección {Fore.RED}{p[2][:-1]}{Fore.LIGHTRED_EX} no existe.{Style.RESET_ALL}')
        parser.errok()
    else:
        namelist = names.get(p[2][:-1])
        names[p[2][:-1]] = namelist[1:] + [namelist[0]]
        address = int(endAddress, 2) - int(startAddress[0], 2)
        address = decToBin(address, 15) if address >= 0 else twoComplement(str(address)[1:])
        p[0] = buildBranchInstr(op, cond, address)


def p_expression_mov(p):
    '''
    instr       : MOV register COMMA expression
                | MOV register COMMA register
    '''
    op, func, sflag = instructions_data.get(p[1].upper())
    rd, ra1 = registers_data.get(p[2]), registers_data.get(p[4])
    if isinstance(p[4], int):
        p[0] = buildImmDataInstr(op, rd, '00000', decToBin(p[4], 15), sflag, func)
    else:
        p[0] = buildRegDataInstr(op, rd, '00000', ra1, sflag, func)


def p_expression_cmp(p):
    '''
    instr       : CMP register COMMA expression
                | CMP register COMMA register
    '''
    op, func, sflag = instructions_data.get(p[1].upper())
    rd, ra1 = registers_data.get(p[2]), registers_data.get(p[4])
    if isinstance(p[4], int):
        p[0] = buildImmDataInstr(op, '00000', rd, decToBin(p[4], 15), sflag, func)
    else:
        p[0] = buildRegDataInstr(op, '00000', rd, ra1, sflag, func)


def p_expression_arithmetic(p):
    '''
    instr       : dataInst register COMMA register COMMA expression
                | dataInst register COMMA register COMMA register
    '''
    op, func, sflag = instructions_data.get(p[1])
    rd, ra1 = registers_data.get(p[2]), registers_data.get(p[4])
    if isinstance(p[6], int):
        p[0] = buildImmDataInstr(op, rd, ra1, decToBin(p[6], 15), sflag, func)
    else:
        ra2 = registers_data.get(p[6])
        p[0] = buildRegDataInstr(op, rd, ra1, ra2, sflag, func)


def p_int(p):
    '''
    expression  : INT
    '''
    p[0] = p[1]


def p_label(p):
    '''
    label       : LABEL
    '''
    p[0] = {'label': p[1]}


def p_name(p):
    '''
    name        : NAME
    '''
    p[0] = p[1] + ':'


def p_register(p):
    '''
    register    : REGISTER
    '''
    p[0] = p[1].upper()


def p_arithmetic(p):
    '''
    dataInst    : ADD
                | SUB
                | DIV
                | MUL
                | LST
                | SLL
                | SRL
                | MOD
    '''
    p[0] = p[1].upper()


def p_memory(p):
    '''
    memInstr    : LDR
                | STR
    '''
    p[0] = p[1].upper()


def p_branch(p):
    '''
    branchInstr : B
                | BEQ
    '''
    p[0] = p[1].upper()


def p_error(p):
    try:
        print(f"{Fore.LIGHTRED_EX} Line {abs(lexer.lineno)}: Syntax error on '{p.value}' {Style.RESET_ALL}")
    except AttributeError:
        print(f"{Fore.LIGHTRED_EX}Line {abs(lexer.lineno)}: Syntax error {Style.RESET_ALL}")


s = readFile('newprogram.asm').rstrip('\n').rstrip(' ')
lexer.input(s)
while True:
    tok = lexer.token()
    if not tok:
        break

lexer.lineno = -1
parser = yacc.yacc()
result = parser.parse(s, lexer=lexer)
print(result)
print('labels: ', labels)
print('names: ', names)

with open('instrucciones.txt', 'w') as f:
    for item in result:
        if item != 'label':
            f.write("%s\n" % toHex(item))
