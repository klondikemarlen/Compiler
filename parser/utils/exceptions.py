class CompileError(Exception):
    pass


class CompileKeywordError(CompileError):
    pass


class CompileSymbolError(CompileError):
    pass


class CompileTypeError(CompileError):
    pass


class CompileClassVarDecError(CompileError):
    pass


class CompileSubroutineError(CompileError):
    pass


class CompileParameterListError(CompileError):
    pass


class CompileSubroutineBodyError(CompileError):
    pass


class CompileVarDecError(CompileError):
    pass


class CompileLetError(CompileError):
    pass


class CompileExpressionError(CompileError):
    pass


class CompileOpError(CompileError):
    pass


class CompileKeywordConstantError(CompileError):
    pass


class CompileDoError(CompileError):
    pass


class CompileSubroutineCallError(CompileError):
    pass


class CompileReturnError(CompileError):
    pass


class CompileIfError(CompileError):
    pass

