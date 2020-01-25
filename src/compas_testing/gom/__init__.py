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

    results_per_stage
    history_to_json
    group_per_stage
    group_per_gkey
    find_points
    find_points_0
    split_points_history
____


Plot in rhino
=============

.. autosummary::
    :toctree: generated/
    :nosignatures:

    read_json
    find_0_stages
    find_0_points
    key_to_listcoord
    get_test_key
    displ_dic
    sliced_dict
    find_max_val
    scaled_val_dic
    x_rgb
    draw_stages_colour
    draw_stages
    del_key_in_dict
    point_trajectory
    find_rhpoint_key
____


"""

from .in_out import *
from .rhino import *

__all__ = [name for name in dir() if not name.startswith('_')]