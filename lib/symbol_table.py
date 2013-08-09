

class SymbolTable(object):

    UNKNOWN = -1
    STRING = 1
    NUMERIC = 2
    BOOLEAN = 3
    METHOD = 10
    CLASS = 20

    """docstring for SymbolTable"""
    def __init__(self):
        super(SymbolTable, self).__init__()
        self.symbol_table = {}

    def get_from_symbol_table(self, x, recurse=False):
        if self.is_symbol(x):
            if recurse:
                while self.is_symbol(x):
                    x = self.symbol_table[x]
                return x
            else:
                return self.symbol_table[x]
        else:
            return x

    def add_symbol(self, name, symbol, symbol_type=None):
        if symbol_type:
            symbol = symbol_type
        elif symbol is String:
            self.symbol_table[name] = [symbol, STRING]
        elif symbol is Numeric:
            self.symbol_table[name] = [symbol, NUMERIC]
        elif symbol is Boolean:
            self.symbol_table[name] = [symbol, BOOLEAN]
        elif symbol is Method:
            self.symbol_table[name] = [symbol, METHOD]
        elif symbol is Class:
            self.symbol_table[name] = [symbol, CLASS]

    def get_new_symbol(self, x):
        """
        Returns a String, Numeric, xxx
        object based on what x ix
        """
        return x
        if x in self.symbol_table:
            return x

    def is_symbol(self, x):
        return self.symbol_table.has_key(x)



