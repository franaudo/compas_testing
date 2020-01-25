"""
********************************************************************************
compas_testing
********************************************************************************

.. currentmodule:: compas_testing


.. toctree::
    :maxdepth: 1


"""

from __future__ import print_function

import os
import sys


__author__ = ["Francesco Ranaudo"]
__copyright__ = "BlockResearchGroup"
__license__ = "MIT License"
__email__ = "ranaudo@arch.ethz.ch"
__version__ = "0.1.0"


HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, "../../"))
DATA = os.path.abspath(os.path.join(HOME, "data"))
DOCS = os.path.abspath(os.path.join(HOME, "docs"))
TEMP = os.path.abspath(os.path.join(HOME, "temp"))


__all__ = ["HOME", "DATA", "DOCS", "TEMP"]
