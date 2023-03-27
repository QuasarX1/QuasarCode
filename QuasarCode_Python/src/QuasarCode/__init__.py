"""
~| Quasar Code - Python Package |~

Adds functionality to Python along with wrapers for existing modules for ease of use

Credits:
    Written by Christopher Rowe
    Notable contribusions taken from code written by Tim Greenshaw 10/2018

Version: 0.7.1
"""

from ._global_settings import settings_object as Settings

from . import edp

from . import Games

from . import IO

from . import MPI

from . import Science

from . import Tools

from .Tools._directorys_and_imports import source_file_relitive_add_to_path
from .IO.Text.console import pause as console_pause
from .IO.Text import console
from .edp import Event
from .Tools._async import start_main_async
