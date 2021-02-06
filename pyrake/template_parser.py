EACH_SELECTOR = "$each "


def parse_template(input):
    parse_any(input)


def parse_any(any):
    if is_dict(any):
        parse_dict(any)
    elif is_list(any):
        parse_list(any)
    elif is_scalar(any):
        parse_scalar(any)
    else:
        raise Exception(f"Unknown type {type(any)}")


def is_dict(any):
    return isinstance(any, dict)


def is_list(any):
    return isinstance(any, list)


def is_scalar(any):
    return (isinstance(any, str) or isinstance(any, int)
            or isinstance(any, float) or isinstance(any, bool))


def parse_dict(d):
    return {'type': 'dict', 'fields': {k: parse_any(v) for k, v in d}}


def parse_list(l):
    groups = []
    items = []
    term = None
    for ele in l:
        if is_each_selector(ele):
            if len(items) > 0:
                groups.append({'term': term, 'items': items})
            term = str(ele)[len(EACH_SELECTOR):]
            items = []
        else:
            items.append(parse_any(ele))

    if len(items) > 0:
        groups.append({'term': term, 'items': items})

    return {'type': 'list', 'groups': groups}


def is_each_selector(any):
    return is_scalar(any) and str(any).startswith(EACH_SELECTOR)


# def parse_scalar(s):
