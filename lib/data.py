from lib.ll_string import String
from lib.ll_numeric import Numeric
from lib.ll_boolean import Boolean
from lib.ll_method import Method
from lib.ll_class import Class
from lib.ll_indicator import Indicator
from lib.ll_vector import Vector
# from lib.ll_float import Float
# from lib.ll_date import Date


class Data(object):

    """docstring for Data"""

    def __init__(self, threads):
        super(Data, self).__init__()

        self.threads = threads

        self.assign_matrix = {
#            ('str','str'):(self.assign_str_str,False),
#            ('str','int'):(self.assign_str_int,False),
#            ('str','bool'):(self.assign_str_bool,False),
#
#            ('int','str'):(self.assign_str_int,True),
#            ('int','int'):(self.assign_int_int,False),
#            ('int','bool'):(self.assign_int_bool,False),
#
#            ('bool','str'):(self.assign_str_bool,True),
#            ('bool','int'):(self.assign_int_bool,True),
#            ('bool','bool'):(self.assign_bool_bool,False),
        }

        self.addition_matrix = {
            ('str','str'):(self.add_str_str,False),
            ('str','int'):(self.add_str_int,False),
            ('str','bool'):(self.add_str_bool,False),

            ('int','str'):(self.add_str_int,True),
            ('int','int'):(self.add_int_int,False),
            ('int','bool'):(self.add_int_bool,False),

            ('bool','str'):(self.add_str_bool,True),
            ('bool','int'):(self.add_int_bool,True),
            ('bool','bool'):(self.add_bool_bool,False),

            ('vector', 'vector'):(self.add_vector_vector,False),
        }

        self.subtraction_matrix = {
#            ('str','str'):(self.subtract_str_str,False),
#            ('str','int'):(self.subtract_str_int,False),
#            ('str','bool'):(self.subtract_str_bool,False),
#
#            ('int','str'):(self.subtract_str_int,True),
#            ('int','int'):(self.subtract_int_int,False),
#            ('int','bool'):(self.subtract_int_bool,False),
#
#            ('bool','str'):(self.subtract_str_bool,True),
#            ('bool','int'):(self.subtract_int_bool,True),
#            ('bool','bool'):(self.subtract_bool_bool,False),
        }

    def get_type(self, x, follow_symbols=True, recurse_symbols=True, thread=0):

        if follow_symbols:
            x = self.threads.symbol_table(thread).get_from_symbol_table(x, recurse=recurse_symbols)

        if String.is_string(x):
            return 'str'
        elif Numeric.is_numeric(x):
            return 'int'
        elif Boolean.is_boolean(x):
            return 'bool'
        elif Indicator.is_indicator(x):
            return 'indicator'
        elif Vector.is_vector(x):
            return 'vector'
        # elif Float.is_float(x):
        #    return 'float'
        # elif Date.is_date(x):
        #    return 'date'
        elif self.threads.symbol_table(thread).is_symbol(x):
            return 'symbol'
        else:
            return None

    def get_value(self, x, follow_symbols=True, recurse_symbols=True,
                  decode=True, thread=0):

        data_type = self.get_type(x, follow_symbols=follow_symbols,
                                  recurse_symbols=recurse_symbols)
        if follow_symbols:
            x = self.threads.symbol_table(thread).get_from_symbol_table(x, recurse=recurse_symbols)

        results = x
        if data_type == 'str':
            if decode:
                results = String(x).decode()
        elif data_type == 'int':
            if decode:
                results = Numeric(x).decode()
        elif data_type == 'bool':
            if decode:
                results = Boolean(x).decode()
        elif data_type == 'indicator':
            if decode:
                results = Indicator(x).decode()
        elif data_type == 'vector':
            if decode:
                reesults = Vector(x).decode()
        elif data_type == 'symbol':
            pass
        else:
            results = None

        return results

    def update_mangle(self, direction):
        if not direction:
            mangle_state = self.state.assign_mangle_state % 3
            if mangle_state == 0:
                self.state.mangle = self.state.ip
            elif mangle_state == 1:
                self.state.mangle = self.state.code[self.state.ip].importance
            else:
                self.state.mangle = self.state.importance
            # This just makes it silly.
            # self.state.assign_mange_state += 1

        self.state.mangle += direction

    def compare(self, a_value, b_value, decoded=True):
        # TODO
        if not decoded:
            # TODO 
            # extract symbols - compare flat
            return a_value == b_value
        else:
            # TODO 
            # extract symbols, decode then compare
            return False

    def encode(self, value, data_type):

        results = None
        if data_type == 'str':
            results = String(x).encode()
        elif data_type == 'int':
            results = Numeric(x).encode()
        elif data_type == 'bool':
            results = Boolean(x).encode()
        elif data_type == 'indicator':
            results = Indicator(x).encode()
        elif data_type == 'vector':
            results = Vector(x).encode()

        return results

    def walk_elements(self, a, b):
        total_len = len(a)
        if len(b) > total_len:
            total_len = len(b)

        for x in range(0, total_len):
            a_value = None
            if x < len(a):
                a_value = a[x]
            b_value = None
            if x < len(b):
                b_value = b[x]
            yield a_value, b_value

    def assign(self, src, dest):
        src_type = self.get_type(src)
        src_value = self.get_value(src, decode=False)
        if self.symbol_table.is_symbol(dest):
            dest_value = self.get_value(dest, decode=False)
            dest_type = self.get_type(dest)
            method = self.__getattribute__('assign_%s_%s' % (src_type, dest_type))
            results = method(src_value, dest_value)
            self.symbol_table.symbol_table[dest] = results

        else:
            self.symbol_table.symbol_table[dest] = results

        self.update_mangle(None)

    def add_str_str(self, a, b):
        pass

    def add_str_int(self, a, b):
        pass

    def add_str_bool(self, a, b):
        pass

    def add_int_int(self, a, b):
        pass

    def add_int_bool(self, a, b):
        pass

    def add_bool_bool(self, a, b):

        # Modes:
        # 1) trinary add (somewhat mangled)
        # 2) append src and dest
        # 3) interleave src/dest (keeping all elements)
        # 4) interleave src/dest (alternating elements)

        mangle = self.state.mangle % 4

        new_value = ['?']
        a_array = Boolean(a).element_array()
        b_array = Boolean(b).element_array()

        # Implement whatever bizarre boolean addition logic here
        results_map = [
            {
                ('<','<') : '<',  # 0 0 - 0
                ('<','>') : '>',  # 0 1 - 1
                ('<','^') : '^',  # 0 2 - 2
                ('>','<') : '>',  # 1 0 - 1 1
                ('>','>') : '^',  # 1 1 - 2 1
                ('>','^') : '<',  # 1 2 - 0 2
                ('^','<') : '^',  # 2 0 - 2 0
                ('^','>') : '<',  # 2 1 - 0 1
                ('^','^') : '>',  # 2 2 - 1 2
            }
        ]

        for s,d in self.walk_elements(a_array, b_array):
            if s and d:
                new_value.append(results_map[0][(s, d)])
            elif s:
                new_value.append(s)
            else:
                new_value.append(d)

        return ''.join(new_value)

    def add_vector_vector(self, a, b):
        mangle = self.state.mangle % 4

        new_value = ['^']
        a_array = Vector(a).element_array()
        b_array = Vector(b).element_array()

        for s, d in self.walk_elements(a_array, b_array):
            if s and d:
