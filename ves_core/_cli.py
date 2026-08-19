import os
import sys
import json
import time
import shlex
import ctypes
import traceback
from typing import (
    Iterable,
    Any
)
from pathlib import Path
from datetime import datetime
from ._managers.base import BaseVES
from ._format_time_duration import format_time_duration
from .terminal_size_print import (
    print_dividing_line,
    center_title
)
from ._command_caller import (
    Command_Caller,
    Command_Not_Found_Error,
    Command_Invalid_Arguments_Error
)
from ._variable_manager import VariableManager
from ._ves_exception import *

class VESCLI:
    def __init__(self, ves: BaseVES):
        self._ves = ves
        self._values = VariableManager()
        self._return_value: Any = None
        self._cmd_caller = Command_Caller(
            cmds = {
                "create": self._ves.create,
                "chbase": self._change_base_dir,
                "recursive": self._recursive,
                "ifr": self._ves.install_for_requirements,
                "shell": self._ves.shell,
                "repl": self._ves.repl,
                "install": self._install_cli,
                "uninstall": self._uninstall_cli,
                "copy": self._copy_env_cli,
                "cmdls": self._cmdlist_cli,
                "freeze": self._ves.freeze,
                "list": self._list_cli,
                "remove": self._ves.remove,
                "delete": self._ves.remove,
                "print": print,
                "title": self.title,
                "set_var": self._values.set,
                "set_const": self._values.set_const,
                "get_var": self._values.get,
                "remove_var": self._values.remove,
                "set_var_from_ret": self._set_var_from_ret,
                "set_const_from_ret": self._set_const_from_ret,
                "jump": self._jump,
                "je": self._jump_equal,
                "jne": self._jump_not_equal,
                "jlt": self._jump_lt,
                "jgt": self._jump_gt,
                "jle": self._jump_le,
                "jge": self._jump_ge,
                "jt": self._jump_true,
                "jf": self._jump_false,
                "execute": self._file_interface,
                "help": self.print_help,
                "exit": self._exit_this_cli,
            }
        )

    def _change_base_dir(self, base_dir: str):
        """
        Change the base directory

        :param base_dir: The new base directory
        """
        self._ves.base_dir = Path(base_dir)
    
    def _set_var_from_ret(self, key: str):
        """
        Set a variable from the return value of the last command.

        Args:
            key (str): The name of the variable to set.
        """
        self._values.set(key, self._return_value)

    def _set_const_from_ret(self, key: str):
        """
        Set a constant from the return value of the last command.

        Args:
            key (str): The name of the constant to set.
        """
        self._values.set_const(key, self._return_value)
    
    def _install_cli(self, env_name: str, package: str):
        """
        Install a package in the environment

        :param env_name: The name of the environment
        :param package: The package to install
        """
        self._ves.install(env_name, package)
    
    def _uninstall_cli(self, env_name: str, package: str):
        """
        Uninstall a package in the environment

        :param env_name: The name of the environment
        :param package: The package to uninstall
        """
        self._ves.install(env_name, package, uninstall=True)
    
    def _exit_this_cli(self, exit_code: int = 0):
        """
        Exit this CLI

        :param exit_code: The exit code
        """
        raise VES_CLI_EXIT(exit_code)
    
    def _jump(self, line: int, absolute: bool = False):
        """
        Jump to the line
        (Can only run in file mode)

        :param line: The line to jump to
        """
        raise VES_CLI_JUMP(line, absolute)
    
    def _jump_equal(self, key1: str, key2: str, line: int, absolute: bool = False):
        """
        if var1 == var2 jump to line

        :param key1: The first key
        :param key2: The second key
        :param line: The line to jump to
        :param absolute: If the line is absolute
        """
        value1 = self._values.get(key1)
        value2 = self._values.get(key2)
        if value1 == value2:
            self._jump(line, absolute)
    
    def _jump_not_equal(self, key1: str, key2: str, line: int, absolute: bool = False):
        """
        if var1 != var2 jump to line
        :param key1: The first variable to compare
        :param key2: The second variable to compare
        :param line: The line to jump to
        :param absolute: If the line is absolute
        """
        value1 = self._values.get(key1)
        value2 = self._values.get(key2)
        if value1 != value2:
            self._jump(line, absolute)
    
    def _jump_gt(self, key1: str, key2: str, line: int, absolute: bool = False):
        """
        if var1 > var2 jump to line

        :param key: The variable to check
        :param line: The line to jump to
        :param absolute: If the line is absolute
        """
        value1 = self._values.get(key1)
        value2 = self._values.get(key2)
        if value1 > value2:
            self._jump(line, absolute)
    
    def _jump_lt(self, key1: str, key2: str, line: int, absolute: bool = False):
        """
        if var1 < var2 jump to line

        :param key: The variable to check
        :param line: The line to jump to
        :param absolute: If the line is absolute
        """
        value1 = self._values.get(key1)
        value2 = self._values.get(key2)
        if value1 < value2:
            self._jump(line, absolute)

    def _jump_ge(self, key1: str, key2: str, line: int, absolute: bool = False):
        """
        if var1 >= var2 jump to line

        :param key: The variable to check
        :param line: The line to jump to
        :param absolute: If the line is absolute
        """
        value1 = self._values.get(key1)
        value2 = self._values.get(key2)
        if value1 >= value2:
            self._jump(line, absolute)

    def _jump_le(self, key1: str, key2: str, line: int, absolute: bool = False):
        """
        if var1 <= var2 jump to line

        :param key: The variable to check
        :param line: The line to jump to
        :param absolute: If the line is absolute
        """
        value1 = self._values.get(key1)
        value2 = self._values.get(key2)
        if value1 <= value2:
            self._jump(line, absolute)
    
    def _jump_true(self, key: str, line: int, absolute: bool = False):
        """
        if var1 jump to line

        :param key: The variable to check
        :param line: The line to jump to
        :param absolute: If the line is absolute
        """
        if self._values.get(key):
            self._jump(line, absolute)

    def _jump_false(self, key: str, line: int, absolute: bool = False):
        """
        if not var1 jump to line

        :param key: The variable to check
        :param line: The line to jump to
        :param absolute: If the line is absolute
        """
        if not self._values.get(key):
            self._jump(line, absolute)
    
    @staticmethod
    def title(title: str):
        """
        Set the console title

        :param title: The title to set
        """
        if os.name == "nt":
            try:
                ctypes.windll.kernel32.SetConsoleTitleW(title)
            except:
                os.system(f"title {title}")
        else:
            print(f"\033]2;{title}\007")
    
    def _var_expand(self, commands: list[str]) -> list[Any]:
        """
        Expand variables in a command

        :param commands: The command to expand
        :return: The expanded command
        """
        cmds_copy: list[Any] = []
        for command in commands:
            if command.startswith("$"):
                cmds_copy.append(self._values.get(command[1:]))
            else:
                cmds_copy.append(command)
        return cmds_copy

    def _recursive(self, *commands: str):
        return self.main([shlex.split(command) for command in commands])

    def main(self, commands: Iterable[list[str]] | None = None):
        """
        Run the VES

        :param commands: The commands to run
        """
        try:
            if commands is None:
                try:
                    if len(sys.argv) > 1:
                        cmd = sys.argv[1:]
                        cmd[0] = cmd[0].lower()
                        self.match_cmd(cmd)
                    else:
                        self.cli()
                except VES_CLI_JUMP as e:
                    print("JUMP can not be used in the current mode.")
            else:
                commands = list(commands)
                run_point: int = 0
                if not commands:
                    self.cli()
                else:
                    while True:
                        try:
                            cmd = commands[run_point]
                            cmd[0] = cmd[0].lower()
                            self.match_cmd(cmd)
                            run_point += 1
                        except VES_CLI_JUMP as e:
                            raw_point = run_point
                            if e.absolute:
                                run_point = e.line
                            else:
                                run_point += e.line
                            if run_point < 0 or run_point >= len(commands):
                                print("Jump out of range")
                                run_point = raw_point
        except VES_CLI_EXIT as e:
            return e.code
        except Exception as e:
            now = datetime.now()
            path = Path(f"traceback/[{now.strftime('%Y-%m-%d-%H-%M-%S')}]_Traceback.txt")
            if not path.parent.exists():
                path.parent.mkdir(parents=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(traceback.format_exc())
            raise
        return 0
    
    def print_help(self):
        """
        Print help message
        """
        print("VES - Virtual Environment System")
        print("Usage: ves <command> [args]")
        print("Commands:")
        print("")
        print("=" * 22)
        print("  " + self._cmd_caller.help(20).replace("\n", "\n  "))
        print("=" * 22)
    
    @staticmethod
    def print_python_version():
        print(f"Python {sys.version}")

    def cli(self):
        self.title("VES - Virtual Environment System")
        center_title("VES - Virtual Environment System")
        print_dividing_line()

        print(f"Base dir: {self._ves.base_dir}")
        self.print_python_version()
        while True:
            try:
                choice = input("> ")
            except KeyboardInterrupt:
                print("\nKeyboard Interrupt")
                continue
            except EOFError:
                print("\nEOF Error")
                break

            cmd = shlex.split(choice)
            if len(cmd) >= 1:
                cmd[0] = cmd[0].lower()
            
            try:
                self.match_cmd(cmd)
            except VES_CLI_JUMP as e:
                print("JUMP can not be used in interactive mode")
    
    def match_cmd(self, choice: list[str]):
        try:
            return self._cmd_caller(self._var_expand(choice))
        except Command_Not_Found_Error as e:
            print(e)
        except Command_Invalid_Arguments_Error as e:
            print(e)
    
    def _file_interface(self, file_path: str, encoding: str = "utf-8"):
        """
        Run VES from file

        :param file_path: Path to file
        :param encoding: Encoding of file
        """
        print_dividing_line()
        try:
            start_time = time.monotonic_ns()
            with open(file_path, "r", encoding = encoding) as f:
                def _code_generator():
                    for line in f:
                        yield shlex.split(line)
                
                result = self.main(_code_generator())
            end_time = time.monotonic_ns()
            print_dividing_line()
            print(f"VES Sub-Examples Result: {result}")
            print(f"Run time: {format_time_duration(end_time - start_time, use_abbreviation=True)}")
        except Exception as e:
            print_dividing_line()
            print(f"VES Sub-Examples Error: {e}")
            raise
    
    def _copy_env_cli(self, src_venv_name: str, dst_venv_name: str):
        """
        Copy environment from one to another

        :param src_venv_name: Source environment name
        :param dst_venv_name: Destination environment name
        """
        freeze = self._ves.freeze(src_venv_name)
        if not freeze:
            print_dividing_line()
            print(f"VES Sub-Examples Error: Source environment '{src_venv_name}' not found")
            raise
        else:
            if self._ves.exists(dst_venv_name):
                self._ves.remove(dst_venv_name)
            self._ves.create(dst_venv_name)
            self._ves.install(dst_venv_name, freeze.replace("\n", " "))
    
    def _list_cli(self):
        """
        List environments
        """
        envs = list(self._ves.get_envs())
        for env in envs:
            print(env)
    
    def _activate_cli(self, venv_name: str):
        """
        Activate environment

        :param venv_name: Environment name
        """
        if self._ves.initable(venv_name):
            self._ves.init_venv(venv_name)
        self._ves.shell(venv_name)
    
    def _cmdlist_cli(self, json_format: bool = False):
        """
        List all available commands

        :param json_format: Whether to output in json format
        """
        if json_format:
            print(json.dumps(self._cmd_caller.cmds))
        else:
            print("Available commands:")
            for cmd in self._cmd_caller.cmds:
                print(f"  - {cmd}")