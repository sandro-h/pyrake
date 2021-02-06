from enum import Enum


class TemplateType(Enum):
    STRING = 1
    INTERPOLATION = 2
    LITERAL = 3
    LIST = 4
    DICT = 5


def create_string(parts):
    return {'type': TemplateType.STRING, 'parts': parts}


def create_literal(value):
    return {'type': TemplateType.LITERAL, 'value': value}


def create_interpolation(term, var_name=''):
    return {
        'type': TemplateType.INTERPOLATION,
        'term': term,
        'var_name': var_name
    }


def create_list(groups):
    return {'type': TemplateType.LIST, 'groups': groups}


def create_dict(fields):
    return {'type': TemplateType.DICT, 'fields': fields}
