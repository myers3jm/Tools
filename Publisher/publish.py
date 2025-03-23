# Publisher for markdown-based interactive media
import sys
import markdown
import argparse

def html_prologue(title):
    return f'''
<html>
    <head>
        <link rel="stylesheet" href="style.css">
        <link rel="stylesheet" href="https://unpkg.com/simpledotcss/simple.min.css">
        <title>{title}</title>
    </head>
    <body>
        <div>
'''

def html_epilogue(previous, next):
    previous_link = f'<a href="{previous}.html">{previous}</a>' if previous != '' else ''
    next_link = f'<a href="{next}.html">{next}</a>' if next != '' else ''
    return f'''
        </div>
        <div>
            <table id="links">
                <tr>
                    <td class="previous">
                        {previous_link}
                    </td>
                    <td class="next">
                        {next_link}
                    </td>
                </tr>
            </table>
        </div>
    </body>
</html>
'''

CSS = '''
p {
    text-indent: 48 !important;
    margin-top: 24 !important;
    margin-bottom: 24 !important;
}
div {
    margin-top: 36 !important;
    margin-bottom: 36 !important;
}
table#links {
    width: 100%;
}
td {
    border: 0px !important;
}
td.previous {
    text-align: start !important;
}
td.next {
    text-align: end !important;
}
'''

if __name__ == '__main__':
    # Set up argument parser
    parser = argparse.ArgumentParser(
        prog='publish',
        description='Publish Markdown files to HTML with styling consistent with that of a novel'
    )
    source_args = parser.add_mutually_exclusive_group(required=True)
    source_args.add_argument('-f', '--file', help='Specify a single markdown source')
    source_args.add_argument('-d', '--directory', help='Specify a directory containing order.txt and multiple markdown sources')
    parser.add_argument('-o', '--output', help='Specify the output directory for the generated HTML pages', required=True)

    args = parser.parse_args()
    path_to_sources = ''
    order_path = ''
    output_path = ''
    if args.__contains__('file'):
        path_to_sources = args.file
    if args.__contains__('directory'):
        path_to_sources = args.directory
        order_path = f'{path_to_sources}\\order.txt'
    if args.__contains__('output'):
        output_path = f'{args.output}\\'

    print(f'{path_to_sources}\t{order_path}\t{output_path}')

    # Get ordered sources
    ordered_sources = {}
    with open(order_path, 'r', encoding='utf8') as file:
        contents = file.readlines()
        ordered_sources = {x.strip(): f'{path_to_sources}\\{x.strip()}.md' for x in contents}
        file.close()
    
    # Act on each source file
    for title, source in ordered_sources.items():
        html = ''
        # Get source content
        with open(source, 'r', encoding='utf8') as file:
            html = str.join('\n', [f'\t\t\t{x}' for x in markdown.markdown(file.read().replace('---', 'SCENE_BREAK')).split('\n')])
            html = html.replace('\t<p>SCENE_BREAK</p>', '</div>\n\t\t<div>')
            file.close()
        # Add links
        titles = list(ordered_sources.keys())
        current_index = titles.index(title)
        previous = titles[current_index - 1] if current_index != 0 else ''
        next = titles[current_index + 1] if current_index != len(titles) - 1 else ''

        # Write html file
        with open(f'{output_path}{title}.html', 'w', encoding='utf8') as file:
            file.write(html_prologue(title))
            file.write(html)
            file.write(html_epilogue(previous, next))
            file.close()
    
    # Write stylesheet
    with open(f'{output_path}style.css', 'w') as file:
        file.write(CSS)
        file.close()