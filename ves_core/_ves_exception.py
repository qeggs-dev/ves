class VES_CLI_EXIT(Exception):
    def __init__(self, code: int):
        self.code = code

class VES_CLI_JUMP(Exception):
    def __init__(self, line: int, absolute: bool = False):
        self.line = line
        self.absolute = absolute