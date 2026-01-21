class Caller_Error(Exception):
    pass

class Command_Not_Found_Error(Caller_Error, KeyError):
    def __init__(self, command: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command = command
    
    def __str__(self) -> str:
        return f"Command '{self.command}' not found"

class Command_Invalid_Arguments_Error(Caller_Error):
    def __init__(self, command: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command = command
    
    def __str__(self) -> str:
        return f"Command '{self.command}' has invalid arguments"