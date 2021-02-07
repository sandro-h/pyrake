from pyrake.template_parser import parse_template
from pyrake.evaluator import evaluate_template
from pyrake.html_handler import EVALUATION_CONFIG, TEMPLATE_PARSER_CONFIG, parse_html


def test_eval_current_text():
    html = parse_html('hello there more stuff')
    template = parse_template({'foo': '$(.)'}, config=TEMPLATE_PARSER_CONFIG)

    res = evaluate_template(template, html, context=EVALUATION_CONFIG)

    assert res == {'foo': 'hello there more stuff'}


def test_eval_nested_text():
    html = parse_html("""
    <div>
        <span class="foo">hello</span>
    </div>
    """)
    template = parse_template({'foo': '$(.foo)'},
                              config=TEMPLATE_PARSER_CONFIG)

    res = evaluate_template(template, html, context=EVALUATION_CONFIG)

    assert res == {'foo': 'hello'}


def test_eval_attribute_pipe():
    html = parse_html('<div some-attr="hello" />')
    template = parse_template({'foo': '$(div | @some-attr)'},
                              config=TEMPLATE_PARSER_CONFIG)

    res = evaluate_template(template, html, context=EVALUATION_CONFIG)

    assert res == {'foo': 'hello'}


def test_eval_till_pipe():
    html = parse_html('<div>hello there more stuff</div>')
    template = parse_template({'foo': '$(div | text | till there)'},
                              config=TEMPLATE_PARSER_CONFIG)

    res = evaluate_template(template, html, context=EVALUATION_CONFIG)

    assert res == {'foo': 'hello '}


def test_eval_till_pipe_no_match():
    html = parse_html('<div>hello there more stuff</div>')
    template = parse_template({'foo': '$(div | text | till blablabla)'},
                              config=TEMPLATE_PARSER_CONFIG)

    res = evaluate_template(template, html, context=EVALUATION_CONFIG)

    assert res == {'foo': 'hello there more stuff'}


def test_eval_next_pipe():
    html = parse_html("""
    <p>first sibling</p>
    <p>second sibling</p>
        """)
    template = parse_template({'foo': '$(p | next)'},
                              config=TEMPLATE_PARSER_CONFIG)

    res = evaluate_template(template, html, context=EVALUATION_CONFIG)

    assert res == {'foo': 'second sibling'}


def test_eval_prev_pipe():
    html = parse_html("""
    <p>first sibling</p>
    <p class="second">second sibling</p>
        """)
    template = parse_template({'foo': '$(p.second | prev)'},
                              config=TEMPLATE_PARSER_CONFIG)

    res = evaluate_template(template, html, context=EVALUATION_CONFIG)

    assert res == {'foo': 'first sibling'}


def test_select_pipe():
    html = parse_html("""
    <div>
        <p>
            <span class="two">wrong two span</span>
        </p>
        <p>
            <span class="one">one span</span>
            <span class="two">two span</span>
        </p>
    </div>
        """)
    template = parse_template({'foo': '$(p | next | select .two)'},
                              config=TEMPLATE_PARSER_CONFIG)

    res = evaluate_template(template, html, context=EVALUATION_CONFIG)

    assert res == {'foo': 'two span'}


def test_textonly_pipe():
    html = parse_html("""
    <div>
        <p>other text</p>
        text of
        <p>more text</p>
        interest
    </div>
        """)
    template = parse_template({'foo': '$(div | textonly)'},
                              config=TEMPLATE_PARSER_CONFIG)

    res = evaluate_template(template, html, context=EVALUATION_CONFIG)

    assert res == {'foo': 'text of interest'}


def test_trim_pipe():
    html = parse_html('<div> hello &nbsp;   world    </div>')
    template = parse_template({'foo': '$(div | text | trim)'},
                              config=TEMPLATE_PARSER_CONFIG)

    res = evaluate_template(template, html, context=EVALUATION_CONFIG)

    assert res == {'foo': 'hello world'}


def test_replace_pipe():
    html = parse_html('<div>hello there more stuff</div>')
    template = parse_template({'foo': '$(div | text | replace there world)'},
                              config=TEMPLATE_PARSER_CONFIG)

    res = evaluate_template(template, html, context=EVALUATION_CONFIG)

    assert res == {'foo': 'hello world more stuff'}


def test_replace_groups_pipe():
    html = parse_html('<div>hello there more stuff</div>')
    template = parse_template(
        {'foo': '${div | text | replace .*(there).* $1}'},
        config=TEMPLATE_PARSER_CONFIG)

    res = evaluate_template(template, html, context=EVALUATION_CONFIG)

    assert res == {'foo': 'there'}


def test_replace_with_empty():
    html = parse_html('<div>CHF 1745.-</div>')
    template = parse_template({'foo': '$(div | text | replace [^0-9])'},
                              config=TEMPLATE_PARSER_CONFIG)

    res = evaluate_template(template, html, context=EVALUATION_CONFIG)

    assert res == {'foo': '1745'}


def test_propagate_null_in_pipes():
    html = parse_html('<div>bla bla</div>')
    template = parse_template(
        {'foo': '$(#unknown | @some-attr | trim | till bla)'},
        config=TEMPLATE_PARSER_CONFIG)

    res = evaluate_template(template, html, context=EVALUATION_CONFIG)

    assert res == {'foo': ''}
