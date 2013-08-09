import copy

from lib.program_state import ProgramState


class Threads(object):

    def __init__(self):
        self.threads = [ProgramState()]
        self.alive = True

    def thread(self, thread=0):
        return self.threads[thread]

    def importance(self, thread=0):
        if not self.threads[thread]:
            return None
        return self.threads[thread].importance

    def set_importance(self, new_value, thread=0):
        if not self.threads[thread]:
            return None
        self.threads[thread].importance = new_value

    def inc_importance(self, amount=1, thread=0):
        if not self.threads[thread]:
            return None
        self.threads[thread].importance += amount

    def dec_importance(self, amount=1, thread=0):
        if not self.threads[thread]:
            return None
        if self.threads[thread].importance > 1:
            self.threads[thread].importance -= amount

    def code(self, thread):
        if not self.threads[thread]:
            return None
        return self.threads[thread].code

    def ip(self, thread=0, subthread=0):
        if not self.threads[thread]:
            return None
        return self.threads[thread].ip

    def set_ip(self, new_value, thread=0, subthread=0):
        if not self.threads[thread]:
            return None
        self.threads[thread].ip = new_value

    def ip_dir(self, thread=0, subthread=0):
        if not self.threads[thread]:
            return None
        return self.threads[thread].ip_dir

    def set_ip_dir(self, new_value, thread=0, subthread=0):
        if not self.threads[thread]:
            return None
        self.threads[thread].ip_dir = new_value

    def execution_probability(self, thread=0):
        if not self.threads[thread]:
            return None
        return self.threads[thread].execution_probability

    def command_stack(self, thread=0):
        if not self.threads[thread]:
            return None
        return self.threads[thread].command_stack

    def symbol_table(self, thread=0):
        if not self.threads[thread]:
            return None
        return self.threads[thread].symbol_table

    def last_value(self, thread=0, subthread=0):
        if not self.threads[thread]:
            return None
        return self.threads[thread].last_value

    def set_last_value(self, new_value, thread=0, subthread=0):
        if not self.threads[thread]:
            return None
        self.threads[thread].last_value = new_value

    def code_line_stack(self, thread=0):
        if not self.threads[thread]:
            return None
        return self.threads[thread].code_line_stack

    def full_command_cache(self, thread=0):
        if not self.threads[thread]:
            return None
        return self.threads[thread].full_command_cache

    def maybe_stack(self, thread=0):
        if not self.threads[thread]:
            return None
        return self.threads[thread].maybe_stack

    def forget_stack(self, thread=0):
        if not self.threads[thread]:
            return None
        return self.threads[thread].forget_stack

    def invert_next_importance_check(self, thread=0):
        if not self.threads[thread]:
            return None
        return self.threads[thread].invert_next_importance_check

    def set_invert_next_importance_check(self, new_value, thread=0):
        if not self.threads[thread]:
            return None
        self.threads[thread].invert_next_importance_check = new_value

    def swing_ip(self, thread=0):
        if not self.threads[thread]:
            return None
        return self.threads[thread].swing_ip

    def enable_rhi(self, thread=0):
        if not self.threads[thread]:
            return None
        return self.threads[thread].enable_rhi

    def mangle(self, thread=0):
        if not self.threads[thread]:
            return None
        return self.threads[thread].mangle

    def assign_mangle_source(self, thread=0):
        if not self.threads[thread]:
            return None
        return self.threads[thread].assign_mangle_source

    def reverse_next_assignment_arrow(self, thread=0):
        if not self.threads[thread]:
            return None
        return self.threads[thread].reverse_next_assignment_arrow

    def instruction_skip(self, thread=0):
        if not self.threads[thread]:
            return None
        return self.threads[thread].instruction_skip

    def swap_rhi_and_value(self, thread=0):
        if not self.threads[thread]:
            return None
        return self.threads[thread].swap_rhi_and_value

    def invert_this(self, thread=0):
        if not self.threads[thread]:
            return None
        return self.threads[thread].invert_this

    def set_invert_this(self, new_value, thread=0):
        if not self.threads[thread]:
            return None
        self.threads[thread].invert_this = new_value

    def last_smiley(self, thread=0, subthread=0):
        if not self.threads[thread]:
            return None
        return self.threads[thread].last_smiley

    def set_last_smiley(self, new_value, thread=0):
        if not self.threads[thread]:
            return None
        self.threads[thread].last_smiley = new_value

    # command builder stuff

    def command(self, thread=0):
        if not self.threads[thread]:
            return None
        return self.threads[thread].command
    
    def set_command(self, new_value, thread=0):
        if not self.threads[thread]:
            return None
        self.threads[thread].command = new_value

    def command_state(self, thread=0):
        if not self.threads[thread]:
            return None
        return self.threads[thread].command_state

    def set_command_state(self, new_value, thread=0):
        if not self.threads[thread]:
            return None
        self.threads[thread].command_state = new_value

    def complete(self, thread=0):
        if not self.threads[thread]:
            return None
        return self.threads[thread].complete

    def set_complete(self, complete=False, thread=0):
        if not self.threads[thread]:
            return None
        self.threads[thread].complete = complete

    def copy(self, source_thread):
        if not self.threads[source_thread]:
            return None
        new_thread = copy.deepcopy(self.threads[source_thread])
        new_thread.last_smiley = None
        new_thread.command_stack = []
        new_thread.command = []
        new_thread.command_state = 0
        new_thread.complete = False

        self.threads.append(new_thread)
        new_thread_id = len(self.threads) - 1
        self.debug(4, "New thread %s created from %s" % (new_thread_id, source_thread))
        return new_thread_id

    def delete(self, thread_id):
        if not self.threads[thread_id]:
            return None
        self.debug(4, "Deleting thread %d" % thread_id)
        self.threads[thread_id] = None
        thread_count = 0
        for x in self.threads:
            if x:
                thread_count += 1
        if not thread_count:
            self.debug(4, "No threads remain, we are no longer alive")
            self.alive = False
        else:
            self.debug(5, "%d active threads" % thread_count)

    def collapse(self, thread_1, thread_2):
        pass

    def mingle(self, thread_1, thread_2):
        pass

    def thread_alive(self, thread=0):
        return self.threads[thread] != None
