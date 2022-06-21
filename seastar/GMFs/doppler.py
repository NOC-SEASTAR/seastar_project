#!/usr/bin/env python
# coding=utf-8
"""
"""

import numpy as np
from scipy.constants import c  # speed of light in vacuum


# import pdb


def cdop_func(x):
    """
    """
    return 1. / (1. + np.exp(-x))


def mouche12(u10, phi, inc, pol):
    """
    """
    # Check inputs
    sizes = np.array([np.size(inc), np.size(u10), np.size(phi)])
    size = sizes.max()
    if ((sizes != size) & (sizes != 1)).any():
        raise Exception('Inputs sizes do not agree.')
    if pol not in ['VV', 'HH']:
        raise Exception('Unknown polarisation : ' + pol)
    # NN coefficients (W=weights and B=biases)
    # (coefficient names in mouche2012 are given)
    if pol == 'VV':
        # lambda[0:2,1]
        B1 = np.array([-0.343935744939, 0.108823529412, 0.15],
                      dtype='float32')
        # lambda[0:2,0]
        W1 = np.array([0.028213254683, 0.0411764705882, .00388888888889],
                      dtype='float32')
        # omega[i,0]
        B2 = np.array([14.5077150927, -11.4312028555, 1.28692747109,
                       -1.19498666071, 1.778908726, 11.8880215573,
                       1.70176062351, 24.7941267067, -8.18756617111,
                       1.32555779345, -9.06560116738],
                      dtype='float32')
        # omega[i,[3,2,1]]
        W2 = np.array([[19.7873046673, 22.2237414308, 1.27887019276],
                       [2.910815875, -3.63395681095, 16.4242081101],
                       [1.03269004609, 0.403986575614, 0.325018607578],
                       [3.17100261168, 4.47461213024, 0.969975702316],
                       [-3.80611082432, -6.91334859293, -0.0162650756459],
                       [4.09854466913, -1.64290475596, -13.4031862615],
                       [0.484338480824, -1.30503436654, -6.04613303002],
                       [-11.1000239122, 15.993470129, 23.2186869807],
                       [-0.577883159569, 0.801977535733, 6.13874672206],
                       [0.61008842868, -0.5009830671, -4.42736737765],
                       [-1.94654022702, 1.31351068862, 8.94943709074]],
                      dtype='float32')
        # gamma[0]
        B3 = np.array(4.07777876994, dtype='float32')
        # gamma[1:11]
        W3 = np.array([7.34881153553, 0.487879873912, -22.167664703,
                       7.01176085914, 3.57021820094, -7.05653415486,
                       -8.82147148713, 5.35079872715, 93.627037987,
                       13.9420969201, -34.4032326496],
                      dtype='float32')
        # beta
        B4 = np.array(-52.2644487109, dtype='float32')
        # alpha
        W4 = np.array(111.528184073, dtype='float32')
    elif pol == 'HH':
        # lambda[0:2,1]
        B1 = np.array([-0.342097701547, 0.118181818182, 0.15],
                      dtype='float32')
        # lambda[0:2,0]
        W1 = np.array([0.0281843837385, 0.0318181818182, 0.00388888888889],
                      dtype='float32')
        # omega[i,0]
        B2 = np.array([1.30653883096, -2.77086154074, 10.6792861882,
                       -4.0429666906, -0.172201666743, 20.4895916824,
                       28.2856865516, -3.60143441597, -3.53935574111,
                       -2.11695768022, -2.57805898849],
                      dtype='float32')
        # omega[i,[3,2,1]]
        W2 = np.array([[-2.61087309812, -0.973599180956, -9.07176856257],
                       [-0.246776181361, 0.586523978839, -0.594867645776],
                       [17.9261562541, 12.9439063319, 16.9815377306],
                       [0.595882115891, 6.20098098757, -9.20238868219],
                       [-0.993509213443, 0.301856868548, -4.12397246171],
                       [15.0224985357, 17.643307099, 8.57886720397],
                       [13.1833641617, 20.6983195925, -15.1439734434],
                       [0.656338134446, 5.79854593024, -9.9811757434],
                       [0.122736690257, -5.67640781126, 11.9861607453],
                       [0.691577162612, 5.95289490539, -16.0530462],
                       [1.2664066483, 0.151056851685, 7.93435940581]],
                      dtype='float32')
        # gamma[0]
        B3 = np.array(2.68352095337, dtype='float32')
        # gamma[1:11]
        W3 = np.array([-8.21498722494, -94.9645431048, -17.7727420108,
                       -63.3536337981, 39.2450482271, -6.15275352542,
                       16.5337543167, 90.1967379935, -1.11346786284,
                       -17.57689699, 8.20219395141],
                      dtype='float32')
        # beta
        B4 = np.array(-66.9554922921, dtype='float32')
        # alpha
        W4 = np.array(136.216953823, dtype='float32')
    # Make inputs as a single matrix (and clip phi in [0,180])
    inputs = np.zeros((3, size), dtype='float32')
    for ivar, var in enumerate((inc, u10, phi)):
        if sizes[ivar] == 1:
            inputs[ivar, :] = np.repeat(var, size)
        else:
            inputs[ivar, :] = np.ravel(var)
        if ivar == 2:
            inputs[ivar, :] = np.abs(((inputs[ivar, :] + 180) % 360) - 180)
        inputs[ivar, :] *= W1[ivar]
        inputs[ivar, :] += B1[ivar]
    # Compute CDOP
    B2 = np.tile(B2.reshape((11, 1)), (1, size))
    dop = W4 * cdop_func(np.dot(W3, cdop_func(np.dot(W2, inputs) + B2)) + B3) + B4
    # Reshape output
    # (using the shape of input which have the maximum ndim)
    ndims = np.array([np.ndim(inc), np.ndim(u10), np.ndim(phi)])
    tmp = np.where(sizes == size)[0]
    ivar = tmp[ndims[tmp].argmax()]
    shp = np.shape((inc, u10, phi)[ivar])
    dop = dop.reshape(shp)
    return dop


