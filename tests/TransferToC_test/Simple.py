from ...Main.Modules import make_modules
from ...Main.TransferToC import transfer_to_c
from ...Main.Settings import settings_load
from pathlib import Path
import subprocess


settings = settings_load()
compiler = settings['compiler']


def transfer(enter_path: Path, resul_path: Path):
    module = make_modules(enter_path)
    transfer_to_c(module, resul_path, compiler)


def execute(path: Path) -> subprocess.CompletedProcess:
    result = subprocess.run(
        [path.as_posix()], capture_output=True, text=True
    )
    return result
