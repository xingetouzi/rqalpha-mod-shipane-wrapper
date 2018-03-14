def __get_manager_id__():
    from rqalpha.environment import Environment
    env = Environment.get_instance()
    manage_id = env.strategy_loader.get_manager_id()
    return manage_id


def __wrapper_init__(manager_id):
    from shipane_sdk.ricequant import manager
    from functools import wraps

    def decorator(func):
        @wraps(func)
        def wrapped(context):
            context._manager = manager.RiceQuantStrategyManagerFactory(context).create(manager_id)
            return func(context)

        return wrapped

    return decorator


def __wrapper_before_trading__(manage_id):
    from shipane_sdk.ricequant import manager
    from functools import wraps

    def decorator(func):
        @wraps(func)
        def wrapped(context):
            context._manager = manager.RiceQuantStrategyManagerFactory(context).create(manage_id)
            return func(context)

        return wrapped

    return decorator


def __wrapper_handle_bar__(func):
    from functools import wraps

    @wraps(func)
    def wrapped(context, bar_dict):
        try:
            return func(context, bar_dict)
        finally:
            context._manager.work()

    return wrapped

init = __wrapper_init__(__get_manager_id__())(init)
before_trading = __wrapper_before_trading__(__get_manager_id__())(before_trading)
handle_bar = __wrapper_handle_bar__(handle_bar)
del __get_manager_id__
del __wrapper_init__
del __wrapper_before_trading__
del __wrapper_handle_bar__

