
def bind(meth, func):
    obj = meth.__self__
    name = meth.__func__.__name__
    setattr(obj, name, func.__get__(obj, obj.__class__))
