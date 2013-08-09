class CommandConstants(object):

    # Types of commands
    UNKNOWN = -1
    ASSIGNMENT = 1
    CONTAINER_START = 10
    CONTAINER_END = 11
    GENERAL_NO_ARG = 50
    GENERAL_ONE_ARG = 51

    instruction_list = {'->':ASSIGNMENT,
                        '<-':ASSIGNMENT,
                        '<=':ASSIGNMENT,
                        '=>':ASSIGNMENT,
                        '+>':ASSIGNMENT,
                        '<+':ASSIGNMENT,
                        '(':CONTAINER_START,
                        ')':CONTAINER_END,
                        '[':CONTAINER_START,
                        ']':CONTAINER_END,
                        'NOP':GENERAL_NO_ARG,
                        'REM':GENERAL_ONE_ARG,
                        'COME FROM':GENERAL_ONE_ARG
                       }

    assignment_instructions = []
    container_start_instructions = []
    container_end_instructions = []
    general_no_arg_instructions = []
    general_one_arg_instructions = []

    command_templates = [
        [GENERAL_NO_ARG],
        [GENERAL_ONE_ARG, '*'],
        ['*', ASSIGNMENT, '*']
    ]

    _instr_mapping = {
        ASSIGNMENT:assignment_instructions,
        CONTAINER_START:container_start_instructions,
        CONTAINER_END:container_end_instructions,
        GENERAL_NO_ARG:general_no_arg_instructions,
        GENERAL_ONE_ARG:general_one_arg_instructions
    }

    for x in instruction_list:
        _instr_mapping[instruction_list[x]].append(x)

    smile_expr = '^\s*(?P<smiley>(?P<topper>[>|(]?)(?P<eyes>[:bp?=;xX%8B.\'`$PS#])(?P<nose>[-*O+^]?)(?P<mouth>[)|(/\\0Oopq@QDbCdE\[\]*pc><3#F?Vv^e]))\s*(?P<remainder>.*)$'

    """docstring for CommandConstants"""
    def __init__(self):
        super(CommandConstants, self).__init__()
        raise Exception("This class does not need to be instantiated")

    @staticmethod
    def is_command(command):
        if hasattr(command, 'command'):
            return command.command in CommandConstants.instruction_list
        else:
            return command in CommandConstants.instruction_list

#    @staticmethod
#    def _is_match(template_value, cmd, symbol_table):
#        if template_value == '*':
#            return True
#
#        cmd_value = cmd.command
#        cmd_value = symbol_table.get_from_symbol_table(cmd_value)
#
#        if not cmd_value in CommandConstants.instruction_list:
#            return False
#
#        if template_value == CommandConstants.instruction_list[cmd_value]:
#            return True
#
#        return False
#
#    @staticmethod
#    def _check_template(template, partial, symbol_table):
#        if len(template) > len(partial):
#            return False
#
#        good = True
#        z = zip(template, partial)
#        for t, c in z:
#            if not CommandConstants._is_match(t, c, symbol_table):
#                good = False
#
#        return good
#
#    @staticmethod
#    def is_complete(partial, symbol_table):
#        # TODO: NEEDS EPIC LOVE !!!!
#        # Returns this command and if the command can be extended
#        for template in CommandConstants.command_templates:
#            if CommandConstants._check_template(template, partial, symbol_table):
#                return True #, False
#
#        return False # , False
