import math


__author__     = 'Francesco Ranaudo'
__copyright__  = 'Copyright 2020, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'ranaudo@arch.ethz.ch'


__all__ = ['double_punch',
           ]


def double_punch(Ncr, D, h, p=37.5):
    """
    Converts the results of double punch test of a concrete cube to the corresponding tension capacity.

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


# ******************************************************************************
#   Main
# ******************************************************************************

if __name__ == "__main__":
    pass
