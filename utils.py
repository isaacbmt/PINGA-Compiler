def decToBin(num, length):
    num = format(num, 'b')
    while len(num) < length:
        num = '0' + num
    return num


def hexToDec(num):
    num = int(num, 16)
    return num


def toHex(str):
    length = len(str) / 4
    num = hex(int(str, 2))[2:]
    while len(num) < length:
        num = '0' + num
    return num


def twoComplement(num):
    aux = 32767
    return format((aux - int(num)) + 1, 'b')


def buildRegDataInstr(op, rd, ra1, ra2, sflag, func):
    return op + '0' + rd + ra1 + ra2 + '0000000000' + sflag + func


def buildImmDataInstr(op, rd, ra1, imm, sflag, func):
    return op + '1' + rd + ra1 + imm + sflag + func


def buildRegMemInstr(op, rd, ra1, ra2):
    return op + '0' + rd + ra1 + ra2 + '00000000000000'


def buildImmMemInstr(op, rd, ra1, imm):
    return op + '1' + rd + ra1 + imm + '0000'


def buildBranchInstr(op, cond, address):
    return op + cond + '0000000000' + address + '0000'


def readFile(filename):
    with open(filename, "r") as file:
        return file.read()
