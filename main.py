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
# t_SEMI = r';'

def t_LABEL(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*:'
    t.type = 'LABEL'
    return t


def t_REGISTER(t):
    r'[Rr][0-9]*'
    if int(t.value[1:]) > 31:
        print(f'{Fore.LIGHTRED_EX}El registro {t.value} no existe.{Style.RESET_ALL}')
    t.type = 'REGISTER'
    return t


def t_INSTRUCTION(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = instructions_tokens.get(t.value.upper(), 'default')  # Check for reserved words

    if t.type == 'default':
        print(f'{Fore.LIGHTRED_EX}La instruccion {t.type} no existe.{Style.RESET_ALL}')
        t.type = 'ADD'
    return t


def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_EOL(t):
    r';'
    t.lexer.lineno += 1


def t_COMMENT(t):
    r'//.*\n'
    t.lexer.lineno += 1
    return t


def t_error(t):
    print("Illegal characters!")
    t.lexer.skip(1)


lexer = lex.lex()

precedence = (
)


def p_int(p):
    '''
    expression : INT
    '''
    p[0] = p[1]


def p_register(p):
    '''
    register   : REGISTER
    '''
    p[0] = p[1].upper()


def p_arithmetic(p):
    '''
    dataInst    : ADD
                | SUB
                | DIV
                | MUL
                | LST
                | LSL
                | LSR
                | MOD
    '''
    p[0] = p[1].upper()


def p_memory(p):
    '''
    memInstr    : LDR
                | STR
    '''
    p[0] = p[1].upper()


def p_expression_memory(p):
    '''
    expression  : memInstr register COMMA LBRACKET register COMMA register RBRACKET
                | memInstr register COMMA LBRACKET register COMMA expression RBRACKET
                | memInstr register COMMA LBRACKET register RBRACKET
    '''
    op = instructions_mem.get(p[1])
    rd, ra1 = registers_data.get(p[2]), registers_data.get(p[5])
    if p[6] == ']':
        p[0] = buildImmMemInstr(op, rd, ra1, toBin(0, 15))
    elif isinstance(p[7], int):
        p[0] = buildImmMemInstr(op, rd, ra1, toBin(p[7], 15))
    else:
        ra2 = registers_data.get(p[7])
        p[0] = buildRegMemInstr(op, rd, ra1, ra2)


def p_expression_mov(p):
    '''
    dataInstM   : MOV register COMMA expression
                | MOV register COMMA register
    '''
    op, func, sflag = instructions_data.get(p[1].upper())
    rd, ra1 = registers_data.get(p[2]), registers_data.get(p[4])
    if isinstance(p[4], int):
        p[0] = buildImmDataInstr(op, rd, '00000', toBin(p[4], 15), sflag, func)
    else:
        p[0] = buildRegDataInstr(op, rd, '00000', ra1, sflag, func)


def p_expression_cmp(p):
    '''
    dataInstC   : CMP register COMMA expression
                | CMP register COMMA register
    '''
    op, func, sflag = instructions_data.get(p[1].upper())
    rd, ra1 = registers_data.get(p[2]), registers_data.get(p[4])
    if isinstance(p[3], int):
        p[0] = buildImmDataInstr(op, rd, rd, toBin(p[4], 15), sflag, func)
    else:
        p[0] = buildRegDataInstr(op, rd, rd, ra1, sflag, func)


def p_expression_arithmetic(p):
    '''
    expression  : dataInst register COMMA register COMMA expression
                | dataInst register COMMA register COMMA register
    '''
    op, func, sflag = instructions_data.get(p[1])
    rd, ra1 = registers_data.get(p[2]), registers_data.get(p[4])
    if isinstance(p[6], int):
        p[0] = buildImmDataInstr(op, rd, ra1, toBin(p[6], 15), sflag, func)
    else:
        ra2 = registers_data.get(p[6])
        p[0] = buildRegDataInstr(op, rd, ra1, ra2, sflag, func)


def p_error(p):
    print('Syntax error')


parser = yacc.yacc()

labels = {}
#
#
# lexer.input('ADD r2 r31 4')
#
#
# while True:
#     try:
#         s = input('>> ')
#     except EOFError:
#         break
s = readFile('test.S')
result = parser.parse(s)
print(result)

#
# while True:
#     tok = lexer.token()
#     if not tok:
#         break
#     print(tok)
