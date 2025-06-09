from exceptions import MaximumCallsReachedError

def limit_calls(max_calls: int):
    def decorator(method):
        method.call_count = 0
        
        def wrapper(self, *args, **kwargs):
            if method.call_count >= max_calls:
                raise MaximumCallsReachedError(max_calls)
            method.call_count += 1
            return method(self, *args, **kwargs)
        return wrapper
    return decorator
