from .__about__ import __version__

__doc__ = f"""
~| Quasar Code - Python Package |~

Adds functionality to Python along with wrapers for existing modules for ease of use

Credits:
    Written by Christopher Rowe
    Notable contribusions taken from code written by Tim Greenshaw 10/2018

Version: {__version__}
"""

from ._global_settings import settings_object as Settings

from . import edp

from . import Games

from . import IO

from . import MPI

from . import Science

from . import Tools

from .Tools._directorys_and_imports import source_file_relitive_add_to_path
from .IO.Text import Console, Stopwatch
from .edp import Event
from .Tools._async import start_main_async
