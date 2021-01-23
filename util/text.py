def wrap_text(text, line_length):
    """Wrap a string of text based on the given line length.

    Words that are longer than the line length will be split with a dash.

    Arguments:
        text (Str): the text that will be wrapped
        line_length (Int): the max length of a line
    Returns:
        List [Str]
    """
    words = text.split()
    lines = []
    while len(words) > 0:
        line = ""
        while len(line) < line_length and len(words) > 0:
            characters_left = line_length - len(line)
            if characters_left >= len(words[0]):
                word = words.pop(0)
            else:
                if len(line) == 0:
                    # Word is too long for line, split word across lines
                    length = line_length - 1  # Give room for the dash
                    word, words[0] = (words[0][:length], words[0][length:])
                    word += "-"
                else:
                    break
            line = " ".join((line, word)).strip()
        lines.append(line)
    return lines