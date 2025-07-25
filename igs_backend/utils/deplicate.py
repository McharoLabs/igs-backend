def deprecated(func):
    def wrapper(*args, **kwargs):
        warnings.warn(
            f"Warning: The method {func.__name__} is deprecated and will be removed in future versions.",
            category=DeprecationWarning,
            stacklevel=2
        )
        return func(*args, **kwargs)
    return wrapper