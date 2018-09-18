import itertools

from .utils import token_types
from .utils import patterns


class JackTokenizer:
    """Removes all comments and white space from input stream and breaks it into Jack-language tokens, as specified by Jack grammar.

    Tokenizing, a basic service of any syntax analyzer, is the act of breaking a given textual input into a stream of tokens. And while it is at it, the tokenizer can also classify the tokens into lexical categories. With that in mind, your first task it to implement, and test, the JackTokenizer module specified in chapter 10. Specifically, you have to develop (i) a Tokenizer implementation, and (ii) a test program that goes through a given input file (.jack file) and produces a stream of tokens using your Tokenizer implementation. Each token should be printed in a separate line, along with its classification: symbol, keyword, identifier, integer constant or string constant.


    """

    KEYWORDS_TABLE = {
        'class': token_types.CLASS,
        'method': token_types.METHOD,
        'function': token_types.FUNCTION,
        'constructor': token_types.CONSTRUCTOR,
        'int': token_types.INT,
        'boolean': token_types.BOOLEAN,
        'char': token_types.CHAR,
        'void': token_types.VOID,
        'var': token_types.VAR,
        'static': token_types.STATIC,
        'field': token_types.FIELD,
        'let': token_types.LET,
        'do': token_types.DO,
        'if': token_types.IF,
        'else': token_types.ELSE,
        'while': token_types.WHILE,
        'return': token_types.RETURN,
        'true': token_types.TRUE,
        'false': token_types.FALSE,
        'null': token_types.NULL,
        'this': token_types.THIS,
    }

    NAMES_TABLE = {
        token_types.TOKEN_TYPE: 'token_type',
        token_types.KEYWORD: 'keyword',
        token_types.SYMBOL: 'symbol',
        token_types.IDENTIFIER: 'identifier',
        token_types.INT_CONST: 'int_const',
        token_types.STRING_CONST: 'string_const',
        token_types.CLASS: 'class',
        token_types.METHOD: 'method',
        token_types.FUNCTION: 'function',
        token_types.CONSTRUCTOR: 'constructor',
        token_types.INT: 'int',
        token_types.BOOLEAN: 'boolean',
        token_types.CHAR: 'char',
        token_types.VOID: 'void',
        token_types.VAR: 'var',
        token_types.STATIC: 'static',
        token_types.FIELD: 'field',
        token_types.LET: 'let',
        token_types.DO: 'do',
        token_types.IF: 'if',
        token_types.ELSE: 'else',
        token_types.WHILE: 'while',
        token_types.RETURN: 'return',
        token_types.TRUE: 'true',
        token_types.FALSE: 'false',
        token_types.NULL: 'null',
        token_types.THIS: 'this',
    }

    XML_ESCAPES = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
    }

    def __init__(self, file):
        """Opens the input file and gets ready to parse it.

        `token_cache` with look like:
        {"example_token":
            {"token_type": 4, "string_val": "example_string"}}
        OR
        {"example_token":
            {"token_type": 0, "keyword": "example_keyword"}}
        """
        self.fd = open(file)
        self.token = ""
        self._next_token = ""
        self.token_queue = []  # first in first out (fifo) queue
        self.token_cache = {}
        self.more_tokens = True
        self.line_number = 1

    def has_more_tokens(self):
        """Do we have more tokens in input?"""
        return self.more_tokens

    def next_clean_line(self):
        """Remove comments and whitespace from line.

        This might combine two lines into one if a multi-line
        comment is partially on several lines.
        eg:
            do Output.printString("Hello world!"); /** test
            test */ do Output.printString("does this compile?");
        will output:
            do Output.printString("Hello world!"); do Output.printString("does this compile?");
        """

        inside_block_comment = False
        block_comment = ""

        for line in self.fd:
            if patterns.BLOCK_COMMENT_START.search(line):
                inside_block_comment = True
            if inside_block_comment:
                block_comment += line
                comment_removed = patterns.BLOCK_COMMENT.sub('', block_comment)
                if comment_removed != block_comment:
                    inside_block_comment = False
                    block_comment = ""
                    line = comment_removed
                else:
                    continue  # continue until block comment end is found!
            line = patterns.LINE_COMMENT.sub('', line)

            line = ' '.join(line.split())  # remove extra whitespace
            if line:
                yield line

    def advance(self):
        """Gets the next token from input and makes it the current token.

        This method should only be called if 'has_more_tokens()' is true.
        Initially there is no current token.

        Only returns non-empty tokens.
        Output is delayed to accommodate comments.
        Output is delayed to accommodate while loop.
        """

        if self.has_more_tokens():
            for line in self.next_clean_line():
                # These 2 lines do ALL the work!
                tokens = patterns.ALL_TERMINATORS.finditer(line)
                self.token_queue = itertools.chain(self.token_queue, tokens)
            # import pdb;pdb.set_trace()
            try:
                self.token = self._next_token or next(self.token_queue).group(0)
                self.line_number += 1
                self._next_token = next(self.token_queue).group(0)
            except StopIteration:
                self._next_token = ''
            if not self._next_token:
                self.more_tokens = False
                self.fd.close()
        else:
            raise StopIteration("No more tokens")

    def token_type(self):
        """Returns the type of the current token.

        :returns: KEYWORD, SYMBOL, IDENTIFIER, INT_CONST, STRING_CONST
        """
        # import pdb;pdb.set_trace()
        try:
            return self.token_cache[self.token]["token_type"]
        except KeyError:
            pass

        if patterns.KEYWORD.fullmatch(self.token):
            temp_type = token_types.KEYWORD
        elif patterns.SYMBOL.fullmatch(self.token):
            temp_type = token_types.SYMBOL
        elif patterns.INT_CONST.fullmatch(self.token):
            temp_type = token_types.INT_CONST
        elif patterns.STRING_CONST.fullmatch(self.token):
            temp_type = token_types.STRING_CONST
        elif patterns.IDENTIFIER.fullmatch(self.token):
            temp_type = token_types.IDENTIFIER
        else:
            temp_type = None

        self.token_cache[self.token] = {"token_type": temp_type}
        return temp_type

    def key_word(self):
        """Returns the keyword which is the current token.

        Should only be called when the 'token_type()' is KEYWORD.
        :returns: CLASS, METHOD, FUNCTION, CONSTRUCTOR, INT, BOOLEAN,
        CHAR, VOID, VAR, STATIC, FIELD, LET, DO, IF, ELSE, WHILE, RETURN,
        TRUE, FALSE, NULL, THIS
        """

        if self.token_type() == token_types.KEYWORD:
            try:
                return self.token_cache[self.token]["key_word"]
            except KeyError:
                pass

            type_ = self.KEYWORDS_TABLE[self.token]
            self.token_cache[self.token] = {"key_word": type_}
            return type_
        else:
            raise TypeError("'token_type()' is not KEYWORD.")

    def symbol(self):
        """Returns the character which is the current token.

        Should only be called when 'token_type()' is SYMBOL.
        :returns: Char
        """

        if self.token_type() == token_types.SYMBOL:
            try:
                return self.token_cache[self.token]["symbol"]
            except KeyError:
                pass

            valid_xml_char = self.XML_ESCAPES[self.token] if self.token in self.XML_ESCAPES else self.token
            self.token_cache[self.token] = {"symbol": valid_xml_char}
            return valid_xml_char
        else:
            raise TypeError("'token_type()' is not SYMBOL.")

    def identifier(self):
        """Returns the identifier which is the current token.

        Should only be called when 'token_type()' is IDENTIFIER.
        :returns: String
        """

        if self.token_type() == token_types.IDENTIFIER:
            try:
                return self.token_cache[self.token]["identifier"]
            except KeyError:
                pass

            self.token_cache[self.token] = {"identifier": self.token}
            return self.token
        else:
            raise TypeError("'token_type()' is not IDENTIFIER.")

    def int_val(self):
        """Returns the integer value of the current token.

        Should only be called when 'token_type()' is INT_CONST.
        :returns: Int
        """

        if self.token_type() == token_types.INT_CONST:
            try:
                return self.token_cache[self.token]["int_val"]
            except KeyError:
                pass

            int_val_token = int(self.token)
            self.token_cache[self.token] = {"int_val": int_val_token}
            return int_val_token
        else:
            raise TypeError("'token_type()' is not INT_CONST.")

    def string_val(self):
        """Returns the string value of the current token.

        Without double quotes.
        Should only be called when 'token_type()' is STRING_CONST.
        :returns: String
        """

        if self.token_type() == token_types.STRING_CONST:
            try:
                return self.token_cache[self.token]["string_val"]
            except KeyError:
                pass

            string_val_token = self.token[1:-1]
            self.token_cache[self.token] = {"string_val": string_val_token}
            return string_val_token
        else:
            raise TypeError("'token_type()' is not STRING_CONST.")
