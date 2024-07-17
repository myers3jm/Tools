import string
import sys
import re
from collections import UserDict

DEBUG = True
def debug(string: str):
    if (DEBUG):
        print(string)

class Report:
    def __init__(self, filename: str, distribution: dict, wordset: list, wordcounts: dict, iso639_3_mappings: dict):
        self.filename = filename
        self.wordset = wordset
        self.distribution = distribution
        self.wordcounts = wordcounts
        self.iso639_3_mappings = iso639_3_mappings

    def __repr__(self) -> str:
        ret = f'# Etymology Report for {self.filename}\n'
        languageSummary = "## Modernized Distribution Summary\n"
        summary = '## Distribution Summary\n'
        body = '## Linguistic Distribution\n'
        simpleDistribution = {}
        settings = ['middle', 'old', 'ancient', 'north', 'south', 'east', 'west']
        for key in sorted(self.distribution.keys(), key=lambda k: len(self.distribution[k]), reverse=True):
            value = distribution[key]
            if len(value) > 0:
                heading = iso639_3_mappings[key].split('(', 1)[0].strip()
                url = heading.replace(' ', '-')
                summary += f'### [{heading}](#{url}): {round(100 * (len(value) / self.getDistinctCount()), 2)}%\n'
                body += f'### {heading}\n#### {round(100 * (len(value) / self.getDistinctCount()), 2)}%\n'
                for word in self.getDistributionValues(key):
                    body += f'{word} - {self.wordcounts[word]}\n'
                    if len(self.getDistributionValues(key)) > 1:
                        body += '\n'
                body += '\n\n'
                simple = str.join(' ', [x.title() for x in heading.split() if x.lower() not in settings]).strip()
                if simple in simpleDistribution.keys():
                    simpleDistribution[simple] += round(100 * (len(value) / self.getDistinctCount()), 2)
                else:
                    simpleDistribution[simple] = round(100 * (len(value) / self.getDistinctCount()), 2)
        languageSummary += str.join('\n', [f'### {x}: {simpleDistribution[x]}%' for x in simpleDistribution.keys()]) + '\n'
        
        ret += languageSummary + '\n'
        ret += summary + '\n'
        ret += body.rstrip()

        return ret
    
    # return: the number of distinct words in the document, case insensitive
    def getDistinctCount(self) -> int:
        return len(self.wordset)
    
    # key: A language abbreviation
    # return: Words present in the document, sorted by frequency
    def getDistributionValues(self, key: str) -> list:
        return sorted(self.distribution[key],  key=lambda word: self.wordcounts[word], reverse=True)

class Etymology:
    def __init__(self, item: str, iso639_3_mappings: dict):
        data = item.split('\t')
        self.word = re.sub(r'^.*?: ', '', data[0])
        self.relationship = data[1]#[data[1].rfind(':'):].lstrip(': ')
        self.relative = data[2]#[data[2].rfind(':'):].lstrip(': ')
        self.origin = data[2][:data[2].rfind(':')].rstrip(': ')
        self.trueOrigin = self.origin
        self.iso639_3_mappings = iso639_3_mappings
    
    def __repr__(self):
        return f'{self.word} | {self.relationship} | {self.relative} | {self.origin} ({self.trueOrigin})\n'
    
    def deduceOrigin(self, net) -> str: # type: ignore
        deductionSteps = []
        def deduce(word: str, n: Net): # type: ignore
            word = clean(word)
            if word in net.keys():
                deductionSteps.append(net[word])
            # base cases
            if word not in net.keys():
                return self.origin
            if (net[word].origin != 'eng'):
                return net[word].origin

            # recursive case
            else:
                tempOrigin = net[word].origin
                relative = clean(net[word].relative)
                if relative not in net.keys():
                    return tempOrigin
                return net[relative].origin
        
        ret = f'{deduce(self.word, net)}\n'
        for deduction in deductionSteps:
            ret += f'\t{deduction}\n'
        self.trueOrigin = deduce(self.word, net)
        return ret

class Net(UserDict):
    def __repr__(self):
        return f'Language: English\nEntries: {len(self.keys())}\nAncestor Languages: {len(self.getLanguages())}\n'
    
    def getLanguages(self):
        return sorted(set([x.origin for x in self.values()]))

def clean(string: str) -> str:
    cleanWord = re.sub('\s', '', string)
    cleanWord = cleanWord.rstrip('\'')
    cleanWord = cleanWord.lstrip('\'')
    cleanWord = re.sub(r'^.*?: ', '', cleanWord)

    return cleanWord

