import subprocess
from pathlib import Path
from ._base import BaseVES as VESBase

class VES_Linux(VESBase):
    def _bin_dir_path(self, env_name: str) -> Path:
        self._venv_path(env_name) / "bin"