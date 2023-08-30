import numpy as np
from math import log10 as log

shadow_loss = []


def create_shadowloss(x):
    arry = np.random.normal(0, 2, int(x / 10))
    for elmnt in arry:
        shadow_loss.append(elmnt)


def propagation_loss(freq, loc, antenna_height, height_user):
    '''
    Calculating propagation loss according to Okamura-Hata model for small city
    '''
    ahm = (1.1 * log(freq) - 0.7) * \
        height_user - (1.56 * log(freq) - 0.8)
    oka_hata_loss = 69.55 + 26.16 * log(freq) - 13.82 * \
        log(antenna_height) - ahm + (
        44.9 - 6.55 * log(antenna_height)) * log(loc / 1000)
    return oka_hata_loss


def fading():
    ''' calculating the second deepest fade in dB'''
    a = np.random.normal(0, (1 / np.sqrt(2)), 10)
    # generating real part of Gaussian Distribution for Rayleigh Distribution
    b = np.random.normal(0, (1 / np.sqrt(2)), 10)
    # generating immaginary part of Gaussian Distribution for Rayleigh
    fade = np.abs(a + b * (1j)).tolist()
    return 20 * log(sorted(fade)[-2])


def shadowing(loc):
    return shadow_loss[int(loc / 10) - 1]


def penetration(loc, node, x):
    if node == 1:
        if loc < (x - 200):
            pen_loss = 0
        elif (x - 200) <= loc <= (x - 190):
            pen_loss = 21 * (loc - (x - 200)) / 10
        else:
            pen_loss = 21
    else:
        if loc < (x - 200):
            pen_loss = 21
        elif (x - 200) <= loc <= (x - 190):
            pen_loss = 21 * ((x - 190) - loc) / 10
        else:
            pen_loss = 0
    return pen_loss


def RSL(freq, x, loc, height_bs, height_sc, height_user, EIRP_bs, EIRP_sc):
    # Base Station
    RSL_bs = EIRP_bs - \
        propagation_loss(freq, loc, height_bs, height_user) - \
        fading() + shadowing(loc) - penetration(loc, 1, x)
    # Small Cell
    RSL_sc = EIRP_sc - \
        propagation_loss(freq, (x - loc), height_sc, height_user) \
        - fading() - penetration(loc, 0, x)
    return RSL_bs, RSL_sc