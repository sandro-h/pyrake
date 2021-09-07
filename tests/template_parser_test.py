from pyrake.template_parser import parse_template
from pyrake.template_primitives import TemplateType


def test_dict():
    parsed = parse_template({'foo': '$(bar)'})

    assert parsed == {
        'type': TemplateType.DICT,
        'fields': {
            'foo': {
                'type': TemplateType.SCALAR,
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
                'type': TemplateType.SCALAR,
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
                'type': TemplateType.SCALAR,
                'parts': [{
                    'type': TemplateType.INTERPOLATION,
                    'term': 'bar',
                    'var_name': ''
                }]
            }]
        }, {
            'term': 'gob',
            'items': [{
                'type': TemplateType.SCALAR,
                'parts': [{
                    'type': TemplateType.LITERAL,
                    'value': 'hi'
                }]
            }]
        }]
    }


def test_scalar_conversion():
    cases = [
        ('$int:$(bar)', int),
        ('$float:$(bar)', float),
        ('$bool:$(bar)', bool),
    ]

    for case in cases:
        parsed = parse_template(case[0])

        assert parsed == {
            'type': TemplateType.SCALAR,
            'convert_to': case[1],
            'parts': [{
                'type': TemplateType.INTERPOLATION,
                'term': 'bar',
                'var_name': '',
            }]
        }


def test_scalar():
    parsed = parse_template(
        '$(td.title a)<br/>Source: $(td.title a | @href)<br/><a href="https://news.ycombinator.com/item?id=$(. | @id)">Comments</a>'
    )

    assert parsed == {
        'type': TemplateType.SCALAR,
        "parts": [
            {
                'type': TemplateType.INTERPOLATION,
                'term': 'td.title a',
                'var_name': '',
            },
            {
                'type': TemplateType.LITERAL,
                'value': '<br/>Source: '
            },
            {
                'type': TemplateType.INTERPOLATION,
                'term': 'td.title a | @href',
                'var_name': '',
            },
            {
                'type': TemplateType.LITERAL,
                'value': '<br/><a href=\"https://news.ycombinator.com/item?id='
            },
            {
                'type': TemplateType.INTERPOLATION,
                'term': '. | @id',
                'var_name': '',
            },
            {
                'type': TemplateType.LITERAL,
                'value': '">Comments</a>'
            },
        ]
    }
