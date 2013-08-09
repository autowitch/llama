import re

class Numeric(object):
    """docstring for Numeric"""
    def __init__(self, encoded):
        super(Numeric, self).__init__()
        self.encoded = encoded

    @staticmethod
    def is_numeric(s):
        return s.startswith('#')

    def extract_single_digit(self, d):
        regex = '(?P<twelves>[A-E]?)(?P<ones>[0-9.:])'
        m = re.match(regex, d)
        twelves = m.group('twelves')
        if not twelves:
            twelves = 0
        else:
            twelves = ord(twelves) - ord('A') + 1
        ones = m.group('ones')
        if ones == '.':
            ones = 10
        elif ones == ':':
            ones = 11
        else:
            ones = int(ones)

        return 12 * twelves + ones

    def decode(self, s=None):
        if not s:
            s = self.encoded

        if s.startswith('#'):
            s = s[1:]

        groups = []
        regex = '(?P<digit>[A-E]?[0-9.:])'
        while len(s) > 0:
            m = re.match(regex, s)
            if m:
                digit = m.group('digit')
                groups.insert(0, digit)
                s = s[m.end():]
            elif s:
                print "NOT A NUMBER!"
                break

        print groups

        offset = 1
        total = 0
        for x in groups:
            value = self.extract_single_digit(x)
            print ">>> %s" % value
            total += offset * value
            offset *= 60

        return total


    def elements(self, value=None):
        if not value:
            value = self.encoded

        if s.startswith('#'):
            value = value[1:]

        regex = '(?P<digit>(?P<twelves>[A-E]?)(?P<ones>[0-9.:]))'
        while len(s) > 0:
            m = re.match(regex, value)
            if m:
                digit = m.group('digit')
                twelves = m.group('twelves')
                ones = m.group('ones')
                value = value[m.end():]
                yield (digit, twelves, ones)

    def element_array(self, value=None):
        return [ x for x in self.elements(value=value) ]
