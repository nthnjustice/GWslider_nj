import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import trapezoid as integrate
from scipy.interpolate import interp1d
from pycbc.conversions import mchirp_from_mass1_mass2, spin1z_from_mass1_mass2_chi_eff_chi_a, spin2z_from_mass1_mass2_chi_eff_chi_a
from pycbc.conversions import mass1_from_mchirp_q, mass2_from_mchirp_q
from constants import *
from template import waveform
from matched_filter import *
import pickle
from signal_processing import *


##GW_class.waveform_TD could be replaced with the strain data found in the dictionary


class GWSignals:

    def __init__(self, ref_params, dictionary, simulated=False):

        self.dictionary= dictionary

        # simulated signal or not
        self.simulated = simulated

        # reference parameters
        #add amplitude into reference params 
        self.mass1, self.mass2, self.chiPlus, self.chiMinus = ref_params
        self.chirp = mchirp_from_mass1_mass2(self.mass1, self.mass2)
        self.ratio = self.mass2 / self.mass1
        self.chi1 = spin1z_from_mass1_mass2_chi_eff_chi_a(self.mass1, self.mass2, self.chiPlus, self.chiMinus)
        self.chi2 = spin2z_from_mass1_mass2_chi_eff_chi_a(self.mass1, self.mass2, self.chiPlus, self.chiMinus)  
        self.comp_params = np.array([self.mass1, self.mass2, self.chi1, self.chi2])

        # minimum / maximum mass parameters for sliders
        #add amp range here
        self.min_mass1 = self.mass1 - 5.0
        self.min_mass2 = self.mass2 - 5.0
        self.max_mass1 = self.mass1 + 5.0
        self.max_mass2 = self.mass2 + 5.0
        self.min_chirp = mchirp_from_mass1_mass2(self.min_mass1, self.min_mass2)
        self.max_chirp = mchirp_from_mass1_mass2(self.max_mass1, self.max_mass2)




# load data 
#150914 data

# Load or define the GW150914 data
with open('data/GW190521_data_dict.pkl', 'rb') as f:
    GW150914_data = pickle.load(f)

# Create the GWSignals object
#gw_150914 = GWSignals(times_150914, templateTD_150914, ref_params_150914, PSD_data_150914, PSD_data_150914)

# Get the dictionary for use in analysis
#gw150914_dict = gw_150914.to_dict()



# class instantiation for real GW events
#GW200129 = GWSignals(times_200129, strains_200129, strainsBP_200129, signal_ref_params['GW200129'][1], freqs_for_PSD_200129, PSD_200129)
GW150914 = GWSignals(signal_ref_params['GW150914'][1], GW150914_data)
#GW190521= GWSignals(times_190521, strains_190521, strainsBP_190521, signal_ref_params['GW190521'][1], freqs_for_PSD_190521, PSD_190521)
#GW200224= GWSignals(times_200224, strains_200224, strainsBP_200224, signal_ref_params['GW200224'][1], freqs_for_PSD_200224, PSD_200224)
#GW200311= GWSignals(times_200311, strains_200311, strainsBP_200311, signal_ref_params['GW200311'][1], freqs_for_PSD_200311, PSD_200311)


# # class instantiation for simulated GW event
# aLIGO_freqs_for_PSD, aLIGO_theoretical_PSD = np.load('data/simulated/aLIGO_PSD.npy')
# aLIGO_theoretical_ASD = np.sqrt(aLIGO_theoretical_PSD)
# ASD_to_whiten_simul = np.ones(Nf)
# ASD_to_whiten_simul[-waveform.num_freqs:] = interp1d(aLIGO_freqs_for_PSD, aLIGO_theoretical_ASD)(freqs)
# simulated_waveform_FD = waveform.get_FD_waveform(params_inj, 0.0)
# simulated_waveform_TD = waveform.iFFT_waveform(simulated_waveform_FD / ASD_to_whiten_simul)

# GWsimulated = GWSignals(waveform.times, simulated_waveform_TD, simulated_waveform_TD, [m1_inj, m2_inj, spin_plus_inj, spin_minus_inj],
#                         aLIGO_freqs_for_PSD, aLIGO_theoretical_PSD, simulated=True)



