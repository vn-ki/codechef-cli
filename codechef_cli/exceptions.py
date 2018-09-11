class CodechefException(Exception):
    pass


class APIInputError(CodechefException):
    pass


class TokensNotFound(CodechefException):
    pass
