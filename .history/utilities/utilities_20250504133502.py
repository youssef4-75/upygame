from .exceptions import MaximumCallsReachedError

def limit_calls(max_calls: int):
    def decorator(method):
        def wrapper(self, *args, **kwargs):
            # Create counter if it doesn't exist
            if not hasattr(self, '__method_call_counts'):
                self.__method_call_counts = {}

            # Initialize counter for this method
            method_name = method.__name__
            if method_name not in self.__method_call_counts:
                self.__method_call_counts[method_name] = 0

            # Check call count
            if self.__method_call_counts[method_name] >= max_calls:
                raise MaximumCallsReachedError(max_calls, method_name)

            # Increment and call
            self.__method_call_counts[method_name] += 1
            return method(self, *args, **kwargs)
        return wrapper
    return decorator

def loop_method(method):
    return method 

def init_method(method):
    return method 

def access_limit(name):
    def decorator(method):
        def wrapper(*arge, permission=None, **kwargs):
            if permission != name:
                raise Exception
            return method(*args, **kwargs)