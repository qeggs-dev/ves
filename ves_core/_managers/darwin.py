import subprocess
from pathlib import Path
from .base import BaseVES as VESBase

class VES_Darwin(VESBase):
    def _bin_dir_path(self, env_name: str) -> Path:
        return self._venv_path(env_name) / "bin"