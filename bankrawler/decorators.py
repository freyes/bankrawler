import sys


def Property(func):
    keys = 'fget', 'fset', 'fdel'
    func_locals = {'doc':func.__doc__}

    def probeFunc(frame, event, arg):
        if event == 'return':
            locals = frame.f_locals
            func_locals.update(dict((k,locals.get(k)) for k in keys))
            sys.settrace(None)
        return probeFunc

    sys.settrace(probeFunc)
    func()
    return property(**func_locals)
