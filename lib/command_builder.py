from lib.command_constants import CommandConstants
from lib.common import show_cmd_stack


class CommandBuilder(object):

    """docstring for CommandExtractor"""

    def __init__(self, threads):
        super(CommandBuilder, self).__init__()
        self.threads = threads

    def is_complete(self, thread=0):
        return self.threads.complete(thread), False

    def build_command(self, new_command, thread=0):

        # Ignore any commands that are in the forget stack. When something
        # is forgotten, whether it is a command, constant, symbol, it is
        # really forgotten.
        self.debug(11, "Building command. State: %s, complete: %s" % \
                (self.threads.command_state(thread), self.threads.complete(thread)),
                thread=thread, ip=self.threads.ip(thread))
        self.debug(11, "Current command stack: %r" % self.threads.command(thread),
                thread=thread, ip=self.threads.ip(thread))
        if new_command.command in self.threads.forget_stack(thread):
            self.debug(4, "Forgot about " % new_command, msg_type="DBG", thread=thread,
                    ip=self.threads.ip(thread))
            return

        is_command = CommandConstants.is_command(new_command)
        self.debug(11, "%s is command: %s" % (new_command, is_command), thread=thread,
                ip=self.threads.ip(thread))
        if is_command and self.threads.command_state(thread) == 0:
            self.debug(11, "Changing to state 1", thread=thread,
                    ip=self.threads.ip(thread))
            self.threads.set_command_state(1, thread=thread)
        elif not is_command and self.threads.command_state(thread) == 1:
            self.debug(11, "Changing to state 2 and marking complete", thread=thread,
                    ip=self.threads.ip(thread))
            self.threads.set_command_state(2, thread=thread)
            self.threads.set_complete(complete=True, thread=thread)
        else:
            self.debug(11, "Adding %s with no state change" % new_command, thread=thread,
                    ip=self.threads.ip(thread))
        self.threads.command(thread).append(new_command)
        self.debug(11, "New command stack: %r" % self.threads.command(thread),
                thread=thread, ip=self.threads.ip(thread))

    def new(self, thread=0):
        self.debug(11, "Starting new command")
        self.threads.set_command_state(0, thread)
        self.threads.set_command([], thread)
        self.threads.set_complete(False, thread)
