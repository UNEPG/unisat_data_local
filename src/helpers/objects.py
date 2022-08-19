from typing import Generic, Set, Dict, Tuple


def get_cls_attrs(obj: Generic, exclude_magics: bool = True, exclude_functions: bool = True) -> Set[str]:
    attrs_all = dir(obj)
    attrs_without_magics = [each for each in attrs_all if not each.startswith('__')]
    attrs_without_functions = [each for each in attrs_without_magics if not callable(getattr(obj, each))]
    if exclude_magics and exclude_functions:
        return set(attrs_without_magics).intersection(set(attrs_without_functions))
    elif exclude_magics:
        return set(attrs_all).intersection(set(attrs_without_magics))
    elif exclude_functions:
        return set(attrs_all).intersection(set(attrs_without_functions))
    return set(attrs_all)


def dict_without_keys(d: Dict, keys: Tuple):
    return {x: d[x] for x in d if x not in keys}
