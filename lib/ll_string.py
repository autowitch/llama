import re


class String(object):

    """docstring for String"""

    def __init__(self, encoded=''):
        super(String, self).__init__()

        # Letter Frequency Chart
        # Single Letters:  ETAONRISHDLFCMUGYPWBVKXJQZ
        # Pairs:           TH HE AN RE ER IN ON AT ND ST ES EN OF TE ED OR TI HI AS TO
        # Doubled Letters: LL EE SS OO TT FF RR NN PP CC

        #    \t \r qu sh ch sp ;  :  '  "  SHFT
        #    |  cc 2  3  9  4  0  6  5  1  8  
        #    \  pp J  Q  Z  th he an re er 7
        #    /  nn X  z  E  T  A  O  N  in !
        #    ?  rr K  d  l  f  c  m  R  on @
        #    ,  ff V  q  t  a  o  u  I  at #
        #    .  tt B  j  h  e  n  g  S  nd $
        #    <  oo W  x  s  i  r  y  H  st %
        #    >  ss P  k  b  b  w  p  D  es ^
        #    `  ee Y  G  U  M  C  F  L  en &
        #    ~  ll to as hi ti or ed te of *
        #    \n (  )  -  _  =  +  [  ]  {  }

        self.char_chart = [
            ('\t', '\r', 'qu', 'sh', 'ch', ' ',  ';',  ':',  "'",  '"',  'SHFT'),
            ('|',  'cc', '2',  '3',  '9',  '4',  '0',  '6',  '5',  '1',  '8'),
            ('\\', 'pp', 'J',  'Q',  'Z',  'th', 'he', 'an', 're', 'er', '7'),
            ('/',  'nn', 'X',  'z',  'E',  'T',  'A',  'O',  'N',  'in', '!'),
            ('?',  'rr', 'K',  'd',  'l',  'f',  'c',  'm',  'R',  'on', '@'),
            (',',  'ff', 'V',  'q',  't',  'a',  'o',  'u',  'I',  'at', '#'),
            ('.',  'tt', 'B',  'j',  'h',  'e',  'n',  'g',  'S',  'nd', '$'),
            ('<',  'oo', 'W',  'x',  's',  'i',  'r',  'y',  'H',  'st', '%'),
            ('>',  'ss', 'P',  'k',  'ly', 'b',  'w',  'p',  'D',  'es', '^'),
            ('`',  'ee', 'Y',  'G',  'U',  'M',  'C',  'F',  'L',  'en', '&'),
            ('~',  'll', 'to', 'as', 'hi', 'ti', 'or', 'ed', 'te', 'of', '*'),
            ('\n', '(',  ')',  '-',  '_',  '=',  '+',  '[',  ']',  '{',  '}')
        ]
        self.str_grid_size_x = 11
        self.str_grid_size_y = 12

        self.base_12_re = "[-+]?[0-9.:]+"
        self.base_5_offset_re_grouped = "(?P<sign>[-])?(?P<digit>[.:|+*])"
        self.base_5_offset_re = "[-]?[.:|+*]"
        self.base_5_nums = '.:|+*'


        self.encoded = ''
        self.decoded = ''
        if encoded:
            self.encoded = encoded
            self.decoded = self.decode(encoded)

    @staticmethod
    def is_string(s):
        return s.startswith('$')

    def extract_string_digit(self, d):
        sign = 1
        offset = 0
        if d[0] == '-':
            sign = -1
            offset = 1
        value = self.base_5_nums.find(d[offset])
        return sign * value

    def decode(self, s=None):
        if not s:
            s = self.encoded

        x_pos = 5
        y_pos = 6
        found_str = []
        if s.startswith('$'):
            s = s[1:]

        parts = s.split(' ')
        num_pair_re = '(?P<y>%s)(?P<x>%s)(?P<op>[X?])?' % (self.base_5_offset_re, self.base_5_offset_re)
        # Operation:
        #   X - skip this char
        #   ? - only include char ... something importance...
        for p in parts:
            m = re.match(num_pair_re, p)
            if m:
                x = m.group('x')
                y = m.group('y')
                x = self.extract_string_digit(x)
                y = self.extract_string_digit(y)
                x_pos += x
                y_pos += y
                if  m.group('op') != 'X':
                    ch = self.char_chart[y_pos][x_pos]
                    found_str.append(ch)
            else:
                raise InvalidStringVector('%s is not a string vector offset' % p)
        return ''.join(found_str)


    def elements(self, value=None):

        if not value:
            values = self.encoded

        if value.startswith('$'):
            value = value[1:]

        parts = value.split(' ')
        num_pair_re = '(?P<y>%s)(?P<x>%s)(?P<op>[X?])?' % (self.base_5_offset_re, self.base_5_offset_re)
        # Operation:
        #   X - skip this char
        #   ? - only include char ... something importance...
        for p in parts:
            m = re.match(num_pair_re, p)
            if m:
                x = m.group('x')
                y = m.group('y')
                op = m.group('op')
                yield (p, x, y, op)

    def element_array(self, value=None):
        return [ x for x in self.elements(value=value) ]
