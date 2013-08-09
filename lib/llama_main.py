import argparse
import re
import sys

from lib.errors import ParseError
from lib.command import Command
from lib.command_processor import CommandProcessor
from lib.command_builder import CommandBuilder
from lib.common import make_debug
#from lib.program_state import ProgramState
from lib.threads import Threads
from lib.smiley import Smiley


class Llama(object):

    """docstring for Llama"""

    def __init__(self):
        super(Llama, self).__init__()
        self.input_file = None

#        self.state = ProgramState()
        self.threads = Threads()

        self.processor = CommandProcessor(self)
        self.builder = CommandBuilder(self.threads)
        self.smiley = Smiley(self)

        self.free_format = False
        self.tight = False

    def parse_args(self):
        # args here
        # !! todo just test code
        parser = argparse.ArgumentParser(description='execute llama programs')
        parser.add_argument('input_file',
                            metavar='FILE',
                            type=argparse.FileType('r'),
                            default=None,
                            help='llamaa source file')
        parser.add_argument('-f', '--free-format',
                            action='store_true', default=False,
                            dest='free_format',
                            help='Allow more freely formatted code')
        parser.add_argument('--80',
                            action='store_true', default=False,
                            dest='tight',
                            help='Punch card (80 column) mode')
        parser.add_argument('-v', '--verbose', action='count',
                            help='debug level (repeat to increase detail)')

        args = parser.parse_args()
        self.input_file = args.input_file
        self.free_format = args.free_format
        self.tight = args.tight
#        global debug_level
        debug_level = args.verbose
        self.debug = make_debug(debug_level)
        self.processor.debug = make_debug(debug_level)
        self.builder.debug = make_debug(debug_level)
        self.smiley.debug = make_debug(debug_level)
        self.threads.debug = make_debug(debug_level)
#        print debug_level

    def is_blank(self, line):
        return re.match('^\s*$', line)

    def load(self):
        first = True
        try:
            for line in self.input_file:
                if first and line.startswith('#'):
                    continue
                line = line.strip()
                if self.is_blank(line):
                    continue
                command = Command(free_format=self.free_format,
                                  tight=self.tight)
                command.parse(line)
                self.threads.code(0).append(command)

        except ParseError, e:
            print >> sys.stderr, e
            return False
        return True

    def pre_process_smiley(self, smiley):
        self.smiley.process(smiley, Smiley.PRE)
        pass

    def post_process_smiley(self, smiley):
        self.smiley.process(smiley, Smiley.POST)
        pass

    def is_important_enough(self, importance, thread=0):
        return importance >= self.threads.importance(thread)

    def check_rhi(self, ip, last_value=None, thread=0):
        if not self.threads.enable_rhi(thread):
            return True

        if not last_value:
            last_value = self.threads.last_value(thread)

        if self.threads.code(thread)[ip].right_hand_indicator and last_value:

            # TODO: use a value evaluator - strings that are encoded
            # differently will still eval the same
            if self.threads.code(thread)[ip].right_hand_indicator != last_value:
                return False

        return True

    def fire_in_the_hole(self, command_stack, thread=0):
        # TODO: Following must move to processor
        if not command_stack:
            return
        self.processor.process(command_stack, thread=thread)
#        if len(command_stack) == 1:
#            return self.processor.process_len_1(command_stack)
#        elif len(command_stack) == 2:
#            return self.processor.process_len_2(command_stack)
#        elif len(command_stack) == 3:
#            return self.processor.process_len_3(command_stack)
#        else:
#            return self.processor.process_len_x(command_stack)

    def execute_instruction(self, command, ip, thread=0):

