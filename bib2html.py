#!/usr/bin/env python3
import sys, os, re
from pybtex.database import parse_file
import codecs
import latexcodec
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('input_file')
ap.add_argument('--output-dir', '-O', default="bibfiles")
ap.add_argument('--output-file', '-o')
args = ap.parse_args()

if args.output_file:
    outfp = open(args.output_file, "w")
else:
    outfp = sys.stdout

db = parse_file(args.input_file)


entries = db.entries

def l2h(s):
    if s is None: return None
    return (codecs.decode(s, 'ulatex+utf8')
            .replace('{', '').replace('}', '')
            .encode('utf8', 'xmlcharrefreplace')
            .decode('utf8')
           )

print('<ul class="bibliography">', file=outfp)

for item in sorted(db.entries.items(), key=lambda x: int(x[1].fields.get('year')), reverse=True):

    key = item[0]
    e = item[1]
    year = e.fields.get('year')
    entrytype = e.type

    if e.persons.get('author', False):
        authors = e.persons['author']
        editors = e.persons.get('editor', None)
    else:
        authors = e.persons['editor']

    title = e.fields.get('title', None)
    title_h = l2h(title)

    url = e.fields.get('url', None)
    doi = e.fields.get('doi', None)
    note = e.fields.get('note', None)
    note_h =  l2h(note)

    journal = e.fields.get('journal', None)
    journal_h = l2h(journal)

    booktitle = e.fields.get('booktitle', None)
    booktitle_h = l2h(booktitle)

    school = e.fields.get('school', None)
    address = e.fields.get('address', None)
    publisher = e.fields.get('publisher', None)

    volume = e.fields.get('volume', None)
    issue = e.fields.get('issue', None)
    pages = e.fields.get('pages', None)
    if pages is not None:
        ppages = pages.replace('--', '&ndash;')

    pdf = args.output_dir + '/' + key + '.pdf'
    if not os.path.exists(pdf):
        print("W: {} does not exist".format(pdf), file=sys.stderr)
        pdf = None

    bibfile = args.output_dir + '/' + key + '.bib'

    author_list = ''
    for i, a in enumerate(authors):
        name = [] 
        name += a.first_names
        name += a.prelast_names
        name += a.last_names
        name = ' '.join(name)

        if i > 0 and i == len(authors) - 1:
            author_list+= ' and '
        elif i != 0:
            author_list+= ', '
        author_list += name


    author_list = bytes(author_list, 'utf-8').decode('latex+utf8')
    author_list = author_list.replace('{', '').replace('}', '')

    print('  <li class="bibentry bibentry-{}">'.format(entrytype),
            file=outfp)
    print('    <span class="bibentry-author">{}</span>'.format(author_list),
            file=outfp)
    print('    <span class="bibentry-year">({})</span>'.format(year),
            file=outfp)
    print('    <span class="bibentry-title">', file=outfp)

    if title_h[-1] not in '?.!':
        title_h = title_h + '.'

    if doi is not None:
        print('''      <a href="http://doi.org/{}">{}</a>
              '''.format(doi, title_h), file=outfp)
    elif url is not None:
        print('''      <a href="{}">{}</a>
              '''.format(url, title_h), file=outfp)
    elif pdf is not None:
        print('''      <a href="{}">{}</a>
              '''.format(pdf, title_h), file=outfp)
    else:
        print('''        {}
              '''.format(title_h), file=outfp)
    print('      </span>', file=outfp)

    if journal is not None:
        print('''    <span class="bibentry-journaltitle">{},
               </span>'''.format(journal_h), file=outfp)
    elif booktitle is not None:
        print('''    <span class="bibentry-booktitle">In: {},
                   </span>'''.format(booktitle_h), file=outfp)
    elif e.type == 'phdthesis':
        print(''''    <span class="bibentry-thesis-type">PhD thesis, {}
                    </span>'''.format(school), file=outfp)
    elif e.type == 'mastersthesis':
        print('''    <span class="bibentry-thesis-type">Master\'s thesis, {}
                   </span>'''.format(school), file=outfp)

    if volume is not None:
        if issue is not None:
            if pages is not None:
                print('''    <span class="bibentry-issue">{}({}):{}
                        </span>'''.format(volume, issue, ppages), file=outfp)
            else:
                print('''    <span class="bibentry-issue">{}({})
                           </span>'''.format(volume, issue), file=outfp)
        else:
            if pages is not None:
                print('''    <span class="bibentry-volume">{}:{}
                        </span>'''.format(volume, ppages), file=outfp)
            else:
                print('''    <span class="bibentry-volume">{}
                        </span>'''.format(volume), file=outfp)
    elif issue is not None:
        if pages is not None:
            print('''    <span class="bibentry-issue">{}:{}
                    </span>'''.format(issue, ppages), file=outfp)
        else:
            print('''    <span class="bibentry-issue">{}
                    </span>'''.format(issue), file=outfp)
    elif pages is not None:
        print('''    <span class="bibentry-pages"> pages {}
                </span>'''.format(ppages), file=outfp)

    if note is not None:
        print('''    <span class="bibentry-note">{}
                </span>'''.format(note_h), file=outfp)

    if pdf is not None:
        print('''    <span class="bibentry-file"><a href="{}">[pdf]</a>
                   </span>'''.format(pdf), file=outfp)
    print('''    <span class="bibentry-bib">
                <a class="bibentry-bib" href="{}">[bib]</a>
               </span>'''.format(bibfile), file=outfp)
    print("  </li>", file=outfp)

    with open(bibfile, 'w') as fp:
        print("@{}{{{},".format(e.type, key), file=fp)
        author_list = ''
        for i, a in enumerate(authors):
            name = ' '.join(a.prelast_names) + ' ' + \
                   ' '.join(a.last_names) + ', ' +  ' '.join(a.first_names)
            author_list += name
            if i != len(authors) - 1:
                author_list += ' and '
        print(" author  = {{{}}},".format(author_list.strip()), file=fp)
        print(" year  = {{{}}},".format(year), file=fp)
        print(" title  = {{{}}},".format(title), file=fp)
        if journal is not None:
            print(" journal  = {{{}}},".format(journal), file=fp)
        if booktitle is not None:
            print(" booktitle  = {{{}}},".format(booktitle), file=fp)
        if volume is not None:
            print(" volume  = {{{}}},".format(volume), file=fp)
        if issue is not None:
            print(" issue  = {{{}}},".format(issue), file=fp)
        if pages is not None:
            print(" pages  = {{{}}},".format(pages), file=fp)
        if editors is not None:
            editor_list = ''
            for i, a in enumerate(editors):
                name = ' '.join(a.prelast_names) + ' ' + \
                       ' '.join(a.last_names) + ', ' +  ' '.join(a.first_names)
                editor_list += name
                if i != len(editors) - 1:
                    editor_list += ' and '
            print(" editor  = {{{}}},".format(editor_list.strip()), file=fp)
        if address is not None:
            print(" address  = {{{}}},".format(address), file=fp)
        if url  is not None:
            print(" url  = {{{}}},".format(url), file=fp)
        if doi is not None:
            print(" doi  = {{{}}},".format(doi), file=fp)
        print("}", file=fp)

print('</ul>', file=outfp)

# for key in entries:
#     e = entries[key]
# #    print("{}:{}".format(key, e.type))
# 
# 
#     year = e.fields.get('year')
#     title = e.fields.get('title')
# 
# 
# 
# 
#     print()

outfp.close()