#                print "%s, %s => %s" % (s[0], d[0], (int(s[0]) + int(d[0]) ) % 9 + 1)
                direction = (int(s[0]) + int(d[0]) - 1) % 9 + 1
                distance = (int(s[1]) + int(d[1])) % 9 # (% 11)
                op = ''
                new_value.append('%s%s%s' % (direction, distance, op))

            elif s:
                new_value.append("%s%s%s" % (s[0], s[1], s[2]))
            else:
                new_value.append("%s%s%s" % (d[0], d[1], d[2]))

        return ''.join(new_value)

    def add(self, src, dest):

        src_type = self.get_type(src)
        src_value = self.get_value(src, decode=False)
        if self.symbol_table.is_symbol(dest):
            dest_value = self.get_value(dest, decode=False)
            dest_type = self.get_type(dest)
        else:
            self.assign(src, dest)
            return

#        method = self.__getattribute__('add_%s_%s' % (src_type, dest_type))
        (method, reverse) = self.addition_matrix[src_type, dest_type]
        if reverse:
            results = method(dest_value, src_value)
        else:
            results = method(src_value, dest_value)
        self.symbol_table.symbol_table[dest] = results

        self.update_mangle(1)

    def subtract(self, x, y):
        src_type = self.get_type(src)
        src_value = self.get_value(src, decode=False)
        if self.symbol_table.is_symbol(dest):
            dest_value = self.get_value(dest, decode=False)
            dest_type = self.get_type(dest)
        else:
            self.assign(src, dest)
            return

        method = self.__getattribute__('subtract_%s_%s' % (src_type, dest_type))
        results = method(src_value, dest_value)
        self.symbol_table.symbol_table[dest] = results

        self.update_mangle(-1)

    def mangle(self, x, y):
        pass