if __name__ == '__main__':
    args = sys.argv
    if len(args) < 1:
        debug("Missing argument 'input file'")
        sys.exit()
    filename = args[1]
    if len(filename) == 0: sys.exit()
    
    origins = []
    iso639_3_mappings = {}
    with open('./etymology/iso-639-3_Name_Index.tab', 'r', encoding='utf8') as file:
        origins = [x.split('\t') for x in file.read().split('\n') if len(x.split('\t')) > 1]
        origins = origins[1:]
        for item in origins:
            iso639_3_mappings[item[0]] = item[1]

    with open('./etymology/etymwn.tsv', 'r', encoding='utf8') as file:
        def passesFilter(x: str) -> bool:
            if '!OED' in x: return False
            lst = x.split('\t')
            if len(lst) != 3: return False
            word = lst[0].lower().strip()
            relationship = lst[1].lower().strip()
            relative = lst[2].lower().strip()
            if 'eng:' not in word or '-' in word or len(word.split(' ')) > 2: return False
            if 'etymology' not in relationship and 'is_derived_from' not in relationship: return False
            if '-' in relative: return False
            
            return True

        net = Net({x.split('\t')[0].split()[1]: Etymology(x, iso639_3_mappings) for x in file.read().split('\n') if passesFilter(x)})
        for key in net.keys():
            net[key].deduceOrigin(net)

        if DEBUG:
            with open('./debug.txt', 'w', encoding='utf8') as file:
                for key in net.keys():
                    # debug(f'{key} ===> {net[key]}\n')
                    file.write(f'{key} ===> {net[key]}\n')
        
        debug(net)

        #origins = [x.split('\t') for x in data.split('\n') if ('eng:' in x.split('\t')[0] and 'rel:etymology' in x.split('\t')[1] and '-' not in x.split('\t')[2])] #  and 'eng:' not in x.split('\t')[2]
        #derivations = [x.split('\t') for x in data.split('\n') if ('eng:' in x.split('\t')[0] and 'OED-->' not in x.split('\t')[0] and 'OED2' not in x.split('\t')[0] and 'rel:is_derived_from' in x.split('\t')[1] and '-' not in x.split('\t')[2] and 'OED2' not in x.split('\t')[2] and 'OED-->' not in x.split('\t')[2])]
        ancestorLangs = net.getLanguages()

    wordset = set()
    wordcounts = {}

    with open(filename, 'r', encoding='utf8') as file:
        uncommented = re.sub('(?s)<!--.*-->', '', file.read(), 0, re.M)
        words = [x.translate(str.maketrans('', '', string.punctuation.replace('\'', ''))).lower().strip() + '\n' for x in re.split('\s+', uncommented) if len(x.translate(str.maketrans('', '', string.punctuation.replace('\'', ''))).lower().strip()) > 2]
        for word in words:
            cleanWord = clean(word)
            if cleanWord in wordcounts.keys():
                wordcounts[cleanWord] += 1
            else:
                wordcounts[cleanWord] = 1
        wordset = sorted(set([re.sub('\s', '', x.rstrip('\'\n').lstrip('\'').replace('"', '')) for x in words if len(x.strip()) > 0]))
    
    debug(f'{len(wordset)} unique words')
    
    etymologies = {}
    distribution = {}

    for abbrv in ancestorLangs:
        distribution[abbrv] = set()

    for word in wordset:
        cleanWord = clean(word)
        if cleanWord in etymologies.keys() and etymologies[cleanWord] in distribution.keys():
            distribution[etymologies[cleanWord].deduceOrigin(net)].add(cleanWord)
        else:
            if (cleanWord in net.keys()):
                etymologies[cleanWord] = net[cleanWord]
                etymologies[cleanWord].deduceOrigin(net)
                distribution[etymologies[cleanWord].trueOrigin].add(cleanWord)

    foundWords = set()
    debug(f'Distribution keys: {len(distribution.keys())}')
    for key in distribution.keys():
        if (len(distribution[key]) > 0):
            debug(f'{key}: {len(distribution[key])}')
        for value in distribution[key]:
            foundWords.add(value)

    debug(f'{len(foundWords)} words found in the dictionary')

    notFoundWords = set([re.sub('\s', '', x) for x in wordset if re.sub('\s', '', x) not in foundWords])
    debug(f'{len(notFoundWords)} words not found in the dictionary')
    debug(f'{len(foundWords)} + {len(notFoundWords)} = {len(foundWords) + len(notFoundWords)} : {len(wordset)}')

    if DEBUG:
        with open('./debug.txt', 'w') as file:
            notFoundStr = str.join("\n", sorted(notFoundWords))
            file.write(f'{notFoundStr}')
            file.write('###')
            foundStr = str.join("\n", sorted(foundWords))
            file.write(f'{foundStr}\n\n')
    
    report = Report(filename, distribution, wordset, wordcounts, iso639_3_mappings)
    
    reportFilePath = f'{filename.split(".")[0]}_report.md'
    with open(reportFilePath, 'w') as file:
        file.write(str(report))