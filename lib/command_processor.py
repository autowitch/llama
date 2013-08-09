from lib.command_constants import CommandConstants
from lib.command import Command
from lib.ll_string import String
from lib.ll_numeric import Numeric
from lib.ll_boolean import Boolean
from lib.ll_indicator import Indicator
from lib.ll_vector import Vector
from lib.ll_method import Method
from lib.ll_class import Class
from lib.data import Data

class CommandProcessor(object):

    """docstring for CommandProcessor"""

    def __init__(self, llama):
        super(CommandProcessor, self).__init__()
        self.llama = llama
        self.threads = llama.threads
        self.data = Data(self.threads)

        self.built_in_methods = {
            'READ OUT':self.read_out,
            'WRITE IN':self.write_in
        }

        self.command_handlers = {
            'REM':self.rem,
            'NOP':self.nop,
            'COME FROM':self.come_from,
            '<=': self.assign_left,
            '=>': self.assign_right,
            '<-': self.subtract_left,
            '->': self.subtract_right,
            '<+': self.add_left,
            '+>': self.add_right
        }

    def come_from(self, x, y, thread=0):
        pass

    def check_come_from_value(self, ip, value, thread=0):

        # COME FROM statements that aren't important enough will be
        # ignored.
        if not self.llama.is_important_enough(self.threads.code(thread)[ip].importance):
            return False

        # Get the IP of the statement that is ip_dir from the COME FROM
        # and get whatever value the command has.
        new_ip = self.llama.next_ip(ip)
        compare_value = self.llama.threads.code(thread)[new_ip].command
        compare_value = self.threads.symbol_table(thread).get_from_symbol_table(compare_value)
        return value == compare_value

    def check_come_from(self, value, thread=0):
        # TODO Index COME Froms? - may be fun with a constantly changine
        # code base
#        value = self.symbol_table.get_from_sybmol_table(value)
        for x in range(0, len(self.threads.code(thread))):
            if self.threads.code(thread)[x].command == 'COME FROM':
                if self.check_come_from_value(x, value):
                    # TODO: Multithread here - array of ip or program state?
                    new_thread_id = self.threads.copy(thread)
                    new_ip = self.llama.next_ip(x)
                    new_ip = self.llama.next_ip(new_ip)
                    self.threads.set_ip(new_ip, thread=new_thread_id)
                    # self.threads.set_ip(new_ip, thread=thread)
                    #self.last_value = None # To prevent redoing this
                    self.threads.set_last_value(None, thread=thread) # To prevent redoing this
                    self.threads.set_last_value(None, thread=new_thread_id) # To prevent redoing this
                    self.debug(3, "Executing Come From: Sending IP to %s" % new_ip, thread=thread,
                            ip=self.threads.ip(thread))
                    self.debug(3, "The IP will increment from that point", thread=thread,
                            ip=self.threads.ip(thread))
                    return True
                else:
                    pass
        return False

    def read_out(self, x, thread=0):
        data = None
        target = self.threads.symbol_table(thread).get_from_symbol_table(x)
        if String.is_string(target):
            string_value = String(target)
            data = string_value.decode(target[1:])
        elif Numeric.is_numeric(target):
            numeric_value = Numeric(target)
            data = numeric_value.decode(target[1:])
        elif Boolean.is_boolean(target):
            boolean_value = Boolean(target, classic=self.llama.tight)
            data = boolean_value.decode(target)
        elif Vector.is_vector(target):
            vector_value = Vector(target)
            data = vector_value.decode()
        elif Indicator.is_indicator(target):
            # Indicators cannot be read out
            self.debug(1, "Attempt to read out an indicator: %s" % target, msg_type="WRN", thread=thread,
                    ip=self.threads.ip(thread))

        if data:
            self.debug(4, "Called readout with %s displayed as %s" % \
                    (target, data), thread=thread,
                    ip=self.threads.ip(thread))
            print data

    def write_in(self, x, thread=0):
        pass

    def nop(self, x, y, thread=0):
        pass

    def rem(self, x, y, thread=0):
        pass

    def assign_left(self, x, y, thread=0):
        for x_value in x:
            for y_value in y:
                if x_value.command in self.built_in_methods:
                    self.debug(4, "Built in method %s is target of assignment" %  \
                            x_value.command, thread=thread,
                            ip=self.threads.ip(thread))
                    self.built_in_methods[x_value.command](y_value.command, thread=thread)
                else:
                    new_symbol = self.threads.symbol_table(thread).get_new_symbol(y_value.command)
                    symbol = self.threads.symbol_table(thread)
                    self.threads.symbol_table(thread).symbol_table[x_value.command] = y_value.command
                    self.llama.threads.set_last_value(new_symbol, thread=thread)
                    self.debug(3, "Assigned:  \x1b[1;33m%s = %s" % (x_value.command, y_value.command), thread=thread,
                            ip=self.threads.ip(thread))
                    if self.check_come_from(new_symbol):
                        self.debug(3, "COME FROM found after left assignment", thread=thread,
                                ip=self.threads.ip(thread))
                        return

    def assign_right(self, x, y, thread=0):
        return self.assign_left(y, x, thread=thread)

    def subtract_left(self, x, y, thread=0):
        pass

    def subtract_right(self, x, y, thread=0):
        return self.subtract_left(y, x)

    def add_left(self, x, y, thread=0):
        for x_value in x:
            for y_value in y:
                self.data.add(y_value.command, x_value.command)

    def add_right(self, x, y, thread=0):
        return self.add_left(y, x)

    def extract_command_elements(self, command_stack, thread=0):
        state = 0
        arg_0 = []
        commands = []
        arg_1 = []

        for x in command_stack:

            is_command = CommandConstants.is_command(x)
