class CodechefException(Exception):
    pass


class APIInputError(CodechefException):
    pass


class TokensNotFound(CodechefException):
    pass

class APIError(CodechefException):
    pass
