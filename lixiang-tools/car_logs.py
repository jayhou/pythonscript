import fileinput
import re

PATTEN = 'Property.service|CAR.HAL|DIAG.SERVICE'
PATTENS = PATTEN.split('|')
COLOR_PATTENS = PATTEN.split(' ')
for pat in PATTENS:
    pat = '\033[1;33m'+pat+'\033[0m'
    COLOR_PATTENS.append(pat)
    print(pat)

with fileinput.input() as f_input:
    patten = re.compile(PATTEN)
    for line in f_input:
        if patten.findall(line):
            result = ''
            for pat2 in PATTENS:
                if line.__contains__(pat2):
                    # print(pat2 + " in " + line)
                    # print("index:" + str(PATTENS.index(pat2) + 1))
                    # print("color pat:" + COLOR_PATTENS.__getitem__(PATTENS.index(pat2) + 1))
                    result = eval(repr(line).replace(pat2,COLOR_PATTENS.__getitem__(PATTENS.index(pat2) + 1)))
            print(line, end='')