import copy
import re

from lib.command_constants import CommandConstants


class Smiley(object):

    """docstring for Smiley"""

    # TODO:
    #     Mangle mode up/down
    #     Mangle mode on <= from importance/overall importance/line number
    PRE = 1
    POST = 2

    def __init__(self, llama):
        super(Smiley, self).__init__()
        self.llama = llama

        # some convenience assignments
        self.threads = llama.threads
        self.reconsider_stack = []

    def inc_code_line_importance(self, thread=0):
        self.threads.code(thread)[self.threads.ip(thread)].importance += 1

    def cache_apply_full_command(self, thread=0):
        pass

    def dec_code_line_importance(self, thread=0):
        if self.threads.code(thread)[self.threads.ip(thread)].importance > 1:
            self.threads.code(thread)[self.threads.ip(thread)].importance -= 1

    def inc_overall_importance(self, thread=0):
        self.threads.inc_importance(thread)

    def dec_overall_importance(self, thread=0):
        self.threads.dec_importance(thread)

    def rotate_data_element_indexed_by_importance(self, thread=0):
        pass

    def inc_ip_skip(self, thread=0):
        self.state.ip_dir += 1
        if not self.state.ip_dir:
            self.state.ip_dir = 1

    def dec_ip_skip(self, thread=0):
        self.state.ip_dir -= 1
        if not self.state.ip_dir:
            self.state.ip_dir = -1

    def dec_statement_execution_probablity(self, thread=0):
        if self.code[self.state.ip].execution_probability > 10:
            self.code[self.state.ip].execution_probability -= 5
        # TODO: May want overall execution probabilities

    def inc_statement_execution_probablity(self, thread=0):
        if self.code[self.state.ip].execution_probability < 100:
            self.code[self.state.ip].execution_probability -= 5

    def push_code_line_to_stack(self, thread=0):

        """
        This will take a copy of the current code line and push it onto a stack.
        It can later be inserted back into the code.
        """

        self.state.code_line_stack.append(self.code[self.state.ip])

    def pop_insert_from_code_line_stack(self, thread=0):
        pass

    def replace_indexed_by_importance(self, thread=0):
        cmd = self.code[self.state.ip].command
        if cmd in self.symbol_table:
            offset = self.state.importance
            if offset >= len(self.symbol_table):
                offset = len(self.symbol_table) - 1
            self.code[self.state.ip].command = self.symbol_table[offset]

    def pop_replace_from_code_line_stack(self, thread=0):
        if len(self.state.code_line_stack):
            code_line = self.state.code_line_stack.pop()
        self.code[self.state.ip] = code_line

    def dec_all_statements_importance(self, thread=0):
        for x in self.code:
            if x.importance > 1:
                x.importancd -= 1

    def reverse_importance_evaulation_of_next(self, thread=0):
        self.state.invert_next_importance_check = not self.state.invert_next_importance_check

    def remove_data_element_indexed_by_importance(self, thread=0):
        pass

    def reconsider(self, thread=0):
        current_state = copy.deepcopy(self.state)
        self.reconsider_stack.append(current_state)

    def maybe(self, thread=0):
        if self.reconsider_stack:
            new_state = self.reconsider_stack.pop()
            # In-place updating of state
            for x in new_state.__dict__:
                self.state.__dict__[x] = new_state.__dict__[x]
            self.state.invert_this = True

    def swap_surrounding_code_lines(self, thread=0):
        ip1 = self.state.next_ip()
        ip2 = self.state.next_ip(ip_dir=self.state.ip_dir * -1)
        tmp = self.code[ip1]
        self.code[ip1] = self.code[ip2]
        self.code[ip2] = tmp

    def assemble_full_command_ignoring_next_action(self, thread=0):
        pass

    def inc_all_statements_importance(self, thread=0):
        for x in self.code:
            x.importancd += 1

    def forget(self, thread=0):

        """
        ABSTAIN (Proudly stolen from INTERCAL)

        If on a symbol, the symbol is removed from the symbol table, cached
        and can be brought back if a REINSTATE is executed on the same
        symbol. If the symbol is reinstated, it will be restore with it's
        original value. Nothing can read or write to this symbol while it
        is abstained. It will be ignored for the purposes of constructing
        full statements.

        If on an statement (NOP, COME FROM, => and the like), that statement
        type no longer exists (as far as the interpreter is concerned) and
        will be ignored when constructing full statements. It can be
        REINSTATED by using the reinstate smiley on the same command.

        The same behaviour applies when ABSTAINING on a target (method)
        (WRITE IN, READ OUT and the like). Those targets will no longer
        exist as far as the interpreter is concerned and will not be used
        in statement construction.

        If a value is ABSTAINED. The value no longer exists. Nothing can be
        set to it, and nothing with that value can be read.
        """

        forget_it = self.code[self.state.ip].command
        if forget_it not in self.state.forget_stack:
            self.state.forget_stack.append(forget_it)

    def remember(self, thread=0):

        """
        REINSTATE (Proudly stolen from INTERCAL)

        Undoes the action of an ABSTAIN. See abstain() for details.

        When REINSTATING on a non-abstained value, the interpreter will
        ignore the reinstation.
        """

        forget_it = self.code[self.state.ip].command
        if forget_it in self.state.forget_stack:
            self.state.forget_stack.remove(forget_it)

    def offset_by_importance(self, thread=0):
        pass

    def toggle_swing_ip(self, thread=0):
        self.state.swing_ip = not self.state.swing_ip

    def jump_importance_times_ip_dir(self, thread=0):
        offset = self.code[self.state.ip].ip_dir * \
                self.code[self.state.ip].importance
        self.state.ip = self.state.next_ip(ip_dir=offset)

    def jump_importance_times_neg_ip_dir(self, thread=0):
        offset = self.code[self.state.ip].ip_dir * \
                self.code[self.state.ip].importance * -1
        self.state.ip = self.state.next_ip(ip_dir=offset)

    def toggle_swap_rhi_and_value(self, thread=0):
        self.state.swap_rhi_and_value = False

    def rotate_assignment_mangle_mode(self, thread=0):
        self.state.assignment_mangle_mode += 1
        if self.state.assignment_mangle_mode > 5:
            self.state.assignment_mangle_mode = 1

    def clown_nose_buffer(self, thread=0):
        pass

    def rotate_data_element_up_to_importance_idx(self, thread=0):
        pass

    def swap_statement_overall_importance(self, thread=0):
        statement_importance = self.code[self.state.ip].importance
        self.code[self.state.ip].importance = self.state.importance
        self.state.importance = statement_importance

    def reverse_ip(self, thread=0):
        self.state.ip_dir *= -1

    def delete_current_code_line(self, thread=0):
        pass

    def skip_next_instruction(self, thread=0):
        self.state.instruction_skip = True

    def set_execution_probability_to_50(self, thread=0):
        self.code[self.state.ip].execution_probability = 50

    def move_cur_code_line_to_end(self, thread=0):
        pass

    def move_cur_code_line_neg_ip_dir(self, thread=0):
        pass

    def disable_rhi(self, thread=0):
        self.state.enable_rhi = False

    def enable_rhi(self, thread=0):
        self.state.enable_rhi = True

    def invert_rhi(self, thread=0):
        self.state.enable_rhi = not self.state.enable_rhi

    def reverse_next_assignment_arrow(self, thread=0):
        self.state.reverse_next_assignment_arrow = True
        pass

    def mood_rotator(self, thread=0):
        pass

    def evil_mode(self, thread=0):
        pass

    def invert_smiley(self, thread=0):
        pass

    def swap_smileys_with_prev(self, thread=0):
        ip1 = self.state.ip
        ip2 = self.state.next_ip(ip_dir=self.state.ip_dir * -1)
        tmp = self.code[ip1].smiley
        self.code[ip1].smiley = self.code[ip2].smiley
        self.code[ip2].smiley = tmp

    def swap_importance_with_prev(self, thread=0):
        ip1 = self.state.ip
        ip2 = self.state.next_ip(ip_dir=self.state.ip_dir * -1)
        tmp = self.code[ip1].importance
        self.code[ip1].importance = self.code[ip2].importance
        self.code[ip2].importance = tmp

    def swap_statement_with_prev(self, thread=0):
        ip1 = self.state.ip
        ip2 = self.state.next_ip(ip_dir=self.state.ip_dir * -1)
        tmp = self.code[ip1]
        self.code[ip1] = self.code[ip2]
        self.code[ip2] = tmp

    def inc_or_dec_importance_based_on_last_value(self, thread=0):

        """
        If the symbol or constant is the same as the last_value in the
        program state, increment the importance by one. Otherwise, decrement
        it by one.

        If the command is an actual command (action), increment if it is the
        same as the last command executed (last_command). Otherwise, decrement.
        """

        pass

    def inc_mangle_mode(self, thread=0):

        """
        The mangle mode is used during additions, subtractions and asisgnments
        to control how data is modified. So for additions, it will define
        just what addition actually means in this language. Their are multiple
        definitions of addition and the interpreter will iterate through them
        by using the modulus of the mangle mode. The number of mangle modes
        depends on the operation and the types of arguments being passed into
        the operation (adding two strings will have a different definition of
        add than adding a string and an integer - and the number of ways
        to perform the addition will vary).

        Normally assignment will just put a value into a variable. However,
        in some cases, it may merge the two instead. This depends on the
        current mangle mode.

        Mangle modes rotate up automatically with addition, down with
        subtraction and use either line number or importance on assignment.

        This provides a smiley to allow for more manual control of the
        mangle modes.
        """

        self.state.mangle += 1

    def dec_mangle_mode(self, thread=0):

        """
        The mangle mode is used during additions, subtractions and asisgnments
        to control how data is modified. So for additions, it will define
        just what addition actually means in this language. Their are multiple
        definitions of addition and the interpreter will iterate through them
        by using the modulus of the mangle mode. The number of mangle modes
        depends on the operation and the types of arguments being passed into
        the operation (adding two strings will have a different definition of
        add than adding a string and an integer - and the number of ways
        to perform the addition will vary).

        Normally assignment will just put a value into a variable. However,
        in some cases, it may merge the two instead. This depends on the
        current mangle mode.

        Mangle modes rotate up automatically with addition, down with
        subtraction and use either line number or importance on assignment.

        This provides a smiley to allow for more manual control of the
        mangle modes.
        """

        self.state.mangle -= 1

    def rotate_assign_mangle_set(self, thread=0):

        """
        Assignments modify the mangle mode as well as addition and subtraction.
        Addition always increments the mangle mode. Subtraction always
        decrements. Assignments don't move anything up or down, so a more
        ... creative ... method is used.

        The new mangle mode can come from:
            The line number
            The overall importance
            The importance of the current line
        """

        self.state.assign_mangle_source += 1

    def process(self, smiley, state, thread=0):
        mouth_methods = {
            ')':(self.inc_code_line_importance, Smiley.PRE),
            '|':(self.inc_or_dec_importance_based_on_last_value, Smiley.PRE),
            '(':(self.dec_code_line_importance, Smiley.PRE),
            '/':(self.inc_overall_importance, Smiley.PRE),
            '\\':(self.dec_overall_importance, Smiley.PRE),
            '0':(self.rotate_data_element_indexed_by_importance, Smiley.PRE),
            'O':(self.inc_ip_skip, Smiley.PRE),
            'o':(self.dec_ip_skip, Smiley.PRE),
            'p':(self.dec_statement_execution_probablity, Smiley.PRE),
            'q':(self.inc_statement_execution_probablity, Smiley.PRE),
            '@':(self.push_code_line_to_stack, Smiley.PRE),
            'Q':(self.pop_insert_from_code_line_stack, Smiley.PRE),
            'D':(self.replace_indexed_by_importance, Smiley.PRE),
            'b':(self.pop_replace_from_code_line_stack, Smiley.PRE),
            'C':(self.dec_all_statements_importance, Smiley.PRE),
            'd':(self.reverse_importance_evaulation_of_next, Smiley.PRE),
            'E':(self.remove_data_element_indexed_by_importance, Smiley.PRE),
            '[':(self.reconsider, Smiley.PRE),
            ']':(self.maybe, Smiley.PRE),
            '*':(self.swap_surrounding_code_lines, Smiley.PRE),
            'p':(self.assemble_full_command_ignoring_next_action, Smiley.PRE),
            'c':(self.inc_all_statements_importance, Smiley.PRE),
            '>':(self.forget, Smiley.POST),
            '<':(self.remember, Smiley.PRE),
            '3':(self.offset_by_importance, Smiley.PRE),
            '#':(self.toggle_swing_ip, Smiley.PRE),
            'F':(self.jump_importance_times_ip_dir, Smiley.PRE),
            '?':(self.jump_importance_times_neg_ip_dir, Smiley.PRE),
            'V':(self.toggle_swap_rhi_and_value, Smiley.PRE),
            'v':(self.rotate_assignment_mangle_mode, Smiley.PRE),
            '^':(self.cache_apply_full_command, Smiley.PRE),
        }

        nose_methods = {
            '-':None,
            '*':(self.clown_nose_buffer, Smiley.PRE),
            'O':(self.swap_smileys_with_prev, Smiley.POST),
            '+':(self.swap_importance_with_prev, Smiley.POST),
            '^':(self.swap_statement_with_prev, Smiley.POST),
            '':(self.rotate_data_element_up_to_importance_idx, Smiley.PRE),
            ' ':(self.rotate_data_element_up_to_importance_idx, Smiley.PRE),
        }

        eye_methods = {
            ':':(self.dec_code_line_importance, Smiley.POST),
            'b':(self.inc_code_line_importance, Smiley.POST),
            'p':(self.inc_overall_importance, Smiley.POST),
            '?':(self.dec_overall_importance, Smiley.POST),
            '=':(self.swap_statement_overall_importance, Smiley.PRE),
            ';':(self.reverse_ip, Smiley.PRE),
            'x':(self.delete_current_code_line, Smiley.POST),
            'X':(self.skip_next_instruction, Smiley.POST),
            '%':(self.set_execution_probability_to_50, Smiley.PRE),
            '8':(self.move_cur_code_line_to_end, Smiley.POST),
            'B':(self.move_cur_code_line_neg_ip_dir, Smiley.POST),
            '.':(self.disable_rhi, Smiley.PRE),
            "'":(self.enable_rhi, Smiley.PRE),
            '`':(self.invert_rhi, Smiley.PRE),
            '$':(self.reverse_next_assignment_arrow, Smiley.POST),
            'P':(self.inc_mangle_mode, Smiley.PRE),
            'S':(self.dec_mangle_mode, Smiley.PRE),
            '#':(self.rotate_assign_mangle_set, Smiley.PRE),
        }

        eyebrow_methods = {
            '|':(self.mood_rotator, Smiley.PRE),
            '>':(self.evil_mode, Smiley.PRE),
            '(':(self.invert_smiley, Smiley.PRE),
            '':None,
            ' ':None
        }

        m = re.match(CommandConstants.smile_expr, smiley)
        topper = m.group('topper')
        eyes = m.group('eyes')
        nose = m.group('nose')
        mouth = m.group('mouth')

        for symbol, handler in [(mouth, mouth_methods), #:
                                (nose, nose_methods),
                                (eyes, eye_methods),
                                (topper, eyebrow_methods)]:
            if not handler[symbol]:
                continue
            method, in_state = handler[symbol]
            if in_state == state:
                method(thread=thread)

