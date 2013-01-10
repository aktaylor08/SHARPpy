''' Frequently used functions '''
import numpy as np
import numpy.ma as ma
from sharppy.sharptab.constants import MISSING, TOL

__all__ = ['MS2KTS', 'KTS2MS', 'MS2MPH', 'MPH2MS', 'MPH2KTS', 'KTS2MPH']
__all__ += ['M2FT', 'FT2M']


def MS2KTS(val):
    '''
    Convert meters per second to knots

    Parameters
    ----------
    val : float
        Speed (m/s)

    Returns
    -------
    Val converted to knots (float)

    '''
    return val * 1.94384449


def KTS2MS(val):
    '''
    Convert knots to meters per second

    Parameters
    ----------
    val : float
        Speed (kts)

    Returns
    -------
        Val converted to meters per second (float)

    '''
    return val * 0.514444


def MS2MPH(val):
    '''
    Convert meters per second to miles per hour

    Parameters
    ----------
    val : float
        Speed (m/s)

    Returns
    -------
    Val converted to miles per hour (float)

    '''
    return val * 2.23694


def MPH2MS(val):
    '''
    Convert miles per hour to meters per second

    Parameters
    ----------
    val : float
        Speed (mph)

    Returns
    -------
    Val converted to meters per second (float)

    '''
    return val * 0.44704


def MPH2KTS(val):
    '''
    Convert miles per hour to knots

    Parameters
    ----------
    val : float
        Speed (mph)

    Returns
    -------
    Val converted to knots (float)

    '''
    return val * 0.868976


def KTS2MPH(val):
    '''
    Convert knots to miles per hour

    Parameters
    ----------
    val : float
        Speed (kts)

    Returns
    -------
    Val converted to miles per hour (float)

    '''
    return val * 1.15078


def M2FT(val):
    '''
    Convert meters to feet

    Parameters
    ----------
    val : float
        Distance (m)

    Returns
    -------
        Val converted to feet (float)

    '''
    return val * 3.2808399


def FT2M(val):
    '''
    Convert feet to meters

    Parameters
    ----------
    val : float
        Distance (ft)

    Returns
    -------
        Val converted to meters (float)

    '''
    return val * 0.3048


def _vec2comp(wdir, wspd):
    '''
    Underlying function that converts a vector to its components

    Parameters
    ----------
    wdir : number, masked_array
        Angle in meteorological degrees
    wspd : number, masked_array
        Magnitudes of wind vector

    Returns
    -------
    u : number, masked_array (same as input)
        U-component of the wind
    v : number, masked_array (same as input)
        V-component of the wind

    '''
    u = wspd * ma.sin(np.radians(wdir % 360.)) * -1
    v = wspd * ma.cos(np.radians(wdir % 360.)) * -1
    return u, v


def vec2comp(wdir, wspd, missing=MISSING):
    '''
    Convert direction and magnitude into U, V components

    Parameters
    ----------
    wdir : number, array_like
        Angle in meteorological degrees
    wspd : number, array_like
        Magnitudes of wind vector (input units == output units)
    missing : number (optional)
        Optional missing parameter. If not given, assume default missing
        value from sharppy.sharptab.constants.MISSING

    Returns
    -------
    u : number, array_like (same as input)
        U-component of the wind (units are the same as those of input speed)
    v : number, array_like (same as input)
        V-component of the wind (units are the same as those of input speed)

    '''
    wdir = ma.asanyarray(wdir).astype(np.float64)
    wspd = ma.asanyarray(wspd).astype(np.float64)
    wdir.set_fill_value(missing)
    wspd.set_fill_value(missing)
    assert wdir.shape == wspd.shape, 'wdir and wspd have different shapes'
    if wdir.shape:
        wdir[wdir == missing] = ma.masked
        wspd[wspd == missing] = ma.masked
        wdir[wspd.mask] = ma.masked
        wspd[wdir.mask] = ma.masked
        u, v = _vec2comp(wdir, wspd)
        u[np.fabs(u) < TOL] = 0.
        v[np.fabs(v) < TOL] = 0.
    else:
        if wdir == missing:
            wdir = ma.masked
            wspd = ma.masked
        elif wspd == missing:
            wdir = ma.masked
            wspd = ma.masked
        u, v = _vec2comp(wdir, wspd)
        if ma.fabs(u) < TOL:
            u = 0.
        if ma.fabs(v) < TOL:
            v = 0.
    return u, v