def convertDoppler2Velocity(freq_GHz, dop, inci):
    """
    """
    if 100 < freq_GHz < 0.1:
        raise Exception('Inputs freq_GHz should be in GHz, e.g. C-band: 5.5;\
                X-band 9.55; Ku-band 13.6')
    n = 1.000293
    c_air = c / n;
    wavelength = c_air / freq_GHz / 1e9;
    los_vel = -dop * wavelength / 2;
    surf_vel = los_vel / np.sin(inci * np.pi / 180.);
    return los_vel, surf_vel


# =======================================================================
def yurovsky19(theta,  # Incidence angle, 0...65 [deg]
               phi,  # Radar-to-wave(wind) azimuth, 0...180 [deg], (0 deg is upwind)
               u,  # Wind Speed at 10m-height, 3...15 [m/s]
               # Optional parameters:
               # WARNING
               # swh = 0.22*u**2/g,    # wind sea significant wave height [m], PM by
               # default WARNING swh was commented in Yuri version
               # WARNING omega was commented in Yuri version
               # omega = 0.83*g/u,     # wind sea peak radial frequency [rad/s], PM by default
               # WARNING
               swh_sw=0,  # swell significant wave height [m], 0 by default
               # (note SWH=sqrt(8)*a, where a is the wave amplitude)
               omega_sw=0,  # swell peak radial frequency [rad/m], 0 by default
               phi_sw=0,  # radar-to-swell azimuth [deg], 0 by default
               drift=0.015,  # wind drift coefficient, 1.5%U by default
               lambdar=0.008,  # radar wavelength [m], Ka-band by default
               beta_ws=0.20,  # 3rd moment of Wind Sea spectrum (Pierson-Moskowitz) parameter
               beta_sw=0.0625,  # 3rd moment of SWell spectrum parameter
               zerocrosswind=False,  # if this parameter set to 1,
               # the MTFwindsea is replaced by MTFswell (crosswind is zeroed)
               **kwargs):
    # KaDOP computes sea surface Doppler spectrum centroid for VV and HH
    # polarizations, DCvv and DChh, based on the empirical MTF [10.1109/TGRS.2017.2787459]
    # DC is expressed in m/s, DC[m/s]= DC[Hz]*lambda/2, where lambda is the radar wavelength.
    # By default, the DC is estimated for Pierson-Moskowitz (PM),[10.1029/JZ069i024p05181]
    # wind sea spectrum without swell. If significant wave height (SWH)
    # and peak frequency (omega) are known, they can be specified explicitly.
    # Swell can be added independently by specifying its SWH and omega,
    # no swell by default.

    cosd = lambda x: np.cos(x * np.pi / 180)
    sind = lambda x: np.sin(x * np.pi / 180)
    acosd = lambda x: np.arccos(x) * 180 / np.pi
    sech = lambda x: 1 / np.cosh(x * np.pi / 180)

    # =======================================================================
    def MTF(theta, phi, u, C):
        # evaluate complex MTF using C-coefficients
        # 1st column of C-matrix is Bijk, 2nd column is Cijk from Equation (A1),
        # Table A1 or A2

        # =======================================================================
        def evalfun(theta, phi, u, C):
            # evaluate magnitude or phasor of MTF
            # C is column, either Bijk or Cijk

            pp = C[0] + \
                 C[1] * theta ** 1 + \
                 C[2] * theta ** 2 + \
                 C[3] * theta ** 3 + \
                 C[4] * cosd(1 * phi) + \
                 C[5] * theta ** 1 * cosd(1 * phi) + \
                 C[6] * theta ** 2 * cosd(1 * phi) + \
                 C[7] * theta ** 3 * cosd(1 * phi) + \
                 C[8] * cosd(2 * phi) + \
                 C[9] * theta ** 1 * cosd(2 * phi) + \
                 C[10] * theta ** 2 * cosd(2 * phi) + \
                 C[11] * theta ** 3 * cosd(2 * phi) + \
                 C[12] * np.log(u) ** 1 + \
                 C[13] * theta ** 1 * np.log(u) ** 1 + \
                 C[14] * theta ** 2 * np.log(u) ** 1 + \
                 C[15] * theta ** 3 * np.log(u) ** 1 + \
                 C[16] * cosd(1 * phi) * np.log(u) ** 1 + \
                 C[17] * theta ** 1 * cosd(1 * phi) * np.log(u) ** 1 + \
                 C[18] * theta ** 2 * cosd(1 * phi) * np.log(u) ** 1 + \
                 C[19] * theta ** 3 * cosd(1 * phi) * np.log(u) ** 1 + \
                 C[20] * cosd(2 * phi) * np.log(u) ** 1 + \
                 C[21] * theta ** 1 * cosd(2 * phi) * np.log(u) ** 1 + \
                 C[22] * theta ** 2 * cosd(2 * phi) * np.log(u) ** 1 + \
                 C[23] * theta ** 3 * cosd(2 * phi) * np.log(u) ** 1

            return pp
            # =======================================================================

        Mabs = evalfun(theta, phi, u, C[:, 0])
        Mphs = evalfun(theta, phi, u, C[:, 1])
        M = np.exp(Mabs) * Mphs / abs(Mphs)

        return M
        # =======================================================================

    g = 9.8  # Gravitational constant [m/s^2]
    gamma = 7.3e-5  # Surface tension [N/m]

    if 'swh' not in kwargs.keys():
        swh = 0.22 * u ** 2 / g  # Wind sea Significant Wave Height [m], PM by default
    else:
        swh = kwargs.pop('swh')

    if 'omega' not in kwargs.keys():
        omega = 0.83 * g / u  # Wind sea peak radial frequency [rad/s], PM by default
    else:
        omega = kwargs.pop('omega')

    # Set of coefficients, Table A1 and A2.
    # 1st column is Bijk, 2nd column is Cijk from Equation (A1)

    coefs = {}
    coefs["VVws"] = np.array([[+2.037368e+00, -9.991774e-01 - 1.859445e-03j], \
                              [-9.956181e-03, +9.995403e-02 - 3.728707e-02j], \
                              [+1.733240e-03, -9.495314e-04 + 5.073520e-04j], \
                              [-2.110994e-05, -1.742060e-06 + 2.930913e-06j], \
                              [-1.704388e-02, -2.062522e-03 + 4.317005e-03j], \
                              [-4.002570e-02, -2.021244e-02 + 1.328154e-01j], \
                              [+2.213287e-03, +1.037791e-03 - 5.526796e-03j], \
                              [-1.778161e-05, -1.183648e-05 + 4.932378e-05j], \
                              [-2.933537e-02, -5.651327e-05 + 1.289564e-03j], \
                              [+2.755026e-02, +7.638659e-02 + 7.101499e-02j], \
                              [+1.382417e-03, -3.141920e-03 - 2.127452e-03j], \
                              [-2.811759e-05, +3.360741e-05 + 1.363174e-05j], \
                              [-2.637003e-01, -1.300697e-03 + 6.335937e-04j], \
                              [+2.457828e-02, -1.060972e-02 + 4.969400e-03j], \
                              [-1.537867e-03, -2.108491e-05 - 1.405381e-05j], \
                              [+1.667354e-05, +2.373730e-06 - 1.623276e-06j], \
                              [+1.342060e-02, +4.740406e-04 - 8.386239e-04j], \
                              [+1.791006e-02, +9.982368e-03 - 1.343944e-02j], \
                              [-1.048575e-03, -4.634691e-04 + 1.129914e-03j], \
                              [+9.158551e-06, +5.153546e-06 - 1.134140e-05j], \
                              [+1.809446e-02, +2.879613e-04 - 3.980226e-04j], \
                              [+8.255341e-03, -2.309667e-02 - 1.347916e-02j], \
                              [-1.286835e-03, +9.359817e-04 + 5.873901e-04j], \
                              [+1.827908e-05, -1.056345e-05 - 5.154716e-06j]])

    coefs["HHws"] = np.array([[+2.038368e+00, -9.999579e-01 - 2.003675e-03j], \
                              [+6.742867e-02, +1.401092e-01 - 3.822135e-02j], \
                              [-1.544673e-03, -2.832742e-03 + 6.391936e-04j], \
                              [+1.167191e-05, +1.755927e-05 - 1.325959e-06j], \
                              [-1.716876e-02, -2.510170e-03 + 5.669125e-03j], \
                              [-2.064313e-02, -1.886127e-03 + 1.301061e-01j], \
                              [+1.172491e-03, +2.217910e-04 - 5.440821e-03j], \
                              [-6.111610e-06, -2.769183e-06 + 5.317919e-05j], \
                              [-2.939264e-02, +1.738649e-03 + 1.255492e-03j], \
                              [+4.007160e-03, +3.758102e-02 + 7.395083e-02j], \
                              [+1.482772e-03, -1.072406e-03 - 2.254102e-03j], \
                              [-2.163604e-05, +8.151756e-06 + 1.559167e-05j], \
                              [-2.643806e-01, -8.840229e-04 + 6.209692e-04j], \
                              [-1.240919e-02, -3.155538e-02 + 3.907412e-03j], \
                              [+2.162084e-04, +8.937600e-04 - 1.544636e-05j], \
                              [-3.482596e-07, -6.512207e-06 - 4.914423e-07j], \
                              [+1.347741e-02, +7.416105e-04 - 1.536552e-03j], \
                              [+7.223413e-03, -2.172061e-03 - 1.458223e-02j], \
                              [-5.037439e-04, +1.053785e-04 + 1.203955e-03j], \
                              [+2.889241e-06, -9.978940e-07 - 1.415368e-05j], \
                              [+1.812623e-02, -6.400749e-04 - 4.329797e-04j], \
                              [+2.313635e-02, -5.070167e-03 - 1.231709e-02j], \
                              [-1.569241e-03, -5.514080e-06 + 5.292689e-04j], \
                              [+1.795667e-05, +8.560235e-07 - 4.894367e-06j]])

    coefs["VVsw"] = np.array([[+2.037368e+00, -1.047849e+00 - 1.086382e-03j], \
                              [-9.956181e-03, +9.779865e-02 + 9.409557e-03j], \
                              [+1.733240e-03, -9.521228e-04 - 1.330189e-03j], \
                              [-2.110994e-05, -8.936468e-07 + 1.921637e-05j], \
                              [-1.704388e-02, -2.054076e-02 + 2.380576e-02j], \
                              [-4.002570e-02, +4.046633e-02 + 1.544692e-01j], \
                              [+2.213287e-03, -1.395978e-03 - 5.769671e-03j], \
                              [-1.778161e-05, +1.340544e-05 + 4.688263e-05j], \
                              [-2.933537e-02, -4.552795e-03 - 3.923333e-03j], \
                              [+2.755026e-02, +2.273467e-02 + 1.289799e-02j], \
                              [+1.382417e-03, -8.407162e-04 + 1.345284e-05j], \
                              [-2.811759e-05, +9.080283e-06 - 3.645146e-06j], \
                              [-2.637003e-01, +4.449188e-03 + 1.717938e-03j], \
                              [+2.457828e-02, -1.171622e-02 - 2.045575e-03j], \
                              [-1.537867e-03, +9.499907e-05 + 4.015526e-04j], \
                              [+1.667354e-05, +8.816342e-07 - 5.631314e-06j], \
                              [+1.342060e-02, +5.159466e-03 - 6.475855e-03j], \
                              [+1.791006e-02, -9.459894e-03 - 1.412467e-02j], \
                              [-1.048575e-03, +3.075467e-04 + 9.873627e-04j], \
                              [+9.158551e-06, -3.260269e-06 - 8.840548e-06j], \
                              [+1.809446e-02, +1.029965e-03 + 1.201244e-03j], \
                              [+8.255341e-03, -3.648071e-03 - 5.884530e-03j], \
                              [-1.286835e-03, +1.828698e-06 + 7.071967e-05j], \
                              [+1.827908e-05, +1.276843e-07 + 8.061632e-08j]])

    coefs["HHsw"] = np.array([[+2.038368e+00, -1.070596e+00 + 4.617718e-04j], \
                              [+6.742867e-02, +1.422845e-01 + 4.036745e-03j], \
                              [-1.544673e-03, -2.882753e-03 - 1.021860e-03j], \
                              [+1.167191e-05, +1.838410e-05 + 1.433121e-05j], \
                              [-1.716876e-02, -1.404714e-02 + 2.765220e-02j], \
                              [-2.064313e-02, +2.884548e-02 + 1.580035e-01j], \
                              [+1.172491e-03, -6.833107e-04 - 6.044204e-03j], \
                              [-6.111610e-06, +4.112504e-06 + 5.471463e-05j], \
                              [-2.939264e-02, +1.196099e-02 - 5.905559e-03j], \
                              [+4.007160e-03, -6.952809e-03 + 1.881372e-02j], \
                              [+1.482772e-03, +3.991268e-04 - 2.664768e-04j], \
                              [-2.163604e-05, -4.235270e-06 - 1.228258e-06j], \
                              [-2.643806e-01, +1.676822e-02 + 5.227076e-05j], \
                              [-1.240919e-02, -3.573475e-02 - 7.998733e-04j], \
                              [+2.162084e-04, +1.083750e-03 + 3.168845e-04j], \
                              [-3.482596e-07, -8.535620e-06 - 4.213366e-06j], \
                              [+1.347741e-02, +3.305453e-03 - 8.652656e-03j], \
                              [+7.223413e-03, -6.991652e-03 - 1.631189e-02j], \
                              [-5.037439e-04, +1.321311e-04 + 1.143512e-03j], \
                              [+2.889241e-06, -5.730351e-07 - 1.266315e-05j], \
                              [+1.812623e-02, -7.689661e-03 + 1.684635e-03j], \
                              [+2.313635e-02, +1.171194e-02 - 6.082012e-03j], \
                              [-1.569241e-03, -6.270342e-04 + 9.248031e-05j], \
                              [+1.795667e-05, +6.716300e-06 - 1.181313e-08j]])

    if zerocrosswind == True:
        coefs["VVws"] = coefs["VVsw"]
        coefs["HHws"] = coefs["HHsw"]

    G = lambda theta, phi: cosd(phi) * sind(theta) - 1j * cosd(theta)
    spread = lambda phi: sech(1.0 * acosd(cosd(phi))) ** 2
    Braggsum = lambda phi: (spread(phi) - spread(phi + 180)) / (spread(phi) + spread(phi + 180))
    vbr = lambda theta, lambdar: np.sqrt(g * sind(theta) / (4 * np.pi / lambdar) + \
                                         gamma * (4 * np.pi / lambdar * sind(theta) ** 3))

    if (np.size(theta) == np.size(phi)) & (np.size(phi) == np.size(u)):
        THETA = theta
        PHI = phi
        U = u
        OMEGA = omega
        SWH = swh
        OMEGA_sw = omega_sw
        SWH_sw = swh_sw
        PHI_sw = phi_sw
    else:
        [THETA, PHI, U] = np.meshgrid(theta, phi, u)
        [_, _, OMEGA] = np.meshgrid(theta, phi, omega)
        [_, _, SWH] = np.meshgrid(theta, phi, swh)

        [_, _, OMEGA_sw] = np.meshgrid(theta, phi, omega_sw)
        [_, _, SWH_sw] = np.meshgrid(theta, phi, swh_sw)
        [_, _, PHI_sw] = np.meshgrid(theta, phi, phi_sw)

    nonpolDoppler = vbr(THETA, lambdar) * Braggsum(PHI) + drift * U * cosd(PHI) * sind(THETA)

    VV = nonpolDoppler + \
         beta_ws * np.real(G(THETA, PHI) * MTF(THETA, PHI, U, coefs.get("VVws"))) / g * \
         SWH ** 2 * OMEGA ** 3 + \
         beta_sw * np.real(G(THETA, PHI_sw) * MTF(THETA, PHI_sw, U, coefs.get("VVsw"))) / g * \
         SWH_sw ** 2 * OMEGA_sw ** 3

    HH = nonpolDoppler + \
         beta_ws * np.real(G(THETA, PHI) * MTF(THETA, PHI, U, coefs.get("HHws"))) / g * \
         SWH ** 2 * OMEGA ** 3 + \
         beta_sw * np.real(G(THETA, PHI_sw) * MTF(THETA, PHI_sw, U, coefs.get("HHsw"))) / g * \
         SWH_sw ** 2 * OMEGA_sw ** 3

    return [-VV, -HH]  # convention different ADMARTIN 24/03/2021
