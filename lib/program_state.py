from lib.symbol_table import SymbolTable


class SubState(object):

    """docstring for SubState"""

    def __init__(self):
        super(SubState, self).__init__()
        self.ip = 0 # [0]
        self.ip_dir = 1 # [1]
        self.command_stack = []
        self.last_value = None
        self.last_smiley = None

        # command builder stuff
        self.command = []

        self.command_state = 0
        self.complete = False
        
class ProgramState(object):

    """docstring for ProgramState"""

    def __init__(self):

        super(ProgramState, self).__init__()

        self.sub_state = []

        self.importance = 3
        self.code = []

        self.ip = 0 # [0]
        self.ip_dir = 1 # [1]
        self.execution_probability = 100
        self.command_stack = []

        self.symbol_table = SymbolTable()

        # Contains the results of the last value assigned (or used)
        # This is used for:
        #     Evaluation of Right Hand Indicators (RHI)
        #     Evaluation of Come From statements
        self.last_value = None

        # The command stack is a repository for code lines that have been
        # cached (using the appropriate smiley)
        self.code_line_stack = []

        # Full commands can be cached and restored
        self.full_command_cache = []

        # A stack for holding the entire program state 
        self.maybe_stack = []

        self.forget_stack = []

        self.invert_next_importance_check = False
        self.swing_ip = None
        self.enable_rhi = True
        self.mangle = 0 # the mangle mode when doing add/subtract/assign
        self.assign_mangle_source = 0
        self.reverse_next_assignment_arrow = False
        self.instruction_skip = False
        self.swap_rhi_and_value = False
        self.invert_this = False

        self.last_smiley = None

        # command builder stuff
        self.command = []

        self.command_state = 0
        self.complete = False

    @staticmethod
    def clone(program_state):
        pass
