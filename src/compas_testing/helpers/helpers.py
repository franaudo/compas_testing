
import json

__author__     = 'Francesco Ranaudo'
__copyright__  = 'Copyright 2020, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'ranaudo@arch.ethz.ch'

all = ['read_json',
       'base_round', 
    ]

def base_round(x, base):
    """
    Custom multiple rounding function.

    Parameters
    ----------
    x : float, number to be rounded
    base: base used to round the number

    Returns
    -------
    int : rounded number
    """

    return base * round(x/base)

    
def read_json(file):
    """
    Reads a json file and returns a dictionary.

    Parameters
    ----------
    file : json file
        A json file with collected data.

    Returns
    -------
    data : dictionnary with data formatted into keys and values
        
    """

    with open(file, 'r') as fp:
        data = json.load(fp)
    return data