def toBin(num, length):
    num = format(num, 'b')
    while len(num) < length:
        num = '0' + num
    return num


def buildRegDataInstr(op, rd, ra1, ra2, sflag, func):
    return op + '0' + rd + ra1 + ra2 + '0000000000' + sflag + func


def buildImmDataInstr(op, rd, ra1, imm, sflag, func):
    return op + '1' + rd + ra1 + imm + sflag + func