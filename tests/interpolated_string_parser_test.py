from pyrake.interpolated_string_parser import parse_interpolated_string


def test_simple():
    parsed = parse_interpolated_string('hello $(world)!')

    assert len(parsed) == 1
    assert parsed[0] == {
        'start': 6,
        'end': 13,
        'term': 'world',
        'var_name': '',
    }


def test_multiple():
    parsed = parse_interpolated_string('hello $(world), what is your $(name)!')

    assert len(parsed) == 2
    assert parsed[0] == {
        'start': 6,
        'end': 13,
        'term': 'world',
        'var_name': '',
    }
    assert parsed[1] == {
        'start': 29,
        'end': 35,
        'term': 'name',
        'var_name': '',
    }


def test_variable_name():
    parsed = parse_interpolated_string('hello $var1(world)!')

    assert len(parsed) == 1
    assert parsed[0] == {
        'start': 6,
        'end': 17,
        'term': 'world',
        'var_name': 'var1',
    }


def test_mixed_brackets():
    parsed = parse_interpolated_string('hello $(world), what is your ${name}!')

    assert len(parsed) == 2
    assert parsed[0] == {
        'start': 6,
        'end': 13,
        'term': 'world',
        'var_name': '',
    }
    assert parsed[1] == {
        'start': 29,
        'end': 35,
        'term': 'name',
        'var_name': '',
    }


def test_ignore_dollar_without_brackets():
    parsed = parse_interpolated_string(
        'hello $somethingelse, what is your ${name}!')

    assert len(parsed) == 1
    assert parsed[0] == {
        'start': 35,
        'end': 41,
        'term': 'name',
        'var_name': '',
    }


def test_term_after_invalid_dollar():
    parsed = parse_interpolated_string('hello $invalid$(var)')

    assert len(parsed) == 1
    assert parsed[0] == {
        'start': 14,
        'end': 19,
        'term': 'var',
        'var_name': '',
    }


def test_half_open_term():
    parsed = parse_interpolated_string('hello $(, what is your $(name)!')

    assert len(parsed) == 1
    assert parsed[0] == {
        'start': 6,
        'end': 29,
        'term': ', what is your $(name',
        'var_name': '',
    }


def test_other_brackets_in_term():
    parsed = parse_interpolated_string(
        'hello $(world{xyz}), what is your ${name:eq(0)}!')

    assert len(parsed) == 2
    assert parsed[0] == {
        'start': 6,
        'end': 18,
        'term': 'world{xyz}',
        'var_name': '',
    }
    assert parsed[1] == {
        'start': 34,
        'end': 46,
        'term': 'name:eq(0)',
        'var_name': '',
    }