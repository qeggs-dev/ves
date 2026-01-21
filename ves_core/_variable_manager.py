from typing import Any
from dataclasses import dataclass

@dataclass
class VESVariable:
    value: Any
    readonly: bool = False

class VariableManager:
    def __init__(self):
        self._variables: dict[str, VESVariable] = {}
    
    def set(self, key: str, value: Any):
        """
        Set a variable.
 
        Args:
            key (str): The name of the variable.
            value (Any): The value of the variable.
        
        Raises:
            ValueError: If the variable is read-only.
        """
        if key in self._variables and self._variables[key].readonly:
                raise ValueError(f"Variable '{key}' is read-only.")
        self._variables[key] = VESVariable(value)
    
    def set_const(self, key: str, value: Any):
        """
        Set a constant variable.

        Args:
            key (str): The name of the variable.
            value (Any): The value of the variable.

        Raises:
            ValueError: If the variable is existing and is read-only.
        """
        if key in self._variables and self._variables[key].readonly:
            raise ValueError(f"Variable '{key}' is read-only.")
        self._variables[key] = VESVariable(value, True)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a variable.

        Args:
            key (str): The name of the variable.
            default (Any): The default value of the variable.

        Returns:
            Any: The value of the variable.
        """
        return self._variables.get(key, VESVariable(default)).value

    def remove(self, key: str):
        """
        Remove a variable.

        Args:
            key (str): The name of the variable.
        """
        if key in self._variables and self._variables[key].readonly:
            raise ValueError(f"Variable '{key}' is read-only.")
        self._variables.pop(key, None)
    
    def strvalue(self, key: str) -> str:
        """
        Get the string representation of a variable.

        Args:
            key (str): The name of the variable.

        Returns:
            str: The string representation of the variable.
        """
        return str(self._variables[key])
    
    def reprvalue(self, key: str) -> str:
        """
        Get the repr representation of a variable.

        Args:
            key (str): The name of the variable.

        Returns:
            str: The repr representation of the variable.
        """
        return repr(self._variables[key])
    
    def __contains__(self, key: str) -> bool:
        return key in self._variables
    
    def __getitem__(self, key: str) -> Any:
        return self._variables[key]

    def __setitem__(self, key: str, value: Any):
        if key in self._variables and self._variables[key].readonly:
            raise ValueError(f"Variable '{key}' is read-only.")
        self._variables[key] = value
    
    def __delitem__(self, key: str):
        if key in self._variables and self._variables[key].readonly:
            raise ValueError(f"Variable '{key}' is read-only.")
        del self._variables[key]