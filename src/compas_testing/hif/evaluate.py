import math


__author__     = 'Francesco Ranaudo'
__copyright__  = 'Copyright 2020, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'ranaudo@arch.ethz.ch'


__all__ = ['double_punch',
           'compute_stress_strain'
           ]


def double_punch(Ncr, D, h, p=37.5):
    """
    Converts the results of a double punch test of a concrete cube to the corresponding tension capacity.

    Parameters
    ----------
    Ncr: float - max compression force from the test
    
    D: float - DOUBLE CHECK!
    
    h : float - DOUBLE CHECK!

    P: float - DOUBLE CHECK!

    Returns
    -------
    fct : float - concrete tension capacity

    """
    fct = 4*10**3*Ncr / (math.pi*(2.4*D*h-p**2))
    return fct


def compute_stress_strain(pd_data):
    """
    Converts the results of a compression test of a concrete cube to the corresponding stress-strain curve.

    Parameters
    ----------
    pd_data: pandas dataframe - dataframe containing the results of the test
    

    Returns
    -------
    pd_data : pandas dataframe - dataframe containing the results of the test with additional columns
    for strees and strain

    """
    # pd_data['Stress'] = pd_data['Forc']
    
    # sigma = force/area
    # epsilon = deformation/height
    # return 
    pass


# ******************************************************************************
#   Main
# ******************************************************************************

if __name__ == "__main__":
    pass
