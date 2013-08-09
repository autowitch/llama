import re

class Vector(object):
    """docstring for Numeric"""
    def __init__(self, encoded):
        super(Vector, self).__init__()
        self.encoded = encoded

#        self.table = [
#            ([ 0,  0,  0,  0,  0,  0,  0,  0], 1),
#            ([ 1,  2,  1,  2,  1,  2,  1,  2], 2),
#            ([ 3,  4,  5,  3,  4,  5,  3,  4], 3),
#            ([ 6,  7,  8,  9,  6,  7,  8,  9], 4),
#            ([10, 11, 12, 13, 14, 10, 11, 12], 5),
#            ([15, 16, 17, 18, 19, 20, 15, 16], 6),
#            ([21, 22, 23, 24, 25, 26, 27, 21], 7),
#            ([28, 29, 30, 31, 32, 33, 34, 35], 8),
##            [36, 37, 38, 39, 40, 41, 42, 43, 44],
##            [45, 46, 47, 48, 49, 50, 51, 52, 53, 54],
##            [55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65],
#        ]
        self.table = [
            [ 0,  1,  2,  3,  4,  5],
            [ 6,  7,  8,  9, 10, 11],
            [12, 13, 14, 15, 16, 17],
            [18, 19, 20, 31, 22, 23],
            [24, 25, 26, 27, 28, 29],
            [30, 31, 32, 33, 34, 35],
        ]
        self.dir_table = {
            '7': (-1, -1),
            '8': ( 0, -1),
            '9': ( 1, -1),
            '4': (-1,  0),
            '5': ( 0,  0),
            '6': ( 1,  0),
            '1': (-1,  1),
            '2': ( 0,  1),
            '3': ( 1,  1)
        }
        self.x_size = len(self.table[0])
        self.y_size = len(self.table)
        self.base = 36

    @staticmethod
    def is_vector(s):
        return s.startswith('^')

    def decode(self, s=None):
        if not s:
            s = self.encoded

        if s.startswith('^'):
            s = s[1:]

        xpos = 0
        ypos = 0

        groups = []
        regex = '(?P<dir>[1-9])(?P<distance>[0-9.:])(?P<op>[X]?)[ ]*'
        while len(s) > 0:
            m = re.match(regex, s)
            if m:
                direction = m.group('dir')
                distance = m.group('distance')
                operation = m.group('op')

                x_offset = self.dir_table[direction][0] * int(distance)
                y_offset = self.dir_table[direction][1] * int(distance)
                ypos += y_offset
                xpos += x_offset
#                print "> %s %s %s" % (direction, distance, operation)
#                print "  %s %s" % (xpos, ypos)

                # Move the coord back into range
                while xpos >= self.x_size:
                    xpos -= self.x_size
                while ypos >= self.y_size:
                    ypos -= self.y_size
                while xpos < 0:
                    xpos += self.x_size
                while ypos < 0:
                    ypos += self.y_size

#                tri_len = ypos + 1 # (length of row on triangle)
#                                   # could also be from the tri tuple
#                while xpos >= tri_len:
#                    xpos -= tri_len
#                print "  %s %s" % (xpos, ypos)
#                print "  %s" % self.table[ypos][xpos]

                value = self.table[ypos][xpos]
                if operation != 'X':
                    groups.insert(0, value)

                s = s[m.end():]
            elif s:
                print "NOT A NUMBER!"
                break

        exp = 1
        total = 0
        for i in groups:
            total += exp * i
            exp *= self.base

        return total


    def elements(self, value=None):
        if not value:
            value = self.encoded

        if value.startswith('^'):
            value = value[1:]

        xpos = 0
        ypos = 0

        regex = '(?P<dir>[1-9])(?P<distance>[0-9.:])(?P<op>[X]?)[ ]*'
        while len(value) > 0:
            m = re.match(regex, value)
            if m:
                direction = m.group('dir')
                distance = m.group('distance')
                operation = m.group('op')

                x_offset = self.dir_table[direction][0] * int(distance)
                y_offset = self.dir_table[direction][1] * int(distance)
                ypos += y_offset
                xpos += x_offset

                # Move the coord back into range
                while xpos > self.x_size:
                    xpos -= self.x_size
                while ypos > self.y_size:
                    ypos -= self.y_size
                while xpos < 0:
                    xpos += self.x_size
                while ypos < 0:
                    ypos += self.y_pos

                tri_len = ypos + 1 # (length of row on triangle)
                                   # could also be from the tri tuple
                while xpos > tri_len:
                    xpos -= tri_len

                yield (direction, distance, operation)

                value = value[m.end():]
            elif s:
                print "NOT A NUMBER!"
                break

    def element_array(self, value=None):
        return [ x for x in self.elements(value=value) ]
