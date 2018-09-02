TOKEN_TYPE = 1
KEYWORD = 2
SYMBOL = 3
IDENTIFIER = 4
INT_CONST = 5
STRING_CONST = 6
CLASS = 7
METHOD = 8
FUNCTION = 9
CONSTRUCTOR = 10
INT = 11
BOOLEAN = 12
CHAR = 13
VOID = 14
VAR = 15
STATIC = 16
FIELD = 17
LET = 18
DO = 19
IF = 20
ELSE = 21
WHILE = 22
RETURN = 23
TRUE = 24
FALSE = 25
NULL = 26
THIS = 27

# Useful modification loop .. use outside of file.
# import parser.utils.token_types as token_types
# for key, value in sorted([(key, getattr(token_types, key)) for key in dir(token_types) if key[0] != "_"], key=lambda x: x[1]):
#         print(key, "=", value+1)
