import inspect
import sys

#global debug_level
#debug_level = 0

def make_debug(debug_level=0):

    def debug(level, msg, level_override=0, msg_type='DBG', thread=None,
            subthread=None, ip=None):
        if debug_level >= level or level_override >= level:
            if not msg:
                print >> sys.stderr, ""
                return

            if thread == None:
                thread = "GLOBAL   "
            else:
                thread = "%-4.4d" % thread
                if subthread != None:
                    thread += ".%4.4d" % subthread
                else:
                    thread += '.0000'

            ip_value = "     "
            if ip != None:
                ip_value = ":%4.4d" % ip
            thread += ip_value

            frame = inspect.currentframe()
            frame = frame.f_back
            mod = inspect.getmodule(frame).__name__
            name = frame.f_code.co_name
            last_color = 32
            if msg_type == 'ERR':
                last_color = 31
            elif msg_type == 'WRN':
                last_color = 33
            elif msg_type == 'INF':
                last_color = 37
            location = "%s.%s" % (mod, name)
            print >> sys.stderr, "\x1b[1;33mLLAMA:\x1b[1;34m%02d:\x1b[1;35m%-3.3s:\x1b[36m%-35.35s \x1b[35m[%s] \x1b[1;%sm%s\x1b[0m" % \
                    (level, msg_type, location, thread, last_color, msg)

    debug.__setattr__('debug_level', debug_level)
    return debug

def show_cmd_stack(cmd):
    s = []
    for x in cmd:
        s.append(str(x))
    return '[%s]' % ',\n'.join(s)

