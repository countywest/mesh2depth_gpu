import os
import platform

if platform.system().lower() == "linux":
    os.environ["PYOPENGL_PLATFORM"] = "egl"

from .convert import convert
from .version import __version__
