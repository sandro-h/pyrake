from pyrake.template_parser import parse_template
from pyrake.evaluator import evaluate_template


def test_evaluate_scalar_literal():
    template = parse_template('hello')

    res = evaluate_template(template, None)

    assert res == 'hello'


def test_evaluate_scalar_term():
    data = {'bar': 'hello world'}
    template = parse_template('$(bar)')

    res = evaluate_template(template, data)

    assert res == 'hello world'


def test_evaluate_scalar_mixed():
    data = {'greeting': 'hello', 'name': 'san'}
    template = parse_template('$(greeting) world, $(name)!')

    res = evaluate_template(template, data)

    assert res == 'hello world, san!'


def test_evaluate_scalar_error():
    data = {'bar': 'hello world'}
    template = parse_template('other text $(non_existent_key)hello world')

    res = evaluate_template(template, data)

    assert res == "other text $(err: KeyError: 'non_existent_key')hello world"


def test_evaluate_scalar_to_int():
    data = {'bar': 777}
    template = parse_template('$int:$(bar)')

    res = evaluate_template(template, data)

    assert res == 777


def test_evaluate_scalar_to_float():
    data = {'bar': 777.7}
    template = parse_template('$float:$(bar)')

    res = evaluate_template(template, data)

    assert res == 777.7


def test_evaluate_scalar_to_true():
    data = {'bar': True}
    template = parse_template('$bool:$(bar)')

    res = evaluate_template(template, data)

    assert isinstance(res, bool)
    assert res


def test_evaluate_scalar_to_false():
    data = {'bar': False}
    template = parse_template('$bool:$(bar)')

    res = evaluate_template(template, data)

    assert isinstance(res, bool)
    assert not res


def test_evaluate_dict():
    data = {'bar': 'hello world'}
    template = parse_template({'field1': 'hi', 'field2': '$(bar)'})

    res = evaluate_template(template, data)

    assert res == {'field1': 'hi', 'field2': 'hello world'}


def test_evaluate_dict_empty():
    data = {}
    template = parse_template({})

    res = evaluate_template(template, data)

    assert res == {}


def test_evaluate_list():
    data = {
        'lelist': [
            {
                'var': 0
            },
            {
                'var': 1
            },
            {
                'var': 2
            },
        ]
    }

    template = parse_template(['$each lelist', 'hey$(var)'])

    res = evaluate_template(template, data)

    assert res == ['hey0', 'hey1', 'hey2']


def test_evaluate_list_multi_groups():
    data = {
        'lelist': [
            {
                'var': 0
            },
            {
                'var': 1
            },
        ],
        'leotherlist': [
            {
                'foo': 'abc'
            },
            {
                'foo': 'def'
            },
        ]
    }

    template = parse_template(
        ['$each lelist', 'hey$(var)', '$each leotherlist', 'omg$(foo)'])

    res = evaluate_template(template, data)

    assert res == ['hey0', 'hey1', 'omgabc', 'omgdef']


def test_evaluate_nested_list():
    data = {
        'outerlist': [{
            'innerlist': [
                {
                    'var': '0.0'
                },
                {
                    'var': '0.1'
                },
            ]
        }, {
            'innerlist': [
                {
                    'var': '1.0'
                },
                {
                    'var': '1.1'
                },
            ]
        }],
    }

    template = parse_template(
        ['$each outerlist', ['$each innerlist', '$(var)']])

    res = evaluate_template(template, data)

    assert res == [['0.0', '0.1'], ['1.0', '1.1']]


def test_evaluate_list_without_group():
    data = {'var': '0'}

    template = parse_template(['hey$(var)'])

    res = evaluate_template(template, data)

    assert res == ['hey0']


def test_evaluate_list_error():
    data = {}

    template = parse_template(['$each lelist', 'hey$(var)'])

    res = evaluate_template(template, data)

    assert res == ["$(err: KeyError: 'lelist')"]


def test_evaluate_list_error_in_one_group():
    data = {
        'leotherlist': [
            {
                'foo': 'abc'
            },
            {
                'foo': 'def'
            },
        ]
    }

    template = parse_template(
        ['$each lelist', 'hey$(var)', '$each leotherlist', 'omg$(foo)'])

    res = evaluate_template(template, data)

    assert res == ["$(err: KeyError: 'lelist')", 'omgabc', 'omgdef']
