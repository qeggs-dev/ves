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