#-*- coding: UTF-8 -*-
import re
import util


#% -------- number checking function --------

def check_number_increasing(numbers):
    '''
    Check if the list of numbers is increasing.
    '''
    wrong = []
    for i in range(1, len(numbers)):
        if numbers[i] <= numbers[i-1]:
            wrong.append(numbers[i])
    return wrong

def check_number_list(numbers):
    '''
    Check if the list of numbers is continuous.
    Return the list of numbers which are missing.
    '''
    missing = []
    for i in range(1, len(numbers)):
        if numbers[i] - numbers[i-1] != 1:
            for j in range(numbers[i-1]+1, numbers[i]):
                missing.append(j)
    return missing

#% -------- seperate sections and chapters --------

def __separate_basic(s, pattern, title):
    matches = [m for m in re.finditer(pattern, s, re.MULTILINE)]
    if len(matches) == 0:
        return []
    numbers = []
    fail = []
    for match in matches:
        n = util.parse_number(match[1])
        if n is None:
            fail.append(match[0])
        numbers.append(n)
    if len(fail) > 0:
        raise Exception("%s number is not valid number. Wrong: %s" % (title, fail))
    wrong = check_number_increasing(numbers)
    if len(wrong) > 0:
        raise Exception("%s number is not increasing. Wrong: %s" % (title, wrong))
    missing = check_number_list(numbers)
    if len(missing) > 0:
        raise Exception("%s number is not continuous. Missing: %s" % (title, missing))
    content = util.trim_text(s[0: matches[0].start()])
    res = [(-1, '', content)]
    for i in range(len(matches)):
        endpos = matches[i+1].start() if i < len(matches)-1 else len(s)
        content = s[matches[i].end()+1: endpos]
        content = util.trim_text(content)
        res.append((numbers[i], matches[i].groups(), content))
    return res


def make_pattern(title, length=20):
    return r"^第([零一二三四五六七八九十白千\d]*?)%s(?:[ \t　]+([\S 　]{1,%d}))?$" % (title, length)


def separate_sections(s, pattern=None):
    '''
    Separate text into sections.
    '''
    if pattern is None:
        pattern = make_pattern('卷', 14)
    return __separate_basic(s, pattern, 'Section')


def separate_chapters(s, pattern=None):
    '''
    Separate text into chapters.
    '''
    if pattern is None:
        pattern = make_pattern('章', 20)
    return __separate_basic(s, pattern, 'Chapter')


#% -------- seperate sections and chapters --------

def process_preface(content, title, author):
    lines = content.splitlines()
    to_remove = []
    for i, line in enumerate(lines):
        if line == title or re.match(r'^《%s》$'%title, line):
            to_remove.append(i)
        elif line == author or re.match(r'^(作者[:： \t])?%s$'%author, line):
            to_remove.append(i)
    if len(to_remove) > 0:
        res = '\n'.join([l for i, l in enumerate(lines) if i not in to_remove])
        if res[0] == '\n':
            res = util.trim_text(res)
        return res
    else:
        return content

def process_book(text, sec_name, sec_length, chp_name, chp_length):
    sec_pattern = make_pattern(sec_name, sec_length)
    chp_pattern = make_pattern(chp_name, chp_length)
    
    sections = separate_sections(text, sec_pattern)
    preface = sections[0][2]
    data = []
    for sec in sections[1:]:
        chapters = separate_chapters(sec[2], chp_pattern)
        content = chapters[0][2]
        s = (sec[0], sec[1], content, chapters[1:])
        data.append(s)
    return preface, data
        
