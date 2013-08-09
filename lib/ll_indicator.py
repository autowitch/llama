import re

class Indicator(object):

    """docstring for Indicator"""
    indicator_re = '!(?P<eighteens>[1-9A-H])(?P<ones>[1-9A-H])'
    indicator_rhi_re = '!(?P<one>[1-9A-H]{2})(?P<two>[1-9A-H]{2}(?P<three>[1-9A-H]{2}))'

    def __init__(self, value=None):
        super(Indicator, self).__init__()

        self.encoded = Value

    @staticmethod
    def is_indicator(value):
        if re.match(Indicator.indicator_re, value):
            return True
        return False

    def decode_digit(self, value):
        if value >= 1 and value <= 9:
            return int(value)
        else:
            return ord(value) - ord('A') + 10

    def decode_single_indicator(self, value):
        val1 = self.decode_digit(value[0])
        val2 = self.decode_digit(value[1])

        return 18 * val1 + val2

    def decode(self, value=None):
        if not value:
            value = self.encoded

        if value.startswith('!'):
            value = value[1:]
        val_1 = decode_single_indicator(self, value)
        if len(value) == 2:
            return val_1
        elif len(value) == 6:
            val_2 = decode_single_indicator(self, value[2:])
            val_3 = decode_single_indicator(self, value[4:])
            return val_1, val_2, val_3
        else:
            raise Exception("Invalid indicator: %s" % value)

    def encode(self, value):
        pass

