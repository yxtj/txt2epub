from ebooklib import epub

# create an empty EPUB file
book = epub.EpubBook()

# set the metadata
book.set_identifier('id123456')
book.set_title('My Great Ebook')
book.set_language('en')

# create the sections
section1 = epub.EpubHtml(title='Section 1', file_name='section_1.xhtml')
section2 = epub.EpubHtml(title='Section 2', file_name='section_2.xhtml')

# create the chapters
chapter1_1 = epub.EpubHtml(title='Chapter 1.1', file_name='chap_1.1.xhtml')
chapter1_2 = epub.EpubHtml(title='Chapter 1.2', file_name='chap_1.2.xhtml')
chapter2_1 = epub.EpubHtml(title='Chapter 2.1', file_name='chap_2.1.xhtml')
chapter2_2 = epub.EpubHtml(title='Chapter 2.2', file_name='chap_2.2.xhtml')

# set the content of the chapters and sections
section1.content = '<h1>Section 1</h1>' #+ chapter1_1.content + chapter1_2.content
section2.content = '<h1>Section 2</h1>' #+ chapter2_1.content + chapter2_2.content
chapter1_1.content = '<h2>Chapter 1.1</h2><p>Some text</p>'
chapter1_2.set_content('<h2>Chapter 1.2</h2><p>Some text</p>')
chapter2_1.content = '<h2>Chapter 2.1</h2><p>Some text</p>'
chapter2_2.content = '<h2>Chapter 2.2</h2><p>Some text</p>'

# add the chapters and sections to the book
book.add_item(section1)
book.add_item(section2)
book.add_item(chapter1_1)
book.add_item(chapter1_2)
book.add_item(chapter2_1)
book.add_item(chapter2_2)

# create the Table of Contents
book.toc = ((epub.Section('Section 1', 'section_1.xhtml'), (chapter1_1, chapter1_2)),
            (epub.Section('Section 2', 'section_2.xhtml'), (chapter2_1, chapter2_2)),
            )

# book.toc = (epub.Link('section_1.xhtml', 'Section 1', 'section_1.xhtml'),
#             epub.Link('chap_1.1.xhtml', 'Chapter 1.1', 'chap_1.1.xhtml'),
#             epub.Link('chap_1.2.xhtml', 'Chapter 1.2', 'chap_1.2.xhtml'),
#             epub.Link('section_2.xhtml', 'Section 2', 'section_2.xhtml'),
#             epub.Link('chap_2.1.xhtml', 'Chapter 2.1', 'chap_2.1.xhtml'),
#             epub.Link('chap_2.2.xhtml', 'Chapter 2.2', 'chap_2.2.xhtml'),
#             )


# add the table of contents and navigation to the book
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

# add the Table of Contents to the spine
book.spine = ['nav', section1, chapter1_1, chapter1_2, section2, chapter2_1, chapter2_2]


# write the EPUB file
epub.write_epub('mybook.epub', book, {"pages_title": "页"})

