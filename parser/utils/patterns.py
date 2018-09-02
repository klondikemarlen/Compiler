import re

LINE_COMMENT = re.compile("//.*\n")  # // anything till end of string.
BLOCK_COMMENT_START = re.compile("/\*")  # /* anywhere in a string.
BLOCK_COMMENT = re.compile("/\*.*\*/", re.S)  # /* until */ matches over newlines.

# any of these keywords
KEYWORD = re.compile(
    'class|constructor|function|method|field|static|'
    'var|int|char|boolean|void|true|false|null|this|'
    'let|do|if|else|while|return'
)

# any of the following symbols. Hopefully I escaped the right ones :P
SYMBOL = re.compile(
    '[{}()\[\].,;+\-*/&|<>=~]'
)

# match constants up to 32767
INT_CONST = re.compile(
    '\d{1,4}|(\d{5}(?<=[0-3][0-2][0-7][0-6][0-7]))'
)

# " + any unicode character except " or newline + "
STRING_CONST = re.compile(
    '"(.(?<!"))*"'
)

# A sequence of letters, digits and underscore, not starting with a digit.
IDENTIFIER = re.compile(
    '[A-z_]\w*'
)

# Note that the extra ( ) are critical.
# noinspection RegExpDuplicateAlternationBranch
ALL_TERMINATORS = re.compile('({})|({})|({})|({})|({})'.format(KEYWORD.pattern, SYMBOL.pattern, INT_CONST.pattern, STRING_CONST.pattern, IDENTIFIER.pattern))


if __name__ == "__main__":
    assert SYMBOL.fullmatch("\\") is None
    assert SYMBOL.fullmatch("A") is None
    assert SYMBOL.fullmatch("/") is not None
    assert SYMBOL.fullmatch("{") is not None
    assert SYMBOL.fullmatch(",") is not None
    assert SYMBOL.fullmatch(".") is not None
    assert SYMBOL.fullmatch("|") is not None
    assert SYMBOL.fullmatch("~") is not None
    assert SYMBOL.fullmatch("]") is not None
    assert SYMBOL.fullmatch("(") is not None

    assert INT_CONST.fullmatch("9999") is not None
    assert INT_CONST.fullmatch("32767") is not None
    assert INT_CONST.fullmatch("32768") is None
    assert INT_CONST.fullmatch("32777") is None
    assert INT_CONST.fullmatch("32867") is None
    assert INT_CONST.fullmatch("33767") is None
    assert INT_CONST.fullmatch("42767") is None
    assert INT_CONST.fullmatch("5000000") is None

    assert STRING_CONST.fullmatch('"\n"') is None
    assert STRING_CONST.fullmatch('"') is None
    assert STRING_CONST.fullmatch('"sdf"fdsf"') is None
    assert STRING_CONST.fullmatch('"te;s.<t"') is not None

    assert IDENTIFIER.fullmatch('AB99_') is not None
    assert IDENTIFIER.fullmatch('_AB99') is not None
    assert IDENTIFIER.fullmatch('9AB99') is None
    assert IDENTIFIER.fullmatch('') is None
    assert IDENTIFIER.fullmatch(';.') is None

    keywords = KEYWORD.findall('class Main {')
    symbols = SYMBOL.findall('class Main {')
    ints = INT_CONST.findall('class Main {')
    strings = STRING_CONST.findall('class Main {')
    ids = IDENTIFIER.findall('class Main {')
    print(keywords)
    print(symbols)
    print(ints)
    print(strings)
    print(ids)
