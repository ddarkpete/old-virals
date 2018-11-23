from fuzzywuzzy import fuzz
import fingerfood as fd

import sys

data = []

for line in sys.stdin:
    line = line.split('\t')
    line[4] = line[4].lower()
    #line.append(fd.Fingerprint(line[4]))
    data.append(line)
    print('Preprocess in progress...')

print('Preprocess finished!')

for i in range(0,len(data) - 1):
    for j in range(i + 1, len(data)):
        '''
        matches = data[i][5].compare_with(data[j][5])
        if matches:
            print('find matches in  {} and {}'.format(data[i][0], data[j][0]))
            for match in matches:
                print(match)
        else:
            print('any matches')
        '''
        print("{}\t{}\t{}".format(fuzz.token_sort_ratio(data[i][4], data[j][4]), data[i][0], data[j][0]))