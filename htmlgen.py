#-*- coding: UTF-8 -*-
import util

def text_to_html(content, tag='p', class_name=None):
    '''
    Trun text paragraphs content into html.
    '''
    template = '<%s%s>%s</%s>' % (tag, ' class="%s"' % class_name if class_name is not None else '', '%s', tag)
    paragraphs = [c for c in content.split('\n') if c]
    res = '\n'.join([template % util.trim_text(p) for p in paragraphs])
    return res

# preface

def preface_to_html(content, title, author):
    '''
    Trun preface content into html.
    '''
    res = '<div id="book-title">\n'
    res += '<p class="title">%s</p>\n' % title
    res += '<p class="author">%s</p>\n' % author
    res += '</div>\n'
    paragraphs = [c for c in content.split('\n') if c]
    res += '\n'.join(['<p>%s</p>' % p for p in paragraphs])
    return res

# section

def make_section_head(num, title):
    return '第%s卷 %s' % (num, title) if title is not None else '第%s卷' % num

def section_to_html(num, title, content):
    '''
    Trun section content into html.
    '''
    paragraphs = [c for c in content.split('\n') if c]
    head = '<h1>' + make_section_head(num, title) + '</h1>'
    res = head + '\n' + '\n'.join(['<p>%s</p>' % p for p in paragraphs])
    return res

# chapter

def make_chapter_head(num, title):
    return '第%s章 %s' % (num, title) if title is not None else '第%s章' % num

def chapter_to_html(num, title, content):
    '''
    Trun chapter content into html.
    '''
    paragraphs = [c for c in content.split('\n')]
    head = '<h2>' + make_chapter_head(num, title) + '</h2>'
    res = head + '\n' + '\n'.join(['<p>%s</p>' % p for p in paragraphs])
    return res
