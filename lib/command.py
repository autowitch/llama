import re

from lib.command_constants import CommandConstants
from lib.errors import ParseError


class Command(object):

    """This is primarily a data bucket that holds information about
       a specific command"""

    def __init__(self, line="", free_format=False, tight=False):

        super(Command, self).__init__()

        self.free_format = free_format
        self.tight = tight

        self.smiley = ''
        self.importance = 3
        self.command = ''
        self.right_hand_indicator = None
        self.original_importance = 3
        self.topper = ''
        self.eyes = ''
        self.nose = ''
        self.mouth = ''
        self.execution_probability = 100
        self.command_type = CommandConstants.UNKNOWN

        if line:
            self.parse(line)

    def parse_smiley(self, line, orig):
        m = re.match(CommandConstants.smile_expr, line)
        if m:
            smiley = m.group('smiley')
            remainder = m.group('remainder')
            # TODO: Mixed sets and returns
            self.topper = m.group('topper')
            self.eyes = m.group('eyes')
            self.nose = m.group('nose')
            self.mouth = m.group('mouth')
            if self.eyes == '%':
                self.execution_probability = 50
        else:
            raise ParseError('%s does not start with a smiley' % orig)
        return smiley, remainder

    def parse_command(self, line, orig):
        command_expr = "\s*(?P<command>[^!]+)(?P<remainder>.*)$"
        m = re.match(command_expr, line)
        if m:
            command = m.group('command')
            remainder = m.group('remainder')
        else:
            raise ParseError("%s does not have a command" % orig)
        return command.strip(), remainder

    def parse_importance(self, line, orig):
        importance_expr = "\s*(?P<importance>![!1]*)\s*(?P<remainder>.*)$"
        m = re.match(importance_expr, line)
        if m:
            importance = m.group('importance')
            remainder = m.group('remainder')
        else:
            raise ParseError('%s does not have any importance' % orig)
        return len(importance), remainder

    def parse_rhi(self, line, orig):
        rhi_expr = "(?P<rhi>[^\s]*)\s*(?P<remainder>.*)"
        m = re.match(rhi_expr, line)
        rhi = ""
        remainder = ""
        if m:
            rhi = m.group("rhi")
            remainder = m.group("remainder")
        return rhi, remainder

    def __str__(self):
        return "%s    %s    %s    %s" % (self.smiley, self.command,
                                         self.importance,
                                         self.right_hand_indicator)

    def parse(self, line):
        orig = line
        if self.free_format:
            self.smiley, line = self.parse_smiley(line, orig)
            self.command, line = self.parse_command(line, orig)
            self.importance, line = self.parse_importance(line, orig)
            self.original_importance = self.importance
            self.right_hand_indicator, line = self.parse_rhi(line, orig)
        elif self.tight:
            self.smiley, tmp = self.parse_smiley(line[0:4].strip(), orig)
            self.command, tmp = self.parse_command(line[4:49].strip(), orig)
            self.importance, tmp = self.parse_importance(line[49:64].strip(), orig)
            self.original_importance = self.importance
            self.right_hand_indicator, tmp = self.parse_rhi(line[64:79].strip(), orig)
        else:
            self.smiley, tmp = self.parse_smiley(line[0:4].strip(), orig)
            self.command, tmp = self.parse_command(line[4:79].strip(), orig)
            self.importance, tmp = self.parse_importance(line[79:131].strip(), orig)
            self.original_importance = self.importance
            self.right_hand_indicator, tmp = self.parse_rhi(line[131:200].strip(), orig)

    def __repr__(self):
        return "<%s, %s, %s (%s), %s: %s>" % (self.smiley, self.command, self.importance, 
                self.original_importance, self.right_hand_indicator,
                self.command_type)
