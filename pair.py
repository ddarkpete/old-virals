import sys

for line in sys.stdin:
    line = line.split('\t')
    if int(line[0]) == 1232935 or int(line[0]) == 340238:
        print(line[0])
        print(line[1])
        print(line[4])
        print()