import re

class Boolean(object):
    """docstring for Boolean"""
    def __init__(self, encoded, classic=False):
        super(Boolean, self).__init__()
        self.encoded = encoded
        self.classic = classic

    @staticmethod
    def is_boolean(s):
        if re.match('\?[<>^]+$', s):
            return True
        return False

    def decode(self, value=None):
        if not value:
            value = self.encoded

        if value.startswith('?'):
            value = value[1:]

        possibilities = {'<':'FALSE',
                         '>':'TRUE',
                         '^':'OTHER'}
        if self.classic:
            possibilities['^'] = 'FILE_NOT_FOUND'
        return ' '.join([possibilities[x] for x in value])

    def elements(self, value=None):
        if not value:
            value = self.encoded

        if value.startswith('?'):
            value = value[1:]

        for x in value:
            yield x

    def element_array(self, value=None):
        return [ x for x in self.elements(value=value) ]

