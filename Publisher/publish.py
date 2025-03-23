# Publisher for markdown-based interactive media
import markdown
import argparse
import zipfile
import os

def compress(directory_path: str, output_path: str = None):
    if output_path == None:
        output_path = f'{os.path.dirname(os.path.normpath(directory_path))}\\Published.zip'
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, directory_path))
        zipf.close()

def html_prologue(title: str):
    return f'''
<html>
    <head>
        <link rel="stylesheet" href="../style.css">
        <link rel="stylesheet" href="https://unpkg.com/simpledotcss/simple.min.css">
        <title>{title}</title>
    </head>
    <body>
        <div>
'''

def html_epilogue(previous: str = None, next: str = None):
    previous_link = f'<a href="{previous}.html">{previous}</a>' if previous != '' else ''
    next_link = f'<a href="{next}.html">{next}</a>' if next != '' else ''
    ret = '\t\t</div>'
    if previous != None or next != None:
        ret += f'''\t\t<div>
            <table id="links">
                <tr>
                    <td class="previous">
                        {previous_link}
                    </td>
                    <td class="toc"><a href="../index.html">Table of Contents</a></td>
                    <td class="next">
                        {next_link}
                    </td>
                </tr>
            </table>
        </div>
    </body>
</html>
'''
    return ret

def html_index(ordered_sources: list):
    ret = '''\t\t\t<p>This is the welcome page for viewing the story I am writing. It contains a table of contents for quick navigation. At the end of each chapter are links to the previous and next chapters (where applicable). Chapters are presented in the order they should be read in.</p>
        </div>
        <div>
'''
    for source in ordered_sources:
        ret += f'\t\t\t<p><a href="./Chapters/{source}.html">{source}</a></p>\n'
    return ret

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
    width: 33% !important;
    text-align: start !important;
}
td.toc {
    width: 33% !important;
    text-align: center !important;
}
td.next {
    width: 33% !important;
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
    parser.add_argument('-z', '--zip', help='Output files to a ZIP archive', action='store_true')

    args = parser.parse_args()
    path_to_sources = ''
    order_path = ''
    output_path = ''
    zip = False
    if args.file:
        path_to_sources = args.file
    if args.directory:
        path_to_sources = args.directory
        order_path = f'{path_to_sources}\\order.txt'
    if args.output:
        output_path = f'{args.output}\\'
    if args.zip:
        zip = True

    # Get ordered sources
    ordered_sources = {}
    with open(order_path, 'r', encoding='utf8') as file:
        contents = file.readlines()
        ordered_sources = {x.strip(): f'{path_to_sources}\\{x.strip()}.md' for x in contents}
        file.close()

    # Create index
    with open(f'{output_path}index.html', 'w', encoding='utf8') as file:
        file.write(html_prologue('Welcome'))
        file.write(html_index(ordered_sources))
        file.write(html_epilogue())
        file.close()

    # Write stylesheet
    with open(f'{output_path}style.css', 'w') as file:
        file.write(CSS)
        file.close()
    
    # Modify output_path to store chapters in deeper directory
    chapters_path = os.path.join(output_path, 'Chapters\\')
    
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
        with open(f'{chapters_path}{title}.html', 'w', encoding='utf8') as file:
            file.write(html_prologue(title))
            file.write(html)
            file.write(html_epilogue(previous, next))
            file.close()
    
    # Compress if requested
    if zip:
        compress(output_path)