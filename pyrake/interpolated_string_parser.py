def parse_interpolated_string(string):
    parsed = []

    in_dollar = False
    in_term = False
    var_name = ''
    term = ''
    left_bracket_char = None
    start = -1

    string_len = len(string)
    k = 0
    while k < string_len:
        char = string[k]
        if in_term:
            if is_right_bracket(char, left_bracket_char):
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
                term += char
        elif in_dollar:
            # Check if variable
            if is_variable_char(char):
                var_name += char
            elif is_left_bracket(char):
                in_term = True
                in_dollar = False
                left_bracket_char = char
                term = ''
            else:
                # Invalid variable name, give up for this potential term.
                in_dollar = False
                if char == '$':
                    # Invalid char was another dollar, so we have to analyze
                    # the potential term
                    k -= 1
        elif char == '$':
            in_dollar = True
            var_name = ''
            start = k
        k += 1

    return parsed


def is_right_bracket(char, left_bracket_char):
    return (char == ')'
            and left_bracket_char == '(') or (char == '}'
                                              and left_bracket_char == '{')


def is_left_bracket(char):
    return char in ('(', '{')


def is_variable_char(char):
    return char.isalnum()
