'''This file stores constants used throughout the slider program.'''


import numpy as np
from pycbc.conversions import mchirp_from_mass1_mass2, chi_eff, chi_a


# constants needed for unit conversion
c = 3.0e8  # speed of light
G = 6.67430e-11  # Newton's gravitational constant
Msun = 1.989e30  # mass of the Sun in kg
pc_SI = 3.08567758128e+16  # number of meters in one parsec

# Simulated Data parameters
m1_inj = 50.
m2_inj = 30.
chi1_inj = 0.3
chi2_inj = -0.4
chirp_inj = mchirp_from_mass1_mass2(m1_inj, m2_inj)
ratio_inj = m2_inj / m1_inj
spin_plus_inj = chi_eff(m1_inj, m2_inj, chi1_inj, chi2_inj)
spin_minus_inj = chi_a(m1_inj, m2_inj, chi1_inj, chi2_inj)
params_inj = np.array([m1_inj, m2_inj, chi1_inj, chi2_inj])
num_params = len(params_inj)

# reference parameters for real data
# FORMAT -- 'GW name': [GPS event time, [mass1, mass2, spin plus, spin minus]]

#GW signals to add: 200112*, 191109, 190828, 190521, 190519, 190630*
signal_ref_params = {'GW150914': [1126259462.4, [34.6, 30.0, 0.52, 0.0]],
                     'GW200129': [1264316116.4, [35.5, 29.0, 0.11, 0.0]],
                     'GW190521': [1242459857.4, [43.4, 33.4, 0.10, 0.0]],
                     'GW200224': [1266618172.4, [40.0, 32.5, 0.73, 0.0]],
                     'GW200311': [1267963151.3, [34.2, 27.7, 0.71, 0.0]],
                     'GW200112*': [1262879936.0, [35.6, 28.3, 0.06, 0.0]],
                     'GW191109': [1257296855.2, [65, 47, -0.29, 0.0]],
                     'GW190828': [1251009263.7, [31.9, 25.8, 0.15, 0.0]],
                     'GW190519': [1242315362.3, [65.1, 40.8, 0.33, 0.0]],
                     'GW190630*': [1245955943.1, [35.1, 24.0, 0.10, 0.0]]}


# choose domain of parameters
m1_min = m1_inj - 5.
m1_max = m1_inj + 5.
m2_min = m2_inj - 5.
m2_max = m2_inj + 5.
chi1_min = -0.997
chi1_max = 0.997
chi2_min = -0.997
chi2_max = 0.997
ratio_min = 0.
ratio_max = 0.99
spin_plus_min = -0.997
spin_plus_max = 0.997
spin_minus_min = -0.997
spin_minus_max = 0.997
amp_min= 0
amp_max= 150


# define other physical parameters
# component masses
m1_SI = m1_inj * Msun
m2_SI = m2_inj * Msun
# total mass
M_SI = m1_SI + m2_SI
M_sec = M_SI * G / c**3
# chirp mass
chirp_SI = (m1_SI * m2_SI)**(3/5) / (m1_SI + m2_SI)**(1/5)
chirp_sec = chirp_SI * G / c**3
# luminosity distance (in Mega-parsec)
DL = 100.
DL_SI = DL * (1.e6) * pc_SI


# set window size for plotting and generating waveforms
window_min = -0.22  # plot beginning 0.2 sec before merger
window_max = 0.03  # plot ending 0.05 sec after merger

# define frequency bins
f_min = 16.
f_max = 1024.
Nf = 2**14 + 1
freqs_full = np.linspace(0., f_max, Nf)
freqs_indexes = np.where(freqs_full > f_min)
freqs = freqs_full[freqs_indexes]
df = freqs[1] - freqs[0]


# checkbox rectangle for plotting
checkbox_rect = [0.05, 0.75, 0.2, 0.2]
menu_rect= [0.05, 0.5, 0.2, 0.2]

# slider rectangles for plotting
slider1_rect = [0.15, 0.22, 0.65, 0.03]
slider2_rect = [0.15, 0.18, 0.65, 0.03]
slider3_rect = [0.15, 0.14, 0.65, 0.03]
slider4_rect = [0.15, 0.10, 0.65, 0.03]
slider5_rect= [0.15, 0.06, 0.65, 0.03]
slider6_rect= [0.15, 0.02, 0.65, 0.03]

# button rectangle to go to injected (or MAP) parameters
button_rect = [0.05, 0.7, 0.2, 0.04]
button_signal= [0.05, 0.65, 0.2, 0.04]
button1_signal= [0.05, 0.6, 0.2, 0.04]
button2_signal= [0.05, 0.55, 0.2, 0.04]
button3_signal= [0.05, 0.5, 0.2, 0.04]
button4_signal= [0.05, 0.45, 0.2, 0.04]
button5_signal= [0.05, 0.4, 0.2, 0.04]
button6_signal= [0.05, 0.35, 0.2, 0.04]
button7_signal= [0.05, 0.30, 0.2, 0.04]


# parameter labels
m1_label = r'$m_1\,\,(M_\odot)$'
m2_label = r'$m_2\,\,(M_\odot)$'
chi1_label = r'$\chi_1$'
chi2_label = r'$\chi_2$'
chirp_label = r'$\mathcal{M}\,\,(M_\odot)$'
ratio_label = r'$q$'
spin_plus_label = r'$\chi_+$'
spin_minus_label = r'$\chi_-$'
amp_label= r'amplitude'
phase_label= r'phase'
det_label= r'Livingston Detector'

