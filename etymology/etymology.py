import string
import sys
import re
import math

if __name__ == '__main__':
    args = sys.argv
    if len(args) < 1:
        print("Missing argument 'input file'")
        sys.exit()
    filename = args[1]
    if len(filename) == 0: sys.exit()

    data = []
    with open('./etymology/etymwn.tsv', 'r', encoding='utf8') as file:
        data = [x.split('\t') for x in file.read().split('\n') if ('eng:' in x.split('\t')[0] and 'rel:etymology' in x.split('\t')[1] and '-' not in x.split('\t')[2] and 'eng:' not in x.split('\t')[2])]
        abbrvs = sorted(set([x[2][:x[2].rfind(':')] for x in data]))

    wordset = set()
    with open(filename, 'r', encoding='utf8') as file:
        words = [x.translate(str.maketrans('', '', string.punctuation)).lower().strip() + '\n' for x in re.split('\W+', file.read()) if len(x.translate(str.maketrans('', '', string.punctuation)).lower().strip()) > 0]
        wordset = sorted(set([x for x in words if len(x.strip()) > 0]))

        print(f'{len(wordset)} unique words')
    
    etymologies = {}
    for item in data:
        word = item[0][item[0].rfind(':'):].lstrip(': ')
        etymologies[word] = item[2][:item[2].rfind(':')].strip()

    distribution = {}
    for abbrv in abbrvs:
        distribution[abbrv] = set()

    for word in wordset:
        cleanWord = re.sub('\W', '', word)
        if cleanWord in etymologies.keys() and etymologies[cleanWord] in distribution.keys():
            distribution[etymologies[cleanWord]].add(cleanWord)
    
    iso639_3_mappings = {}
    with open('./etymology/iso-639-3_Name_Index.tab', 'r', encoding='utf8') as file:
        data = [x.split('\t') for x in file.read().split('\n') if len(x.split('\t')) > 1]
        data = data[1:]
        for item in data:
            iso639_3_mappings[item[0]] = item[1]

    for key in sorted(distribution.keys(), key=lambda k: len(distribution[k]), reverse=True):
        value = distribution[key]
        if len(value) > 0:
            print(f'{iso639_3_mappings[key]}: {round(100 * (len(value) / len(wordset)), 2)}%')