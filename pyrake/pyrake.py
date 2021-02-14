import re
import urllib.request
from pyrake.evaluator import evaluate_template
from pyrake.template_parser import parse_template, is_dict
from pyrake.html_handler import EVALUATION_CONFIG, TEMPLATE_PARSER_CONFIG, parse_html


def run(definitions, cache=None):
    execution = {
        'output': None,
        'cache': cache or {},
        'used_cache_for_all': True,
        'props': {}
    }
    k = 0
    for definition in definitions:
        run_definition(definition, k == len(definitions) - 1, execution)
        k += 1

    return {
        'output': execution['output'],
        'used_cache_for_all': execution['used_cache_for_all'],
        'cache': execution['cache']
    }


def run_definition(definition, is_last, execution):
    template = parse_template(definition['template'],
                              config=TEMPLATE_PARSER_CONFIG)
    (resp, from_cache) = fetch(definition, execution)
    html = parse_html(resp)
    output = evaluate_template(template, html, context=EVALUATION_CONFIG)
    if not from_cache:
        execution['used_cache_for_all'] = False

    if is_last:
        execution['output'] = output
    else:
        if is_dict(output):
            for (k, val) in output.items():
                execution['props'][k] = str(val)
        else:
            print(
                f"WARN: Can't use output as props, not a dict (output={output})"
            )


def fetch(definition, execution):
    url = resolve_props(definition['url'], execution['props'])

    if url.startswith('str://'):
        return (url[6:], False)

    if url.startswith('file://'):
        with open(url[7:], 'r') as file:
            return (file.read(), False)

    cache = execution['cache']
    if url in cache:
        return (cache[url], True)

    response = download(url)
    cache[url] = response
    return (response, False)


def download(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        return response.read().decode()


def resolve_props(string, props):
    i = 0
    res = ''
    for match in re.finditer(r'@(\w+)@', string):
        if i < match.start():
            res += string[i:match.start()]

        val = props.get(match.group(1))
        if val is not None:
            res += val
        else:
            res += string[match.start():match.end()]

        i = match.end()

    if i < len(string):
        res += string[i:]

    return res
