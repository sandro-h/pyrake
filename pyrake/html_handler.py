from bs4 import BeautifulSoup
from pyrake.html_pipes import parse_pipe, text


def parse_string_term(term):
    parts = term.split('|')
    return {
        'selector': parts[0].strip(),
        'pipes': [parse_pipe(p.strip()) for p in parts[1:]]
    }


def parse_list_term(term):
    return term


def parse_html(html):
    return BeautifulSoup(html, features="lxml")


def evaluate_scalar_term(term, cursor, context):
    selector = term['selector']
    if selector == '.':
        ele = cursor
    else:
        found = cursor.select(selector)
        ele = found[0] if found else None

    return apply_pipes(ele, term['pipes'], context)


def apply_pipes(ele, pipes, context):
    cur = ele
    for pipe in pipes:
        if cur is not None or pipe['handles_null']:
            if pipe['requires_context']:
                cur = pipe['func'](cur, context)
            else:
                cur = pipe['func'](cur)

    if cur is None:
        return ''
    if isinstance(cur, str):
        return cur
    return text(cur)


def evaluate_list_term(term, cursor):
    return cursor.select(term)


TEMPLATE_PARSER_CONFIG = {
    'parse_string_term': parse_string_term,
    'parse_list_term': parse_list_term
}

EVALUATION_CONFIG = {
    'evaluate_scalar_term': evaluate_scalar_term,
    'evaluate_list_term': evaluate_list_term,
    'helpers': {}
}
