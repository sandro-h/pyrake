from pyrake.template_primitives import is_scalar, is_dict, is_list, is_scalar_part_interpolation, is_scalar_part_literal

DEFAULT_CONTEXT = {
    'evaluate_scalar_term': lambda term, cursor: cursor[term],
    'evaluate_list_term': lambda term, cursor: cursor[term]
}


def evaluate_template(template, cursor, context=None):
    context = context or DEFAULT_CONTEXT
    if is_dict(template):
        return evaluate_dict(template, cursor, context)

    if is_list(template):
        return evaluate_list(template, cursor, context)

    if is_scalar(template):
        return evaluate_scalar(template, cursor, context)

    raise Exception(f"Unknown template type {template}")


def evaluate_dict(dct, cursor, context):
    return {
        k: evaluate_template(v, cursor, context)
        for (k, v) in dct['fields'].items()
    }


def evaluate_list(lst, cursor, context):
    list_of_lists = [
        evaluate_list_group(g, cursor, context) for g in lst['groups']
    ]
    return [item for sub_list in list_of_lists for item in sub_list]


def evaluate_list_group(group, cursor, context):
    list_cursors = []
    if group['term'] is None:
        # No each declaration, just use the current item for the items inside the array.
        list_cursors = [cursor]
    else:
        try:
            list_cursors = context['evaluate_list_term'](group['term'], cursor)
        except Exception as exc:  # pylint: disable=broad-except
            return [eval_error(exc)]

    return [
        evaluate_template(i, c, context) for c in list_cursors
        for i in group['items']
    ]


def evaluate_scalar(scalar, cursor, context):
    res = ''
    for part in scalar['parts']:
        try:
            res += evaluate_scalar_part(part, cursor, context)
        except Exception as exc:  # pylint: disable=broad-except
            res += eval_error(exc)

    try:
        if scalar.get('convert_to') == int:
            return int(res)
        if scalar.get('convert_to') == float:
            return float(res)
        if scalar.get('convert_to') == bool:
            return res.lower() == 'true'
    except Exception as exc:  # pylint: disable=broad-except
        return eval_error(exc)
    return res


def evaluate_scalar_part(part, cursor, context):
    if is_scalar_part_literal(part):
        return str(part['value'])
    if is_scalar_part_interpolation(part):
        # TODO var_name is not handled right now
        return str(context['evaluate_scalar_term'](part['term'], cursor))

    raise Exception(f"Unknown scalar part {part}")


def eval_error(exc):
    return f"$(err: {exc.__class__.__name__}: {exc})"
