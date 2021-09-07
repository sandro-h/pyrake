import re
from bs4 import Tag, NavigableString


def parse_pipe(term):  # pylint: disable=too-many-return-statements
    if term.startswith('@'):
        return attribute_pipe(term[1:])
    if term.startswith('till '):
        return till_pipe(term[term.index(' ') + 1:].strip())
    if term.startswith('select '):
        return select_pipe(term[term.index(' ') + 1:].strip())
    if term.startswith('replace '):
        parts = term.split(' ')
        return replace_pipe(parts[1], parts[2] if len(parts) > 2 else "")
    if term == 'text':
        return text_pipe()
    if term == 'textonly':
        return textonly_pipe()
    if term == 'next':
        return next_pipe()
    if term == 'prev':
        return prev_pipe()
    if term == 'trim':
        return trim_pipe()
    if term.startswith('helper'):
        return helper_pipe(term[term.index(' ') + 1:].strip())
    raise Exception(f"Unknown pipe '{term}'")


def attribute_pipe(attr):
    return make_pipe(lambda ele: ele.attrs.get(attr))


def text_pipe():
    return make_pipe(text)


def text(ele):
    return trim(" ".join(ele.stripped_strings))


def textonly_pipe():
    def textonly(ele):
        direct_strings = [
            c.string for c in ele.children if isinstance(c, NavigableString)
        ]
        return trim(''.join(direct_strings))

    return make_pipe(textonly)


def till_pipe(substr):
    def till(val):
        str_val = str(val)
        if substr not in str_val:
            return str_val
        return str_val[0:str_val.index(substr)]

    return make_pipe(till)


def next_pipe():
    # gotta deal with sibling text nodes
    def next_sibling_tag(ele):
        for sib in ele.next_siblings:
            if isinstance(sib, Tag):
                return sib
        return None

    return make_pipe(next_sibling_tag)


def prev_pipe():
    # gotta deal with sibling text nodes
    def previous_sibling_tag(ele):
        for sib in ele.previous_siblings:
            if isinstance(sib, Tag):
                return sib
        return None

    return make_pipe(previous_sibling_tag)


def select_pipe(selector):
    def select(ele):
        found = ele.select(selector)
        return found[0] if found else None

    return make_pipe(select)


def trim_pipe():
    return make_pipe(trim)


def trim(string):
    if string is None:
        return None
    return re.sub(r'(\s+)|&nbsp;|\u00a0', ' ', string).strip()


def replace_pipe(search, replace):
    replace = re.sub(r'\$([0-9])', r'\\\1', replace)
    return make_pipe(lambda val: re.sub(search, replace, val))


def helper_pipe(fname):
    def run_helper_func(pipe_input, context):
        helper_locals = {"input": pipe_input, "output": None}
        exec(context["helpers"][fname], {}, helper_locals)  # pylint: disable=exec-used
        return helper_locals["output"]

    return make_pipe(run_helper_func, requires_context=True)


def make_pipe(func, handles_null=False, requires_context=False):
    return {
        'func': func,
        'handles_null': handles_null,
        'requires_context': requires_context
    }
