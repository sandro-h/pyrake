def parse_interpolated_string(str):
    parsed = []

    in_dollar = False
    in_term = False
    var_name = ''
    term = ''
    left_bracket_char = None
    start = -1

    ln = len(str)
    k = 0
    while k < ln:
        c = str[k]
        if in_term:
            if is_right_bracket(c, left_bracket_char):
                # Aaand done
                in_term = False
                term = {
                    'start': start,
                    'end': k,
                    'term': term,
                    'var_name': var_name.strip(),
                }
                parsed.append(term)
            else:
                term += c
        elif in_dollar:
            # Check if variable
            if is_variable_char(c):
                var_name += c
            elif is_left_bracket(c):
                in_term = True
                in_dollar = False
                left_bracket_char = c
                term = ''
            else:
                # Invalid variable name, give up for this potential term.
                in_dollar = False
                if c == '$':
                    # Invalid char was another dollar, so we have to analyze
                    # the potential term
                    k -= 1
        elif c == '$':
            in_dollar = True
            var_name = ''
            start = k
        k += 1

    return parsed


def is_right_bracket(c, left_bracket_char):
    return (c == ')'
            and left_bracket_char == '(') or (c == '}'
                                              and left_bracket_char == '{')


def is_left_bracket(c):
    return c == '(' or c == '{'


def is_variable_char(c):
    return c.isalnum()
