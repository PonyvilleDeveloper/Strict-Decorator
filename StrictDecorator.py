from types import GenericAlias as Generic
from typing import get_origin, get_args

def strict(func):
    assert len(func.__annotations__) > 0, "Don't use @strict decorator on functions without annotations"
    arg_types = {
        arg_name: (
            [type_info] if (type(type_info) is Generic or type(type_info) is type)
            else list(type_info.__args__) if hasattr(type_info, "__args__")
            else type(type_info)
        )
        for arg_name, type_info in func.__annotations__.items()
    }

    def check_single(var, expected_type):
        origin = get_origin(expected_type)
        args = get_args(expected_type)
        if origin is None:
            return isinstance(var, expected_type)
        else:
            if not isinstance(var, origin): return False
            else:
                if origin is list:
                    return True if not args else all(check(item, args[0]) for item in var)
                elif origin is dict:
                    return True if not args or len(args) != 2 else all(check(k, args[0]) and check(v, args[1]) for k, v in var.items())
                elif origin is set:
                    return True if not args else all(check(item, args[0]) for item in var)
                elif origin is tuple:
                    return True if not args else (False if len(args) != len(var) else all(check(item, arg_type) for item, arg_type in zip(var, args)))
        return False
    
    def check(value, types, errmsg):
        if not any([check_single(value, t) for t in types]):
            real_type_name = type(value).__name__
            req_types_names = [t.__name__ if not isinstance(t, Generic) else str(t) for t in types]
            raise TypeError(errmsg + f" func must be {' or '.join(req_types_names)}, not {real_type_name}")

    def strict_decorator(*args, **kwargs):
        arg_vals = {
            arg_name: arg_value
            for arg_name, arg_value in list(zip(
                func.__annotations__.keys(), args[1 if len(args) > len(arg_types) - ("return" in arg_types) else 0:]
            ))
        }
        arg_vals.update(kwargs) 

        for arg_name in arg_vals.keys():
            check(arg_vals[arg_name], arg_types[arg_name], f'Arg "{arg_name}" of "{func.__name__}"')
        
        res = func(*args, **kwargs)
        if "return" in arg_types:
            check(res, arg_types["return"], f'Result of "{func.__name__}"')

        return res
    
    return strict_decorator

if __name__ == "__main__":
    @strict
    def foo(a: int): pass
    foo(9) #Ok

    class test:
        @strict
        def foo(self, a: int): pass

    t = test()
    t.foo('8') #TypeError