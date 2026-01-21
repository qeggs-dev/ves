from typing import Callable, Any
from ._exceptions import *
import inspect
import warnings

class MissingDocstringWarning(Warning):
    """
    Raised when a command does not have a docstring.
    """
    pass

class Command_Caller:
    def __init__(self, cmds: dict[str, Callable[..., Any]] | None = None):
        if cmds is not None:
            self._cmds: dict[str, Callable[..., Any]] = cmds
        else:
            self._cmds: dict[str, Callable[..., Any]] = {}
    
    @property
    def cmds(self) -> list[str]:
        return list(self._cmds.keys())
    
    def register(self, cmd: str, func: Callable[..., Any]):
        self._cmds[cmd] = func
    
    def __call__(self, command: list[str]) -> None | Any:
        if len(command) == 0:
            return None
        
        if command[0] in self._cmds:
            func = self._cmds[command[0]]
            arguments = command[1:]
            sig = inspect.signature(func)
            try:
                sig.bind(*arguments)
            except TypeError as e:
                raise Command_Invalid_Arguments_Error(
                    command[0],
                    str(e)
                )
            return func(*arguments)
        else:
            raise Command_Not_Found_Error(command=command[0])
    
    def help(self, length_of_dividing_line: int = 10, newline_char: str = "\n") -> str:
        text_buffer: list[str] = []
        for cmd in self.cmds:
            if self._cmds[cmd].__doc__:
                text_buffer.append(f"{cmd} - {self._cmds[cmd].__doc__.strip()}")
                text_buffer.append("=" * length_of_dividing_line)
            else:
                warnings.warn(f"Command '{cmd}' has no docstring", MissingDocstringWarning)
        if len(text_buffer) > 0:
            text_buffer.pop() # remove last dividing line
        return newline_char.join(text_buffer)