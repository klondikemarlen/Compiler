import itertools

from parser.utils import token_types


class CompileError(Exception):
    pass


class CompileKeyError(CompileError):
    pass


class PlusEqualsableIterator:
    def __init__(self):
        self._iter = (x for x in [])

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._iter)

    def __iadd__(self, other):
        # import pdb;pdb.set_trace()
        self._iter = itertools.chain(self._iter, [other])
        return self

    def __repr__(self):
        return "<{} at {}>".format(self.__class__.__name__, hex(id(self)))


class CompilationEngine:
    """A recursive top-down parser for Jack.

    The *CompilationEngine* effects the actual compilation output.

    It gets its input from a `JackTokenizer` and emits its parsed structure into an output file/stream.

    The output is generated by a series of `compilexxx()` routines, one for every syntactic element `xxx` of the Jack grammar.

    The contract between these routines is that each `compilexxx()` routine should read the syntactic construct `xxx` from the input, `advance()` the tokenizer exactly beyond `xxx`, and output the parsing of `xxx`.
        Thus, `compilexxx()` may only be called if `xxx` is the next syntactic element of the input.

    In the first version of the compiler, which we now build, this module emits a structured printout of the code, wrapped in XML tags (defined in the specs of project 10). In the final version of the compiler, this module generates executable VM code (defined in the specs of project 11).

    In both cases, the parsing logic and module API are exactly the same.

    The syntax analyzer’s algorithm shown in this slide:
    If xxx is non-terminal, output:
        <xxx>
            Recursive code for the body of xxx
        </xxx>
    If xxx is terminal (keyword, symbol, constant, or identifier), output:
        <xxx>
            xxx value
        </xxx>

    """

    def __init__(self, infile, outfile):
        """Creates a new compilation engine with the given input and output.

        The next routine called must be `compile_class()`.
        """

        # I'm kind of confused about piping ...
        self._infile = infile
        self._outfile = outfile
        self._indent = 0
        self._body = PlusEqualsableIterator()  # iterator of all body elements.

    def compile_class(self):
        """Compiles a complete class.

        class: 'class' className '{' classVarDec* subroutineDec* '}'
        """
        f = self._infile
        current_element = 'class'

        self.add_keywords([current_element])  # step 1 - 'class'
        self.add_identifier('class name')  # step 2 - className
        self.add_symbols(['{'])  # step 3 - '{'

        # write start of element body
        self.write_non_terminal_start(current_element)

        # Need to advance once on outside of loop.
        # This is so that compile_class_var_dec can fail without
        # pulling and extra token.
        while True:  # step 4 - classVarDec*
            f.advance()  # ok maybe inside the loop?
            try:
                self.compile_class_var_dec()  # step 4.i - classVarDec
            except CompileKeyError:
                break

        # This compile has a dead first step too!
        while True:  # step 5 - subroutineDec*
            try:
                self.compile_subroutine()  # step 5.i - subroutineDec
            except CompileKeyError:
                break

        self.add_symbols(['}'])  # step 6 - '}'

        # write end of element body
        self.write_non_terminal_end(current_element)

    def compile_class_var_dec(self):
        """Compiles a static declaration or a field declaration.

        classVarDec: ('static' | 'field) type varName (, varName)* ';'

        NOTE: first step of first function is smothered ... this is so it
        can fail without advancing!
        """

        f = self._infile
        current_element = "classVarDec"

        self.add_keywords(['static', 'field'], step=False)  # step 1 - ('static' | 'field)
        self.add_type()  # step 2 - type
        self.add_identifier('variable name')  # step 3 - varName

        # step 4/5 - (',' varName)* ';'
        # I merged these steps for convenience.
        more_vars = True
        while more_vars:
            self.add_symbols([',', ';'])  # (',' varName)* ';'
            if f.symbol() == ';':
                more_vars = False
            else:
                self.add_identifier('variable name')

        # write element body
        self.write_non_terminal(current_element)

    def compile_subroutine(self):
        """Compiles a complete method, function or constructor.

        subroutineDec: ('constructor' | 'function' | 'method') ('void' | type) subroutineName '(' parameterList ')' subroutineBody

        NOTE: first step of first function is smothered ... this is so it
        can fail without advancing!
        """
        current_element = "subroutineDec"

        self.add_keywords(['constructor', 'function', 'method'], step=False)
        self.add_type(void=True)
        self.add_identifier('subroutine name')
        self.add_symbols(['('])

        self.write_non_terminal_start(current_element)  # write body start

        self.compile_parameter_list()  # new non-terminal

        # Needs special write call as this appears between two non-terminals
        self.add_symbols([')'])
        self.write_terminal(*next(self._body), indent=True)

        self.compile_statements()  # ??

        self.write_non_terminal_end(current_element)  # write body end

    def compile_parameter_list(self):
        """Compiles a (possibly empty) parameter list, not including the enclosing '( )'.

        parameterList: ((type varName)(',' type varName)*)?
        """



    def compile_var_dec(self):
        """Compiles a `var` declaration."""

    def compile_statements(self):
        """Compiles a sequence of statements, not including the enclosing '{ }'.
        """

    def compile_do(self):
        """Compiles a `do` statement."""

    def compile_let(self):
        """Compiles a `let` statement."""

    def compile_while(self):
        """Compiles a `while` statement."""

    def compile_return(self):
        """Compiles a `return` statement."""

    def compile_if(self):
        """Compiles an `if` statement, possibly with a trailing `else` clause.
        """

    def compile_expression(self):
        """Compiles an `expression`."""

    def compile_term(self):
        """Compiles a `term`.

        This routine is faced with a slight difficulty when trying to decide between some of the alternative parsing rules. Specifically, if the current token is an identifier, the routine must distinguish between a variable, an array entry, and a subroutine call. A single look-ahead token, which may be one of "[", "{" or "." suffices to distinguish between the three possibilities. Any other token is not part of this term and should not be advanced over.
        """

    def compile_expression_list(self):
        """Compiles a (possibly empty) comma-separated list of expressions."""

    def add_keywords(self, keywords, step=True):
        """Add keyword(s) definition to body element."""
        f = self._infile

        if step:
            f.advance()

        if f.token_type() == token_types.KEYWORD and any([f.key_word() == f.KEYWORDS_TABLE[key] for key in keywords]):
            terminal = f.NAMES_TABLE[f.key_word()]
            self._body += ['keyword', terminal]
        else:
            expected = "| ".join(["'{}'".format(key) for key in keywords])
            raise CompileKeyError("Expected {}".format(expected))

    def add_symbols(self, symbols, step=True):
        """Add symbol definition to body element."""
        f = self._infile

        if step:
            f.advance()

        if f.token_type() == token_types.SYMBOL and any([f.symbol() == sym for sym in symbols]):
            self._body += ['symbol', f.symbol()]
        else:
            expected = "| ".join(["'{}'".format(sym) for sym in symbols])
            raise CompileError("Expected {}".format(expected))

    def add_identifier(self, identifier, step=True):
        """Add identifier definition to body element."""
        f = self._infile

        if step:
            f.advance()

        if f.token_type() == token_types.IDENTIFIER:
            self._body += ['identifier', f.identifier()]
        else:
            raise CompileError("Expected a {}", identifier)

    def add_type(self, void=False):
        """Add a type declaration.

        type: 'int' | 'char' | 'boolean' | className
        """
        f = self._infile
        valid_types = [token_types.INT, token_types.CHAR, token_types.BOOLEAN]
        if void:
            valid_types.append(token_types.VOID)

        f.advance()
        if f.token_type() == token_types.KEYWORD and any([f.key_word() == type_ for type_ in valid_types]):
            terminal = f.NAMES_TABLE[f.key_word()]
            self._body += ['keyword', terminal]
        elif f.token_type() == token_types.IDENTIFIER:
            self._body += ['identifier', f.identifier()]
        else:
            expected = "| ".join(["'{}'".format(typ) for typ in valid_types + ['className']])
            raise CompileError("Expected {}".format(expected))

    def write_terminal(self, element, terminal, indent=False):
        """Write a terminating xml element."""
        if indent:
            self._outfile.write(' ' * self._indent)
        print('<{element}> {terminal} </{element}>'.format(element=element, terminal=terminal), file=self._outfile)

    def write_non_terminal_start(self, element):
        """Write the start of a non-terminating xml element.

        uses self._body generator.
        """
        self._outfile.write(' ' * self._indent)
        print("<{}>".format(element), file=self._outfile)

        self._indent += 2  # on every body section increase indent.
        for inner_element, terminal in self._body:
            self._outfile.write(' ' * self._indent)
            self.write_terminal(inner_element, terminal)

    def write_non_terminal_end(self, element):
        """Write the end of a non-terminating xml element."""
        self._indent -= 2  # after every body section decrease indent.
        self._outfile.write(' ' * self._indent)
        print("</{}>".format(element), file=self._outfile)

    def write_non_terminal(self, element):
        """Write a non-terminating xml element.

        uses self._body generator.
        """
        self.write_non_terminal_start(element)
        self.write_non_terminal_end(element)
