import ply.lex as lex
import ply.yacc as yacc
from colorama import Fore
from colorama import Style
from utils import toBin
from variables import *


tokens = get_tokens()


def t_LABEL(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*:'
    t.type = 'LABEL'
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = instructions.get(t.value, 'default')  # Check for reserved words

    if t.type == 'default':
        t.type = registers.get(t.value, 'default')  # Check for reserved words

        if t.type == 'default':
            print(f'{Fore.LIGHTRED_EX}La instruccion {t.type} no existe.{Style.RESET_ALL}')
            t.type = 'ADD'
    return t


# def t_NAME(t):
#     r'[a-zA-Z_][a-zA-Z_:0-9]*'
#     t.type = 'NAME'
#     return t


def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_error(t):
    print("Illegal characters!")
    t.lexer.skip(1)


lexer = lex.lex()

# precedence = (
#
# )

lexer.input('ADD GOL SUB MUL R2 R6 4')

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
