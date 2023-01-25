#-*- coding: UTF-8 -*-
import sys, os
import argparse
from ebooklib import epub

import txtparse
import htmlgen

# todo: --cover figure
# todo: add mobi output
# todo: encoding detection

def dump_epub_section_chapter(book, sections):
    pass

def dump_epub_chapter(book, chapters):
    pass


def get_file_name(filenames, sid, cid, title):
    id = (sid, cid, title)
    if cid is None:
        # section name
        fn = 'section_%d.xhtml' % sid
    else:
        # chapter name
        fn = 'chapter_%d.%d.xhtml' % (sid, cid)
    # for duplicated id: add a suffix
    i = 1
    while fn in filenames:
        i += 1
        if cid is None:
            fn = 'section_%d-%d.xhtml' % (sid, i)
        else:
            fn = 'chapter_%d.%d-%d.xhtml' % (sid, cid, i)
    filenames.append(fn)
    return fn

STYLE_FILE_NAME="style/book.css"

def main(args):
    # process the input txt file
    input = args.input if args.input.endswith('.txt') else args.input + '.txt'
    try:
        with open(input, 'r', encoding=args.encoding) as f:
            content = f.read()
            pf_data, data = txtparse.process_book(
                content, args.section_name, args.section_length, args.chapter_name, args.chapter_length)
            pf_data = txtparse.process_preface(pf_data, args.title, args.author)
    except Exception as e:
        raise e
    num_chapters = [len(x[3]) for x in data]
    total_chapters = sum(num_chapters)
    print('Loaded %d sections and %d chapters: %s.' % (len(data), total_chapters, num_chapters))
    
    # prepare the output file
    output = args.output if args.output.endswith('.epub') else args.output + '.epub'
    try:
        if os.path.exists(output):
            os.remove(output)
    except:
        raise Exception("Cannot write to file: %s" % output)
    
    # create an empty EPUB file
    book = epub.EpubBook()

    # set the metadata
    book.set_identifier((args.author+args.title).replace(' ', ''))
    book.set_title(args.title)
    book.set_language(args.language)
    
    book.add_author(args.author)

    if len(pf_data) > 0:
        preface = epub.EpubHtml(title='前言', file_name='preface.xhtml', lang=args.language)
        preface.content = htmlgen.preface_to_html(pf_data, args.title, args.author)
        preface.add_link(href=STYLE_FILE_NAME, rel='stylesheet', type='text/css')
        book.add_item(preface)
    else:
        preface = None

    sections = []

    file_names = []
    n = 0
    # create the sections
    for sid, section in enumerate(data):
        s_num, meta, content, chapters = section
        title = htmlgen.make_section_head(meta[0], meta[1])
        fn = get_file_name(file_names, s_num, None, title)
        section = epub.EpubHtml(title=title, file_name=fn, lang=args.language)
        section.set_content(htmlgen.section_to_html(meta[0], meta[1], content))
        section.add_link(href=STYLE_FILE_NAME, rel='stylesheet', type='text/css')
        book.add_item(section)
        # create the chapters
        cs = []
        for cid, chapter in enumerate(chapters):
            c_num, meta, content = chapter
            title = htmlgen.make_chapter_head(meta[0], meta[1])
            fn = get_file_name(file_names, s_num, c_num, title)
            chapter = epub.EpubHtml(title=title, file_name=fn, lang=args.language)
            chapter.set_content(htmlgen.chapter_to_html(meta[0], meta[1], content))
            chapter.add_link(href=STYLE_FILE_NAME, rel='stylesheet', type='text/css')
            book.add_item(chapter)
            cs.append(chapter)
        n += len(cs)
        print('Progress: %d%% chapters. Finished section %d with %d chapters.' % (n/total_chapters*100 , s_num, len(cs)))
        sections.append((section, cs))
        
    # create the Table of Contents and spine
    print('Organizing chapters into the book.')
    toc = []
    spine = []
    if preface is not None:
        spine.append(preface)
        toc.append(epub.Link(preface.file_name, preface.title, preface.title.removesuffix('.xhtml')))
    toc.append(epub.Link('nav.xhtml', '目录', 'nav'))
    spine.append('nav')
    for section, chapters in sections:
        toc.append((epub.Section(section.title, section.file_name), chapters))
        spine.append(section)
        spine.extend(chapters)
    book.toc = toc
    book.spine = spine

    # add the table of contents and navigation to the book
    if args.write_toc:
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

    # add styles
    print('Generating style sheet.')
    style = '''
body { font-family: 宋体; }
p {text-indent:2em; margin:0.5em 0em;}
h1 {text-align: center; font-size: 1.6em;}
h2 {text-align: center; font-size: 1.3em; margin: 1em 0;}
div#book-title {text-align: center; vertical-align: middle;}
div#book-title p.title {font-size: 2.0em; text-indent:0em; margin: 1em 0;}
div#book-title p.author {font-size: 1.5em; text-indent:0em; margin: 1em 0;}
'''
    nav_css = epub.EpubItem(uid="style_book", file_name=STYLE_FILE_NAME, media_type="text/css", content=style)
    book.add_item(nav_css)
    
    # write the EPUB file
    print('Writing epub file to %s.' % output)
    epub.write_epub(output, book, {"pages_title": "页"})
    print('Done.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert txt files to epub')
    parser.add_argument('input', help='the input txt file to convert')
    parser.add_argument('output', help='the output epub file to create')
    parser.add_argument('-e', '--encoding', help='encoding of the input file. example: gbk, utf-8, utf-16. (default: utf-8)', default='utf-8')
    parser.add_argument('-t', '--title', help='title of the book')
    parser.add_argument('-a', '--author', help='author of the book')
    parser.add_argument('-l', '--language', help='language of the book (default: zh-cn)', default='zh-cn')
    parser.add_argument('-2', '--has_sections', action='store_true', help='whether the book has both sections and chapters', default=True)
    parser.add_argument('-s', '--section_name', help='name of the section (default: 卷)', default='卷')
    parser.add_argument('-n', '--section_length', help='maximum length of the section title', type=int, default=14)
    parser.add_argument('-c', '--chapter_name', help='name of the chapter (default: 章)', default='章')
    parser.add_argument('-m', '--chapter_length', help='maximum length of the chapter title', type=int, default=20)
    parser.add_argument('-w', '--write_toc', action='store_true', help='whether to write the table of contents in the book', default=True)
    
    args = parser.parse_args(sys.argv[1:])
    # args = parser.parse_args('input.txt mybook.epub -t 绍宋 -a 榴弹怕水'.split())
    # args = parser.parse_args('e:/Backup/Book/小说/七月新番《秦吏》.txt 七月新番《秦吏》.epub -t 秦吏 -a 七月新番 -e utf16'.split(' '))
    #print(args)
    main(args)
    