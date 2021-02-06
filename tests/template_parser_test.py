from pyrake.template_parser import parse_template
from pyrake.template_primitives import TemplateType


def test_dict():
    parsed = parse_template({'foo': '$(bar)'})

    assert parsed == {
        'type': TemplateType.DICT,
        'fields': {
            'foo': {
                'type': TemplateType.STRING,
                'parts': [{
                    'type': TemplateType.INTERPOLATION,
                    'term': 'bar',
                    'var_name': ''
                }]
            }
        }
    }


def test_list():
    parsed = parse_template(['$each foo', '$(bar)'])

    assert parsed == {
        'type': TemplateType.LIST,
        'groups': [{
            'term': 'foo',
            'items': [{
                'type': TemplateType.STRING,
                'parts': [{
                    'type': TemplateType.INTERPOLATION,
                    'term': 'bar',
                    'var_name': ''
                }]
            }]
        }]
    }


def test_multi_list():
    parsed = parse_template(['$each foo', '$(bar)', '$each gob', 'hi'])

    assert parsed == {
        'type': TemplateType.LIST,
        'groups': [{
            'term': 'foo',
            'items': [{
                'type': TemplateType.STRING,
                'parts': [{
                    'type': TemplateType.INTERPOLATION,
                    'term': 'bar',
                    'var_name': ''
                }]
            }]
        }, {
            'term': 'gob',
            'items': [{
                'type': TemplateType.STRING,
                'parts': [{
                    'type': TemplateType.LITERAL,
                    'value': 'hi'
                }]
            }]
        }]
    }
