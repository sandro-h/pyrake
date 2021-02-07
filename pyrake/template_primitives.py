from enum import Enum


class TemplateType(Enum):
    SCALAR = 1
    INTERPOLATION = 2
    LITERAL = 3
    LIST = 4
    DICT = 5


def create_scalar(parts, type_conversion):
    scalar = {'type': TemplateType.SCALAR, 'parts': parts}
    if type_conversion is not None:
        scalar['convert_to'] = type_conversion
    return scalar


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


def is_dict(val):
    return val.get('type') == TemplateType.DICT


def is_list(val):
    return val.get('type') == TemplateType.LIST


def is_scalar(val):
    return val.get('type') == TemplateType.SCALAR


def is_scalar_part_literal(part):
    return part.get('type') == TemplateType.LITERAL


def is_scalar_part_interpolation(part):
    return part.get('type') == TemplateType.INTERPOLATION
