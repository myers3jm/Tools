# Generations.py
#
# Estimate the number of generations over a certain number of years given a list of average lifespans during that time

import sys

if __name__ == '__main__':
    # Check args
    args = sys.argv
    if len(args) <= 1:
        print('Please invoke the command as follows:')
        print('\tgenerations.py <number-of-years> [average lifespans]')
        print('For example:')
        print('\tgenerations.py 4000 40 60 40 70 50 35 40')
    
    # Collect args
    years = int(args[1])
    lifespans = [int(x) for x in args[2:]]

    # Calculate generations
    eras = len(lifespans)
    era_length = years // eras
    
    generations = 0
    for lifespan in lifespans:
        generations += era_length // lifespan
    print(generations)
