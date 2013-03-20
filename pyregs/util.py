import logging
import functools

log = logging.getLogger(__name__)

def bind(meth, func):
    obj = meth.__self__
    name = meth.__func__.__name__
    setattr(obj, name, func.__get__(obj, obj.__class__))


class LogMock:
    warning = lambda s: print('WARNING: {}'.format(s))
    error = lambda s: print('ERROR: {}'.format(s))
    info = lambda s: print('INFO: {}'.format(s))
    debug = lambda s: print('DEBUG: {}'.format(s))


def log_except(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except Exception as e:
            log.error('ERROR: {}'.format(e))
            raise e
    return wrapper


# class trace:
#     def __init__(self, f, log=None, wrap=True, log_enter=False,
#                  log_return=False):
#         self.f = f
#         self.wrap = wrap
#         self.log_enter = log_enter
#         self.log_return = log_return
#         if log is None:
#             self.log = LogMock
#         else:
#             self.log = log

#     def __call__(self, *args, **kwargs):
#         if self.log_enter:
#             arg_str = ', '.join(args)
#             kwa_str = ', '.join('{}={}'.format(arg, val)
#                                 for arg, val in kwargs.items())
#             self.log.debug('Calling {}({})'.format(self.f.__name__,
#                                                    arg_str + ' ' + kwa_str))

#         try:
#             ret = self.f(*args, **kwargs)
#         except Exception as e:
#             if self.wrap:
#                 self.log.error(e)
#         if self.log_return:
#             self.log.debug('Returned value: {}'.format(ret))
