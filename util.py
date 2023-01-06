import re


#% -------- remove prefix and suffix spaces --------

def trim_text(text):
    text = re.sub(r'(^\s+)|(\s+$)', '', text)
    return text


#% -------- parse number --------

chinese_number_table ={
    '零':0, '一':1, '二':2, '两':2, '三':3, '四':4, '五':5, '六':6, '七':7, '八':8, '九':9,
    '十':10, '百':100, '千':1000, '万':10000, '亿':100000000}


def parse_chinese_number(s):
    '''
    Translate Chinese number to Arabic number.
    '''
    result = 0
    part = 0
    f_part = 1
    f_digit = 1
    for c in s[::-1]:
        if c in chinese_number_table:
            if c == '万' or c == '亿':
                result += part * f_part
                part = 0
                f_digit = 1
                if f_part >= chinese_number_table['亿']:
                    # 万亿, 亿亿
                    f_part *= chinese_number_table[c]
                else:
                    # 万, 亿
                    f_part = chinese_number_table[c]
            elif c == '十' or c == '百' or c == '千':
                f_digit = chinese_number_table[c]
            else:
                part += chinese_number_table[c] * f_digit
        else:
            return None
    if s[0] == '十':
        # 十, 十二, 十万
        part += 10
    result += part * f_part
    return result


def __test_parse_chinese_number():
    def check(chinese_number, arabic_number):
        convert = parse_chinese_number(chinese_number)
        print(convert , arabic_number, convert == arabic_number)
    
    check('零', 0)
    check('五', 5)
    check('十', 10)
    check('十二', 12)
    check('二十三', 23)
    check('一百零一', 101)
    check('九百二十一', 921)
    check('五十六万零一十', 560010)
    check('一万亿零二千一百零一', 1000000002101)
    check('一万亿二千一百万零一百零一', 1000021000101)
    check('一万零二百三十亿四千万零七千八百九十', 1023040007890)

#__test_parse_chinese_number()

def parse_number(s):
    if re.match(r'^\d+$', s):
        return int(s)
    else:
        return parse_chinese_number(s)
