from functools import wraps


def is_cmd_allowed(fisallowed):
    def is_allowed(func):
        @wraps(func)
        def rfunc(self, *args, **keys):
            if getattr(self, fisallowed)():
                return func(self, *args, **keys)
            else:
                raise Exception("Command not allowed")
        return rfunc
    return is_allowed
