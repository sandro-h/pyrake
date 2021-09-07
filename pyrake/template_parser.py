from pyrake.interpolated_string_parser import parse_interpolated_string
from pyrake.template_primitives import create_dict, create_list, create_literal, create_scalar, create_interpolation
EACH_SELECTOR = "$each "
DEFAULT_CONFIG = {
    'parse_string_term': lambda st: st,
    'parse_list_term': lambda st: st
}


def parse_template(val, config=None):
    config = config or DEFAULT_CONFIG
    return parse_any(val, config)


def parse_any(val, config):
    if is_dict(val):
        return parse_dict(val, config)
    if is_list(val):
        return parse_list(val, config)
    if is_scalar(val):
        return parse_scalar(val, config)

    raise Exception(f"Unknown type {type(val)}")


def is_dict(val):
    return isinstance(val, dict)


def is_list(val):
    return isinstance(val, list)


def is_scalar(val):
    return isinstance(val, (str, int, float, bool))


def parse_dict(dct, config):
    return create_dict({k: parse_any(v, config) for (k, v) in dct.items()})


def parse_list(lst, config):
    groups = []
    items = []
    term = None
    for ele in lst:
        if is_each_selector(ele):
            if items:
                groups.append({'term': term, 'items': items})
            term_str = str(ele)[len(EACH_SELECTOR):]
            term = config['parse_list_term'](term_str)
            items = []
        else:
            items.append(parse_any(ele, config))

    if items:
        groups.append({'term': term, 'items': items})

    return create_list(groups)


def is_each_selector(val):
    return is_scalar(val) and str(val).startswith(EACH_SELECTOR)


def parse_scalar(val, config):
    strval = str(val)

    # Type conversion
    type_conversion = None
    if strval.startswith('$') and ':' in strval:
        col_pos = strval.index(':')
        conv = strval[1:col_pos]
        if conv == 'int':
            type_conversion = int
        elif conv == 'float':
            type_conversion = float
        elif conv == 'bool':
            type_conversion = bool

        if type_conversion is not None:
            strval = strval[col_pos + 1:]

    # String parts
    interpolations = parse_interpolated_string(strval)
    parts = []
    k = 0
    for i in interpolations:
        if i['start'] > k:
            parts.append(create_literal(strval[k:i['start']]))

        term = config['parse_string_term'](i['term'])
        parts.append(create_interpolation(term, i['var_name']))
        k = i['end'] + 1

    if k < len(strval):
        parts.append(create_literal(strval[k:]))

    return create_scalar(parts, type_conversion)
