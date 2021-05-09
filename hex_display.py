import sys

FILE = None
SCALE = 16  # by default


def parse_flags(flags: list):
    global FILE, SCALE
    l_f = len(flags)
    if l_f == 1:
        print("ERROR: Could not find any executable file")
        exit(0)
    if l_f >= 2:
        try:
            with open(sys.argv[1], 'rb') as file:
                FILE = file.read()
        except IOError as e:
            print(e)
            exit(0)
        if l_f == 3:
            # format -as8
            SCALE = int(sys.argv[l_f - 1][3:])


PRINTABLE = [chr(i) for i in range(32, 127)]

if __name__ == '__main__':

    i, j = 0, 0
    addr = 0
    parse_flags(sys.argv)
    characters = []
    for line in FILE:
        if i % (SCALE + 1) == 0:
            address = '{:08x}'.format(addr)
            print(f'0x{address}\t ', end='')
            addr += SCALE
        content = hex(int(line))[2:]
        characters.append(int('0x' + str(content), 16))
        print(f'{"0" + str(content) if len(content) == 1 else str(content)} ', end='')
        i += 1
        j += 1
        if j % (SCALE + 1) == 0:
            characters = list(reversed(characters))
            print('\t ', end='')
            while len(characters) != 0:
                x = chr(characters.pop())
                print(f'{" " if x not in PRINTABLE else x}', end='')
            print()
