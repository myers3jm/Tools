import sys
import string

if __name__ == '__main__':
    # Get command-line arguments
    args = sys.argv
    if len(args) < 1:
        print('Missing argument "input file"')
        sys.exit()

    # Extract input_file_name from args
    input_file_name = args[1]
    output_file_name = args[2]
    if len(input_file_name) == 0 or len(output_file_name) == 0:
        print('Insufficient filename(s) supplied')
        sys.exit()
    
    parsed = []
    # Open the supplied file
    with open(input_file_name, 'r', encoding='utf8') as file:
        raw = file.readlines()
        # Clean the lines
        index = raw.index([x for x in raw if '@@' in x][0]) + 1
        trimmed = [x for x in raw[index:] if '\\ No newline at end of file' not in x]
        colored = []
        for x in trimmed:
            n = x
            # Handle table items
            if n.startswith('-|'):
                n = f'|<p style="color:red">{n.removesuffix('\n').removeprefix('-|')}</p>\n'
            elif n.startswith('+|'):
                n = f'|<p style="color:green">{n.removesuffix('\n').removeprefix('+|')}</p>\n'
            # Handle headings
            elif n.startswith('-#'):
                n = n.removeprefix('-')
                header_size = n.count('#')
                n = n.replace('#', '').strip()
                n = f'{"#" * header_size} <h{header_size} style="color:red">-{n}</h{header_size}>'
            elif n.startswith('+#'):
                n = n.removeprefix('+')
                header_size = n.count('#')
                n = n.replace('#', '').strip()
                n = f'{"#" * header_size} <h{header_size} style="color:green">+{n}</h{header_size}>'
            # Handle everything else
            elif n.startswith('-'):
                n = f'<p style="color:red">{n.removesuffix('\n')}</p>\n'
            elif n.startswith('+'):
                n = f'<p style="color:green">{n.removesuffix('\n')}</p>\n'
            colored.append(n)


        #colored = [f'<span style="color:red">{x.removesuffix('\n')}</span>' for x in trimmed if x.startswith('-')]
        #colored = [f'<span style="color:green">{x}</span>' for x in trimmed if x.startswith('+')]
        
        parsed = colored
        file.close()

    with open(output_file_name, 'w+', encoding='utf8') as file:
        file.writelines(parsed)
        file.close()

    print('Done')