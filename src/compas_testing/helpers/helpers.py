
import json

__author__     = 'Francesco Ranaudo'
__copyright__  = 'Copyright 2020, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'ranaudo@arch.ethz.ch'

all = ['read_json',
       'base_round',
       'key_to_coordinates',
       'get_test_key'
       'normalise_dict',
       'ratio_to_rgb', 
    ]


# ******************************************************************************
#   Math
# ******************************************************************************

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


def normalise_dict(input_dict, factor):

    """
    Create a dictionary in which all values are scaled by a given factor

    Parameters
    ----------
    dic : dictionary 
        key: -
        value : list - a list of scalars

    factor : float or str - scalar used to scale values. if set to "max" normalise with respect
    to the maximum

    Returns
    -------
    output_dict : dict 
        key: str - same key as the input dictionary
        value : list - a list of scalars obtained by dividing the input values by the factor
    
    """

    output_dict = input_dict
    for key, value in output_dict.items():
        if factor == 'max':
            output_dict[key] = [float(i)/max(value) for i in value]
        else:
            output_dict[key] = [float(i)/factor for i in value]

    return output_dict


# ******************************************************************************
#   mix
# ******************************************************************************

def key_to_coordinates(key):
    """
    Converts point keys into XYZ coordinates

    Parameters
    ----------
    key: string - the coordinates of a point in initial stage

    Returns
    -------
    coord : tuple - XYZ coordinates of a point in 3D space
        
    """
    stripkey = key.strip("(").strip(")").split(", ")
    point_coordinates = tuple(float(elem) for elem in stripkey)
    return point_coordinates


def get_test_key(points_history): # TODO: remove after development
    """
    Get a random key to test a function.

    Parameters
    ----------
    points_history : dict

    Returns
    -------
    random_key : variable - a key in the dictionary
        
    """

    import random
    random_key = random.choice(list(points_history.keys()))

    return random_key


# ******************************************************************************
#   json
# ******************************************************************************

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


# ******************************************************************************
#   Visualization
# ******************************************************************************

def ratio_to_rgb(ratio):

    """
    Converts a ratio between 0 and 1 into an rgb color

    Parameters
    ----------
    ratio : float - scalar number between 0 and 1

    Returns
    -------
    rgb : tuple - rgb color 
    
    """
    b = 0
    if round(ratio, 1) == 0.5:
        r = 255
        g = 255
    elif ratio < 0.5:
        r = int(ratio * 2 * 255.0)
        g = 255
    else:
        r = 255
        g = int((1.0 - ratio) * 2 * 255.0)
    rgb = (r, g, b)

    return rgb

# ******************************************************************************
#   Main
# ******************************************************************************

if __name__ == "__main__":
    
    import compas_testing
    from compas_testing.helpers import normalise_dict

    d = {'a':[0, 10, 5.2, 4], 'b':[2,4,6,1,15.3]}
    dn = normalise_dict(d, 'max')
    print(dn)