# TODO: Remove Flatten
#        partial = self.flatten(partial)

        self.builder.build_command(command, thread=thread)
        complete, extendable = self.builder.is_complete(thread=thread)
        if complete:
            self.fire_in_the_hole(self.threads.command(thread), thread=thread)
            self.builder.new(thread=thread)

    #def look_ahead(self, ip=-1, thread=0):
        #if ip == -1:
            #ip = self.threads.ip(thread)
        ##new_ip = self.move_ip(ip)
        #new_ip = self.next_ip(ip)
        #return self.threads.code(thread)[ip], new_ip

    def next_ip(self, ip=-1, ip_dir=-1, thread=0):

        """
        Gets the next IP (Instruction Pointer) based on the
        """

        if ip == -1:
            ip = self.threads.ip(thread)
        if ip_dir == -1:
            ip_dir = self.threads.ip_dir(thread)
        old_ip = ip
        ip += ip_dir
        if ip > len(self.threads.code(thread)):
            while ip > len(self.threads.code(thread)):
                ip -= self.threads.code(thread)
            ip_dir *= -1

        if ip <= 0:
            while ip <= 0:
                ip += self.threads.code(thread)
            ip_dir *= -1
        return ip

    def run(self):

        self.debug(1, "Executing llama in debug mode - level %s" % \
                   self.debug.debug_level)

        self.threads.set_ip(0, thread=0)
        done = False
        last_smiley = None
        while self.threads.alive and not done:
            self.debug(10, "================================================")
            for thread in range(0, len(self.threads.threads)):
                if not self.threads.thread_alive(thread):
                    continue
                command = self.threads.code(thread)[self.threads.ip(thread)]
                if thread != 0:
                    self.debug(10, "------------------------------------------------", thread=thread,
                            ip=self.threads.ip(thread))
                self.debug(2, "Executing:     \"\x1b[1;37m%s\x1b[0m\"" % command, thread=thread,
                        ip=self.threads.ip(thread))
                self.debug(5, "Current Mood:  %s" % self.threads.last_smiley(thread), thread=thread,
                        ip=self.threads.ip(thread))
                self.debug(5, "Importance:    %s" % self.threads.importance(thread), thread=thread,
                        ip=self.threads.ip(thread))
                self.debug(5, "Current IP:  : %s (ip dir is %s)" % \
                           (self.threads.ip(thread), self.threads.ip_dir(thread)), thread=thread,
                           ip=self.threads.ip(thread))
                if command.smiley ==self.threads.last_smiley(thread):
                    self.debug(0, "Overly stable moods: %s on %s" % (self.threads.last_smiley(thread), self.threads.ip(thread)), thread=thread, msg_type="ERR",
                            ip=self.threads.ip(thread))
                    done = True
                    break

                self.debug(10, "Pre-processing Smiley: %s " % command.smiley, thread=thread,
                        ip=self.threads.ip(thread))
                self.pre_process_smiley(command.smiley)
                self.debug(10, "Checking importance %d" % command.importance, thread=thread,
                        ip=self.threads.ip(thread))
                important_enough = self.is_important_enough(command.importance)
                self.debug(10, "is important: %s" % important_enough, thread=thread,
                        ip=self.threads.ip(thread))
                if self.threads.invert_this(thread):
                    self.debug(10, "But importance is inverted", thread=thread,
                            ip=self.threads.ip(thread))
                    important_enough = not important_enough
                    self.threads.set_invert_this(False, thread=thread)

                self.debug(10, "Checking RHI", thread=thread,
                        ip=self.threads.ip(thread))
                if important_enough and self.check_rhi(self.threads.ip(thread)):
                    self.debug(10, "Instruction is important and RHI is ok", thread=thread,
                            ip=self.threads.ip(thread))
                    self.debug(10, "\x1b[1;41;33m!!!! FIRE IN THE HOLE !!!!", thread=thread,
                            ip=self.threads.ip(thread))
                    self.execute_instruction(command, self.threads.ip(thread), thread=thread)

                self.debug(10, "Post-processing Smiley: %s " % command.smiley, thread=thread,
                        ip=self.threads.ip(thread))
                self.post_process_smiley(command.smiley)

                self.threads.set_last_smiley(command.smiley, thread=thread)

                if command.smiley == 'x-p':
                    self.debug(1, "Termination smiley found. Terminating", thread=thread,
                            ip=self.threads.ip(thread))
                    self.threads.delete(thread)
                else:
                    self.debug(10, "Setting next IP", thread=thread,
                            ip=self.threads.ip(thread))
                    self.threads.set_ip(self.next_ip(self.threads.ip(thread)), thread=thread)
                    self.debug(5, "New IP:      : %s (ip dir is %s) " % \
                               (self.threads.ip(thread), self.threads.ip_dir(thread)), thread=thread,
                               ip=self.threads.ip(thread))

                    if self.threads.invert_next_importance_check(thread):
                        self.debug(10, "Inverting next importance check", thread=thread,
                                ip=self.threads.ip(thread))
                        self.threads.set_invert_next_importance_check(False, thread=thread)
                        self.threads.set_invert_this(True, thread=thread)

                self.debug(5, "", thread=thread,
                        ip=self.threads.ip(thread))
