import numpy as np
import matplotlib.pyplot as pl
from math import log10 as log

shadow_loss = np.random.normal(0, 2, 300)


def propagation_loss(freq, distance, antenna_height, height_user):
    '''
    Calculating propagation loss according to Okamura-Hata model for small city
    '''
    ahm = (1.1 * log(freq) - 0.7) * \
        height_user - (1.56 * log(freq) - 0.8)
    oka_hata_loss = 69.55 + 26.16 * log(freq) - 13.82 * \
        log(antenna_height) - ahm + (
        44.9 - 6.55 * log(antenna_height)) * log(distance / 1000)
    return oka_hata_loss


def fading():
    ''' calculating the second deepest fase in dB'''
    a = np.random.normal(0, .707, 10)
    # generating real part of Gaussian Distribution for Rayleigh Distribution
    b = np.random.normal(0, .707, 10)
    # generating immaginary part of Gaussian Distribution for Rayleigh
    fade = np.abs(a + b * (1j)).tolist()
    return 20 * log(sorted(fade)[-2])


def shadowing(distance):
    return shadow_loss[int(distance / 10) - 1]


def penetration(distance, id):
    if id == 'bs':
        if distance < 2800:
            pen_loss = 0
        elif 2800 <= distance <= 2810:
            pen_loss = 21 * (distance - 2800) / 10
        else:
            pen_loss = 21
    else:
        if distance < 2800:
            pen_loss = 21
        elif 2800 <= distance <= 2810:
            pen_loss = 21 * (2810 - distance) / 10
        else:
            pen_loss = 0
    return pen_loss


def RSL(freq, distance1, height_bs, height_sc, height_user, EIRP_bs, EIRP_sc):
    bs_lst = []
    sc_lst = []
    dist = []
    file = open("RSL.txt", "w+")
    for distance in range(1, 3000):
        # Base Station
        RSL_bs = EIRP_bs - \
            propagation_loss(freq, distance, height_bs, height_user) - \
            fading() + shadowing(distance) - penetration(distance, 'bs')
        # Small Cell
        RSL_sc = EIRP_sc - \
            propagation_loss(freq, (3000 - distance), height_sc, height_user) \
            - fading() - penetration(distance, 'sc')
        file.write('Distance: {}, RSL_bs: {}, RSL_sc: {}\n'.format(
            distance, RSL_bs, RSL_sc))
        bs_lst.append(RSL_bs)
        sc_lst.append(RSL_sc)
        dist.append(distance)
    pl.plot(dist, bs_lst, 'b-')
    pl.plot(dist, sc_lst, 'r-')
    pl.xlabel('Distance ( in meters)', fontsize=10)
    pl.ylabel('RSL (in dBm)', fontsize=10)
    pl.title('RSL Value of Base Station and Small Cell', fontsize=15)
    pl.grid()
    pl.show()
    file.close()


if __name__ == "__main__":
    EIRP_bs = 57
    EIRP_sc = 30
    height_bs = 50
    height_sc = 10
    height_user = 1.7
    freq = 1000
    RSL(freq, 2100, height_bs, height_sc, height_user, EIRP_bs, EIRP_sc)