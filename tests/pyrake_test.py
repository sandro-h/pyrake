from pyrake.pyrake import resolve_props, run, download
from .test_util import run_with_http_server


def test_resolve_props():
    cases = [['hello=@param@', {
        'param': 'world'
    }, 'hello=world'],
             [
                 'hello=@unknown_param@', {
                     'param': 'world'
                 }, 'hello=@unknown_param@'
             ],
             [
                 'hello=@param@&aba=@n@', {
                     'param': 'world',
                     'n': '123'
                 }, 'hello=world&aba=123'
             ]]
    for case in cases:
        resolved = resolve_props(case[0], case[1])
        assert resolved == case[2]


def test_run():
    definitions = [{
        'url': """str://
<li><div id="name">Frank</div><div id="age">30</div></li>
<li><div id="name">Zappa</div><div id="age">41</div></li>
<li><div id="name">Caroline</div><div id="age">59</div></li>
""",
        'template': ['$each li', {
            'name': '$(#name)',
            'age': '$(#age)'
        }]
    }]

    output = run(definitions)['output']
    assert output == [{
        'name': 'Frank',
        'age': '30'
    }, {
        'name': 'Zappa',
        'age': '41'
    }, {
        'name': 'Caroline',
        'age': '59'
    }]


def test_download():
    def test(base_url):
        resp = download(base_url)
        assert resp == '<div>hello</div>'

    run_with_http_server(test, '<div>hello</div>')


def test_run_with_download():
    def test(base_url):
        definitions = [{
            'url': base_url,
            'template': ['$each li', {
                'name': '$(#name)',
                'age': '$(#age)'
            }]
        }]

        res = run(definitions)
        assert res['output'] == [{
            'name': 'Frank',
            'age': '30'
        }, {
            'name': 'Zappa',
            'age': '41'
        }, {
            'name': 'Caroline',
            'age': '59'
        }]
        assert res['cache'][base_url] == """str://
<li><div id="name">Frank</div><div id="age">30</div></li>
<li><div id="name">Zappa</div><div id="age">41</div></li>
<li><div id="name">Caroline</div><div id="age">59</div></li>
"""

    run_with_http_server(
        test, """str://
<li><div id="name">Frank</div><div id="age">30</div></li>
<li><div id="name">Zappa</div><div id="age">41</div></li>
<li><div id="name">Caroline</div><div id="age">59</div></li>
""")
