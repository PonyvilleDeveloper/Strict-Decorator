def strict(func):
    assert len(func.__annotations__) > 0, "Don't use @strict decorator on functions without annotations"
    arg_types = {
        arg_name: list(map(
            lambda t: type(t) if not isinstance(t, type) else t,
            list(type_info.__args__) if hasattr(type_info, "__args__") else [type_info]
        ))
        for arg_name, type_info in func.__annotations__.items()
    }

    def strict_decorator(*args, **kwargs):
        arg_vals = {
            arg_name: arg_value
            for arg_name, arg_value in list(zip(
                func.__annotations__.keys(), args[1 if len(args) > len(arg_types) - ("return" in arg_types) else 0:]
            ))
        }
        arg_vals.update(kwargs)

        for arg_name in arg_vals.keys():
            if(type(arg_vals[arg_name]) not in arg_types[arg_name]):
                real_type_name = type(arg_vals[arg_name]).__name__
                req_types_names = [t.__name__ for t in arg_types[arg_name]]
                raise TypeError(f'Arg "{arg_name}" of "{func.__name__}" func must be {" or ".join(req_types_names)}, not {real_type_name}')
        
        res = func(*args, **kwargs)
        if("return" in arg_types and type(res) not in arg_types["return"]):
            real_type_name = type(res).__name__
            req_types_names = [t.__name__ for t in arg_types["return"]]
            raise TypeError(f'Result of "{func.__name__}" func must be {" or ".join(req_types_names)}, not {real_type_name}')

        return res
    
    return strict_decorator