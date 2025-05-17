try:
    from yell import yell  # try real package
except ImportError:
    def yell(*args, **kwargs): pass
