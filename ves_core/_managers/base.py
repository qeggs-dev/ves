import os
import time
import shlex
import shutil
import subprocess
from pathlib import Path
from .._format_time_duration import format_time_duration
from abc import ABC, abstractmethod
from functools import wraps
from ..terminal_size_print import (
    print_dividing_line,
    center_title
)
from typing import (
    overload,
    IO,
    Protocol,
    Callable,
    Literal,
    Any,
    Collection,
    Iterable
)
from collections.abc import Sequence

# 我也不知道这是啥类型，反正先放上去了
class Buffer(Protocol):
    def __buffer__(self, flags: int) -> memoryview:
        ...

class FSPath(Protocol):
    def __fspath__(self) -> str:
        ...

class BaseVES(ABC):
    def __init__(
            self,
            base_dir: Path = Path.cwd() / "envs",
            print_run_statistics: bool = False,
            venv_dir: str = ".venv",
            python_executable_name: str = "python3",
            pip_executable_name: str = "pip3"
        ):
        self._base_dir = base_dir
        self._print_run_statistics = print_run_statistics
        self._envs: dict[str, str] = os.environ.copy()
        self._venv_dir = venv_dir
        self._python_executable_name = python_executable_name
        self._pip_executable_name = pip_executable_name
    
    @property
    def base_dir(self) -> Path:
        """
        The base directory for the virtual environments.
        """
        return self._base_dir

    @base_dir.setter
    def base_dir(self, base_dir: Path):
        if not isinstance(base_dir, Path):
            raise TypeError("base_dir must be a Path")
        self._base_dir = base_dir
    
    def _venv_path(self, env_name: str) -> Path:
        return self.base_dir / env_name / self._venv_dir
    
    @abstractmethod
    def _bin_dir_path(self, env_name: str) -> Path:
        ...
    
    def remove(self, env_name: str):
        """
        Remove a virtual environment.

        :param env_name: The name of the virtual environment to remove.
        """
        path = self._venv_path(env_name)
        shutil.rmtree(path)
    
    def get_envs(self):
        """
        Get a Generator of all virtual environments.

        :return: A Generator of all virtual environments.
        """
        for path in self._base_dir.iterdir():
            if path.is_dir() and (path / ".venv" / "pyvenv.cfg").exists():
                yield path.name
    
    def exists(self, env_name: str):
        return (self._venv_path(env_name) / "pyvenv.cfg").exists()
    
    def initable(self, env_name: str):
        return (self._base_dir / env_name / "init.py").exists()

    @overload
    def _run(
        self,
        args: str | FSPath | Sequence[str | FSPath],
        bufsize: int = -1,
        executable: str | os.PathLike | None = None,
        stdin: IO | None = None,
        stdout: IO | None = None,
        stderr: IO | None = None,
        preexec_fn: Callable[[], object] | None = None,
        close_fds: bool = True,
        shell: bool = False,
        cwd: str | os.PathLike | None = None,
        env: dict[str, str] | None = None,
        universal_newlines: Literal[True] | None = None,
        startupinfo: Any = None,
        creationflags: int = 0,
        restore_signals: bool = True,
        start_new_session: bool = False,
        pass_fds: Collection[int] = (),
        *,
        capture_output: bool = False,
        check: bool = False,
        encoding: str | None = None,
        errors: str | None = None,
        input: str | None = None,
        text: Literal[True],
        timeout: float | None = None,
        user: str | int | None = None,
        group: str | int | None = None,
        extra_groups: Iterable[str | int] | None = None,
        umask: int = -1,
        pipesize: int = -1,
        process_group: int | None = None
    ) -> subprocess.CompletedProcess[str] | None: ...

    @overload
    def _run(
        self,
        args: str | FSPath | Sequence[str | FSPath],
        bufsize: int = -1,
        executable: str | os.PathLike | None = None,
        stdin: IO | None = None,
        stdout: IO | None = None,
        stderr: IO | None = None,
        preexec_fn: Callable[[], object] | None = None,
        close_fds: bool = True,
        shell: bool = False,
        cwd: str | os.PathLike | None = None,
        env: dict[str, str] | None = None,
        universal_newlines: bool | None = None,
        startupinfo: Any = None,
        creationflags: int = 0,
        restore_signals: bool = True,
        start_new_session: bool = False,
        pass_fds: Collection[int] = (),
        *,
        capture_output: bool = False,
        check: bool = False,
        encoding: str,
        errors: str | None = None,
        input: str | None = None,
        text: bool | None = None,
        timeout: float | None = None,
        user: str | int | None = None,
        group: str | int | None = None,
        extra_groups: Iterable[str | int] | None = None,
        umask: int = -1,
        pipesize: int = -1,
        process_group: int | None = None
    ) -> subprocess.CompletedProcess[str] | None: ...

    @overload
    def _run(
        self,
        args: str | FSPath | Sequence[str | FSPath],
        bufsize: int = -1,
        executable: str | os.PathLike | None = None,
        stdin: IO | None = None,
        stdout: IO | None = None,
        stderr: IO | None = None,
        preexec_fn: Callable[[], object] | None = None,
        close_fds: bool = True,
        shell: bool = False,
        cwd: str | os.PathLike | None = None,
        env: dict[str, str] | None = None,
        universal_newlines: bool | None = None,
        startupinfo: Any = None,
        creationflags: int = 0,
        restore_signals: bool = True,
        start_new_session: bool = False,
        pass_fds: Collection[int] = (),
        *,
        capture_output: bool = False,
        check: bool = False,
        encoding: str | None = None,
        errors: str,
        input: str | None = None,
        text: bool | None = None,
        timeout: float | None = None,
        user: str | int | None = None,
        group: str | int | None = None,
        extra_groups: Iterable[str | int] | None = None,
        umask: int = -1,
        pipesize: int = -1,
        process_group: int | None = None
    ) -> subprocess.CompletedProcess[str] | None: ...

    @overload
    def _run(
        self,
        args: str | FSPath | Sequence[str | FSPath],
        bufsize: int = -1,
        executable: str | os.PathLike | None = None,
        stdin: IO | None = None,
        stdout: IO | None = None,
        stderr: IO | None = None,
        preexec_fn: Callable[[], object] | None = None,
        close_fds: bool = True,
        shell: bool = False,
        cwd: str | os.PathLike | None = None,
        env: dict[str, str] | None = None,
        *,
        universal_newlines: Literal[True],
        startupinfo: Any = None,
        creationflags: int = 0,
        restore_signals: bool = True,
        start_new_session: bool = False,
        pass_fds: Collection[int] = (),
        capture_output: bool = False,
        check: bool = False,
        encoding: str | None = None,
        errors: str | None = None,
        input: str | None = None,
        text: Literal[True] | None = None,
        timeout: float | None = None,
        user: str | int | None = None,
        group: str | int | None = None,
        extra_groups: Iterable[str | int] | None = None,
        umask: int = -1,
        pipesize: int = -1,
        process_group: int | None = None
    ) -> subprocess.CompletedProcess[str] | None: ...

    @overload
    def _run(
        self,
        args: str | FSPath | Sequence[str | FSPath],
        bufsize: int = -1,
        executable: str | os.PathLike | None = None,
        stdin: IO | None = None,
        stdout: IO | None = None,
        stderr: IO | None = None,
        preexec_fn: Callable[[], object] | None = None,
        close_fds: bool = True,
        shell: bool = False,
        cwd: str | os.PathLike | None = None,
        env: dict[str, str] | None = None,
        universal_newlines: Literal[False] | None = None,
        startupinfo: Any = None,
        creationflags: int = 0,
        restore_signals: bool = True,
        start_new_session: bool = False,
        pass_fds: Collection[int] = (),
        *,
        capture_output: bool = False,
        check: bool = False,
        encoding: None = None,
        errors: None = None,
        input: Buffer | None = None,
        text: Literal[False] | None = None,
        timeout: float | None = None,
        user: str | int | None = None,
        group: str | int | None = None,
        extra_groups: Iterable[str | int] | None = None,
        umask: int = -1,
        pipesize: int = -1,
        process_group: int | None = None
        ) -> subprocess.CompletedProcess[bytes] | None: ...

    def _run(
        self,
        args: str | FSPath | Sequence[str | FSPath],
        bufsize: int = -1,
        executable: str | os.PathLike | None = None,
        stdin: IO | None = None,
        stdout: IO | None = None,
        stderr: IO | None = None,
        preexec_fn: Callable[[], object] | None = None,
        close_fds: bool = True,
        shell: bool = False,
        cwd: str | os.PathLike | None = None,
        env: dict[str, str] | None = None,
        universal_newlines: bool | None = None,
        startupinfo: Any = None,
        creationflags: int = 0,
        restore_signals: bool = True,
        start_new_session: bool = False,
        pass_fds: Collection[int] = (),
        *,
        capture_output: bool = False,
        check: bool = False,
        encoding: str | None = None,
        errors: str | None = None,
        input: str | Buffer | None = None,
        text: bool | None = None,
        timeout: float | None = None,
        user: str | int | None = None,
        group: str | int | None = None,
        extra_groups: Iterable[str | int] | None = None,
        umask: int = -1,
        pipesize: int = -1,
        process_group: int | None = None
    ) -> subprocess.CompletedProcess[Any] | None:
        center_title("Run Command")
        print_dividing_line()
        if isinstance(args, Sequence):
            print("Command:")
            print(shlex.join((i if isinstance(i, str) else str(i)) for i in args))
        else:
            print("Command:")
            print(args)
        print_dividing_line()
        start_time = time.monotonic_ns()
        result: subprocess.CompletedProcess | None
        try:
            result = subprocess.run(
                args,
                bufsize = bufsize,
                executable = executable,
                stdin = stdin,
                stdout = stdout,
                stderr = stderr,
                preexec_fn = preexec_fn,
                close_fds = close_fds,
                shell = shell,
                cwd = cwd,
                env = env,
                universal_newlines = universal_newlines,
                startupinfo = startupinfo,
                creationflags = creationflags,
                restore_signals = restore_signals,
                start_new_session = start_new_session,
                pass_fds = pass_fds,
                encoding = encoding,
                errors = errors,
                text = text,
                timeout = timeout,
                umask = umask,
                pipesize = pipesize,
                capture_output = capture_output,
                check = check,
                input = input,
                user = user,
                group = group,
                extra_groups = extra_groups,
                process_group = process_group
            )
        except KeyboardInterrupt:
            print("User interrupted")
            result = None
        except Exception as e:
            print("Error: " + str(e))
            result = None
        finally:
            end_time = time.monotonic_ns()
            print_dividing_line()
        
        if self._print_run_statistics:
            print("Run time: " + 
                format_time_duration(
                    end_time - start_time,
                    use_abbreviation=True
                )
            )
            if result is not None:
                print(f"Exit code: {result.returncode}")

        return result
    
    def create(self, env_name: str) -> int | None:
        """
        Create a new virtual environment.

        :param env_name: The name of the virtual environment.
        :return: process return code.
        """
        path = Path(self._base_dir / env_name)
        path.mkdir(parents=True, exist_ok=True)
        result = self._run(
            [
                "python",
                "-m",
                "venv",
                str(self._venv_path(env_name)),
                "--prompt",
                env_name
            ],
            cwd = str(self._base_dir / env_name),
        )
        if result is not None:
            return result.returncode
    
    def init_venv(self, env_name: str) -> int | None:
        """
        Initialize a virtual environment.

        :param env_name: The name of the virtual environment.
        :return: process return code.
        """
        result = self._run(
            [
                str(self._bin_dir_path(env_name) / self._python_executable_name),
                str(self._base_dir / env_name / "init.py"),
                "--base-dir",
                str(self._base_dir),
            ],
            cwd = str(self._base_dir / env_name),
        )
        if result is not None:
            return result.returncode
    
    def install(self, env_name: str, package: str, uninstall: bool = False) -> int | None:
        """
        Install or uninstall a package in the virtual environment.

        :param env_name: The name of the virtual environment.
        :param package: The package to install or uninstall.
        :param uninstall: Whether to uninstall the package.
        :return: None
        """
        result = self._run(
            [
                str(self._bin_dir_path(env_name) / self._pip_executable_name),
                "install" if not uninstall else "uninstall",
                package,
            ]
        )
        if result is not None:
            return result.returncode

    def freeze(self, env_name: str, output_file: str | None = None, encoding: str = "utf-8") -> str | None:
        """
        Freeze the packages in the virtual environment.
        
        :param env_name: The name of the virtual environment.
        :param output_file: The file to write the frozen packages to.
        :param encoding: The encoding to use when writing the frozen packages to a file.
        :return: The frozen packages as a string.
        """
        result = self._run(
            [
                str(self._bin_dir_path(env_name) / self._pip_executable_name),
                "freeze",
            ],
            text = True,
            capture_output = True,
        )
        if result is not None:
            if output_file is not None:
                with open(output_file, "w", encoding = encoding) as f:
                    f.write(result.stdout)
            
            return result.stdout
    
    def install_for_requirements(self, env_name: str, requirements_file: str = "./requirements.txt") -> int | None:
        """
        Install the packages specified in the requirements file.

        :param env_name: The name of the virtual environment.
        :param requirements_file: The file containing the list of packages to install.
        :return: process return code.
        """
        result = self._run(
            [
                str(self._bin_dir_path(env_name) / self._pip_executable_name),
                "install",
                "-r",
                requirements_file
            ]
        )
        if result is not None:
            return result.returncode
    
    def shell(self, env_name: str) -> int | None:
        """
        Activate the virtual environment.

        :param env_name: The name of the virtual environment.
        :return: process return code.
        """
        result = self._run(
            ["bash", "--init-file", str(self._bin_dir_path(env_name) / "activate")],
            env = self._envs
        )
        if result is not None:
            return result.returncode
    
    def repl(self, env_name: str) -> int | None:
        """
        Start the Python REPL.

        :param env_name: The name of the virtual environment.
        :return: process return code.
        """
        result = self._run(
            [str(self._bin_dir_path(env_name) / self._python_executable_name)],
            env = self._envs
        )
        if result is not None:
            return result.returncode
    
    def exec_code(self, env_name: str, script_path: str) -> int | None:
        """
        Execute a Python script.

        :param env_name: The name of the virtual environment.
        :param script_path: The path to the Python script.
        :return: process return code.
        """
        result = self._run(
            [str(self._bin_dir_path(env_name) / self._python_executable_name), script_path],
            env = self._envs
        )
        if result is not None:
            return result.returncode
