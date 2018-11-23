import sys

for line in sys.stdin:
    line = line.split('\t')
    line[4] = line[4].replace('\\','').replace('//','').replace('---0---','').replace('---','').replace('  0  ', '').replace(' . ', '')
    tempLine = line[4].lower()
    if 'aligator' in tempLine:
        print(line[0] + '\t' + line[1] + '\t' + line[2] + '\t' + line[3] + '\t' + line[4][:-1])