#            is_symbol = self.symbol_table.is_symbol(x)

            if is_command and state == 0:
                state = 1
            elif not is_command and state == 1:
                state = 2

            if state == 0:
                arg_0.append(x)
            elif state == 1:
                commands.append(x)
            elif state == 2:
                arg_1.append(x)

        return (arg_0, commands, arg_1)

    def is_constant(self, value, thread=0):
        if self.threads.symbol_table(thread).is_symbol(value):
            return False

        return String.is_string(value) or Numeric.is_numeric(value) or \
                Boolean.is_boolean(value) or Vector.is_vector(value) or \
                Indicator.is_indicator(value)

    def flatten(self, args):
        new_symbol = [x for x in args if not self.is_constant(x.command)]
        # TODO - betterized flattening - taking into account types?
        new_const = ''.join([x.command for x in args if self.is_constant(x.command)])
        if new_const:
            c = Command()
            c.command = new_const
            new_symbol.append(c)
        return new_symbol

    def process(self, command_stack, thread=0):

        arg_0, commands, arg_1 = \
                self.extract_command_elements(command_stack, thread=thread)

        self.debug(11, "Executing command: %s" % command_stack, thread=thread,
                ip=self.threads.ip(thread))
        self.debug(11, "Raw Arg0:          %s" % arg_0, thread=thread,
                ip=self.threads.ip(thread))
        self.debug(11, "Commands:          %s" % commands, thread=thread,
                ip=self.threads.ip(thread))
        self.debug(11, "Raw Arg1:          %s" % arg_1, thread=thread,
                ip=self.threads.ip(thread))

        # TODO - needs code to flatten constants (auto append)
        arg_0 = self.flatten(arg_0)
        arg_1 = self.flatten(arg_1)

        self.debug(11, "Flattened Arg0:    %s" % arg_0, thread=thread,
                ip=self.threads.ip(thread))
        self.debug(11, "Flattened Arg1:    %s" % arg_1, thread=thread,
                ip=self.threads.ip(thread))

        for c in commands:
            self.debug(11, "Executing %s against %s and %s" % \
                    (c, arg_0, arg_1), thread=thread,
                    ip=self.threads.ip(thread))
            self.command_handlers[c.command](arg_0, arg_1, thread=thread)

