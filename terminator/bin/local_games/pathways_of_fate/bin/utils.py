def is_float(num_str):
    try:
        float(num_str)
        return True

    except ValueError:
        return False


def proper(input_string):
    words = input_string.split()

    capitalized_words = [word.capitalize() for word in words]

    result = " ".join(capitalized_words)

    return result


def linearize_text(input_string, line_length):
    if not isinstance(input_string, str):
        input_string = str(input_string)

    if input_string.isspace():
        return [input_string]

    input_string = input_string.replace('\n', '').replace('\r', '')

    lines = []
    current_line = ''

    for index, char in enumerate(input_string):
        if len(current_line) >= line_length:
            if current_line[-1] not in (' ', '?', '!', ',', '.', '(', ')', '"', "'", '-', '\t'):
                current_line += f'{char}{input_string[index:input_string.index(" ")]}'

            else:
                lines.append(current_line)
                current_line = char

        else:
            current_line += char

    if current_line.strip() != '':
        lines.append(current_line)

    for line_index in range(len(lines)):
        lines[line_index] = lines[line_index].strip()

    return lines
