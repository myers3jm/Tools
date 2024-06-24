import string
import sys
import re
import math

class Report:
    def __init__(self, filename: str, distribution: dict, wordset: list, wordcounts: dict, iso639_3_mappings: dict):
        self.wordset = wordset
        self.distribution = distribution
        self.wordcounts = wordcounts
        self.iso639_3_mappings = iso639_3_mappings

    def __repr__(self) -> str:
        ret = f'# Etymology Report for {filename}\n'

        ret += '## Distribution Summary\n'

        for key in sorted(distribution.keys(), key=lambda k: len(distribution[k]), reverse=True):
            value = distribution[key]
            if len(value) > 0:
                ret += f'### {iso639_3_mappings[key]}: {round(100 * (len(value) / self.getDistinctCount()), 2)}%\n'

        ret += '\n---\n\n'

        ret += "## Linguistic Distribution\n"

        for key in sorted(self.distribution.keys(), key=lambda k: len(self.distribution[k]), reverse=True):
            value = self.distribution[key]
            if len(value) > 0:
                ret += f'### {self.iso639_3_mappings[key]}\n#### {round(100 * (len(value) / self.getDistinctCount()), 2)}%\n'
                for word in self.getDistributionValues(key):
                    ret += f'{word} - {self.wordcounts[word]}\n'
                    if len(self.getDistributionValues(key)) > 1:
                        ret += '\n'
                ret += '\n\n'
        return ret
    
    # return: the number of distinct words in the document, case insensitive
    def getDistinctCount(self) -> int:
        return len(self.wordset)
    
    # key: A language abbreviation
    # return: Words present in the document, sorted by frequency
    def getDistributionValues(self, key: str) -> list:
        return sorted(self.distribution[key],  key=lambda word: self.wordcounts[word], reverse=True)

if __name__ == '__main__':
    args = sys.argv
    if len(args) < 1:
        print("Missing argument 'input file'")
        sys.exit()
    filename = args[1]
    if len(filename) == 0: sys.exit()

    data = []
    wordset = set()
    wordcounts = {}
    etymologies = {}
    distribution = {}
    iso639_3_mappings = {}
    
    with open('./etymology/etymwn.tsv', 'r', encoding='utf8') as file:
        data = [x.split('\t') for x in file.read().split('\n') if ('eng:' in x.split('\t')[0] and 'rel:etymology' in x.split('\t')[1] and '-' not in x.split('\t')[2] and 'eng:' not in x.split('\t')[2])]
        abbrvs = sorted(set([x[2][:x[2].rfind(':')] for x in data]))

    with open(filename, 'r', encoding='utf8') as file:
        words = [x.translate(str.maketrans('', '', string.punctuation)).lower().strip() + '\n' for x in re.split('\W+', file.read()) if len(x.translate(str.maketrans('', '', string.punctuation)).lower().strip()) > 2]
        wordset = sorted(set([x for x in words if len(x.strip()) > 0]))

        print(f'{len(wordset)} unique words')
    
    for item in data:
        word = item[0][item[0].rfind(':'):].lstrip(': ')
        if word in wordcounts.keys():
            wordcounts[word] += 1
        else:
            wordcounts[word] = 1
        etymologies[word] = item[2][:item[2].rfind(':')].strip()

    for abbrv in abbrvs:
        distribution[abbrv] = set()

    for word in wordset:
        cleanWord = re.sub('\W', '', word)
        if cleanWord in etymologies.keys() and etymologies[cleanWord] in distribution.keys():
            distribution[etymologies[cleanWord]].add(cleanWord)
    
    with open('./etymology/iso-639-3_Name_Index.tab', 'r', encoding='utf8') as file:
        data = [x.split('\t') for x in file.read().split('\n') if len(x.split('\t')) > 1]
        data = data[1:]
        for item in data:
            iso639_3_mappings[item[0]] = item[1]

    report = Report(filename, distribution, wordset, wordcounts, iso639_3_mappings)
    
    reportFilePath = filename + '_report.md'
    with open(reportFilePath, 'w') as file:
        file.write(str(report))