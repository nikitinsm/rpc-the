

class RpcError(Exception):
    code = None
    message = None


class ParseError(RpcError):
    code = -32700
    message = "Parse error"


class InvalidRequest(RpcError):
    code = -32600
    message = "Invalid Request"


class MethodNotFound(RpcError):
    code = -32601
    message = "Method not found"


class InvalidParams(RpcError):
    code = -32602
    message = "Invalid params"


class InternalError(RpcError):
    code = -32603
    message = "Internal error"


class ServerError(RpcError):
    code = -32000
    message = "Server error"


class UserServerError(ServerError):

    def __init__(self, code, message):
        self.code = code
        self.message = message
