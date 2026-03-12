import subprocess
from pathlib import Path
from ._base import BaseVES as VESBase

class VES_Windows(VESBase):
    def __init__(
            self,
            base_dir: Path = Path.cwd() / "envs",
            print_run_statistics: bool = False,
            venv_dir: str = ".venv",
            python_executable_name: str = "python.exe",
            pip_executable_name: str = "pip.exe"
        ):
        super().__init__(
            base_dir,
            print_run_statistics,
            venv_dir,
            python_executable_name,
            pip_executable_name
        )
    
    def _bin_dir_path(self, env_name: str) -> Path:
        return self._venv_path(env_name) / "Scripts"
    
    def shell(self, env_name: str) -> int | None:
        """
        Activate the virtual environment.

        :param env_name: The name of the virtual environment.
        :return: process return code.
        """
        result = self._run(
            ["powershell", "-NoLogo", "-NoExit", "-File", str(self._bin_dir_path(env_name) / "activate.ps1")],
            env = self._envs
        )
        if result is not None:
            return result.returncode