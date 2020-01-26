"""
********************************************************************************
compas_testing.gom
********************************************************************************

.. currentmodule:: compas_testing.gom

Import/Export
=============

.. autosummary::
    :toctree: generated/
    :nosignatures:

    results_to_list
    group_per_stage
    group_per_gkey
    find_points_between_stages
    find_points_from_stage
    history_to_json

Clean Results
=============

.. autosummary::
    :toctree: generated/
    :nosignatures:

    find_corrupted_stages
    find_corrupted_points
    remove_points_from_results
    split_results

Evaluate Results
================

.. autosummary::
    :toctree: generated/
    :nosignatures:

    find_abs_max_displacement
    evaluate_displacements

"""

from .convert import *
from .clean import *
from .evaluate import *

__all__ = [name for name in dir() if not name.startswith('_')]
