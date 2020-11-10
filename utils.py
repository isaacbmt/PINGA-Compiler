def toBin(num, length):
    num = format(num, 'b')
    while len(num) < length:
        num = '0' + num
    return num


# print('registers = {')
#
# for i in range(32):
#     string = '\'R{}\': \'R{}\''.format(i, i) + ','
#     print(string)
# print('}')
