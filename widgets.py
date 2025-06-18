'''Script to store functions for sliders and checkboxes.'''


from matplotlib.widgets import CheckButtons, Slider, Button
from constants import *
from pycbc.conversions import mchirp_from_mass1_mass2, spin1z_from_mass1_mass2_chi_eff_chi_a, spin2z_from_mass1_mass2_chi_eff_chi_a
from pycbc.conversions import mass1_from_mchirp_q, mass2_from_mchirp_q


# function to remove sliders (so they may be replaced with others)
def remove_sliders(slider_axes, sliders):
    for ax in slider_axes:
        ax.remove()
    for slider in sliders:
        slider.disconnect_events()



# function to make checkboxes
def make_checkboxes(fig):
    # make axes
    checkbox_ax = fig.add_axes(checkbox_rect)
    # checkbox labels
    chirp_q_label = r'use $\mathcal{M}$ and $q$'
    plus_minus_label = r'use $\chi_+$ and $\chi_-$'
    real_data_label = 'use real data'
    checkbox_labels = [chirp_q_label, plus_minus_label, real_data_label]
    # checkboxes start unchecked
    init_status = [False, False, False]
    checkboxes = CheckButtons(checkbox_ax, checkbox_labels, init_status)

    #create buttons
    button_ax = fig.add_axes(button_signal)
    button_ax.set_visible(False)  # hidden initially
    buttons = Button(button_ax, 'GW150914', hovercolor='0.97')

    button1_ax = fig.add_axes(button1_signal)
    button1_ax.set_visible(False)  # hidden initially
    buttons1 = Button(button1_ax, 'GW190521', hovercolor='0.97')

    button2_ax = fig.add_axes(button2_signal)
    button2_ax.set_visible(False)  # hidden initially
    buttons2 = Button(button2_ax, 'GW200129', hovercolor='0.97')


    button3_ax = fig.add_axes(button3_signal)
    button3_ax.set_visible(False)  # hidden initially
    buttons3 = Button(button3_ax, 'GW200224', hovercolor='0.97')

    button4_ax = fig.add_axes(button4_signal)
    button4_ax.set_visible(False)  # hidden initially
    buttons4 = Button(button4_ax, 'GW200220', hovercolor='0.97')

    # Checkbox toggle 
    def on_checkbox_click(label):
        if label == real_data_label:
            idx = checkbox_labels.index(label)
            show_dropdown = checkboxes.get_status()[idx]
            button_ax.set_visible(show_dropdown)
            button1_ax.set_visible(show_dropdown)
            button2_ax.set_visible(show_dropdown)
            button3_ax.set_visible(show_dropdown)
            button4_ax.set_visible(show_dropdown)
            fig.canvas.draw_idle()


    checkboxes.on_clicked(on_checkbox_click)

    # Dropdown selection 
    def on_select(signal_name):
        print(f"Selected GW signal: {signal_name}")
        # Add your logic to update plot or data here

    buttons.on_clicked(on_select)
    buttons1.on_clicked(on_select)
    buttons2.on_clicked(on_select)
    buttons3.on_clicked(on_select)
    buttons4.on_clicked(on_select)

    return checkboxes, buttons, buttons1, buttons2, buttons3, buttons4


# function to make sliders
def make_sliders(fig, checkboxes, init_comp_params):
    # unpack parameter values
    m1_init, m2_init, chi1_init, chi2_init = init_comp_params
    # get status of checkboxes
    chirp_q_checked, plus_minus_checked, real_data_checked = checkboxes.get_status()
    # make axes for sliders
    ax1 = fig.add_axes(slider1_rect)
    ax2 = fig.add_axes(slider2_rect)
    ax3 = fig.add_axes(slider3_rect)
    ax4 = fig.add_axes(slider4_rect)
    ax5 = fig.add_axes(slider5_rect)
    ax6 = fig.add_axes(slider6_rect)
    # make sliders
    if chirp_q_checked:
        chirp_init = mchirp_from_mass1_mass2(m1_init, m2_init)
        ratio_init = m2_init / m1_init
        slider1 = Slider(ax=ax1, label=chirp_label, valmin=chirp_init - 10, valmax=chirp_init + 10, valinit=chirp_init)
        slider2 = Slider(ax=ax2, label=ratio_label, valmin=ratio_min, valmax=ratio_max, valinit=ratio_init)
    else:
        slider1 = Slider(ax=ax1, label=m1_label, valmin=m1_init - 10, valmax=m1_init + 10, valinit=m1_init)
        slider2 = Slider(ax=ax2, label=m2_label, valmin=m2_init - 10, valmax=m2_init + 10, valinit=m2_init)
    if plus_minus_checked:
        spin_plus_init = chi_eff(m1_init, m2_init, chi1_init, chi2_init)
        spin_minus_init = chi_a(m1_init, m2_init, chi1_init, chi2_init)
        slider3 = Slider(ax=ax3, label=spin_plus_label, valmin=spin_plus_min, valmax=spin_plus_max, valinit=spin_plus_init)
        slider4 = Slider(ax=ax4, label=spin_minus_label, valmin=spin_minus_min, valmax=spin_minus_max, valinit=spin_minus_init)
    else:
        slider3 = Slider(ax=ax3, label=chi1_label, valmin=chi1_min, valmax=chi1_max, valinit=chi1_init)
        slider4 = Slider(ax=ax4, label=chi2_label, valmin=chi2_min, valmax=chi2_max, valinit=chi2_init)
    
    slider5 = Slider(ax=ax5, label=amp_label, valmin=-4, valmax=5, valinit= 1)
    slider6 = Slider(ax=ax6, label=phase_label, valmin= -np.pi, valmax= np.pi, valinit= 0)
    # store sliders and axes
    slider_axes = [ax1, ax2, ax3, ax4, ax5, ax6]
    sliders = [slider1, slider2, slider3, slider4, slider5, slider6]
    # remove tick marking initial position of sliders
    for slider in sliders:
        slider.ax.get_lines()[0].set_visible(False)
    return [slider_axes, sliders]


# make button to go to correct (or MAP) parameter values
def make_button(fig):
    button_ax = fig.add_axes(button_rect)
    return Button(button_ax, 'go to reference parameters', hovercolor='0.975')


# function to get component parameters from sliders and checkboxes
def get_comp_params(sliders):
    # convert slider parameters to component parameters
    if sliders[0].label.get_text() is chirp_label and sliders[2].label.get_text() is spin_plus_label:
        m1 = mass1_from_mchirp_q(sliders[0].val, 1./sliders[1].val)
        m2 = mass2_from_mchirp_q(sliders[0].val, 1./sliders[1].val)
        chi1 = spin1z_from_mass1_mass2_chi_eff_chi_a(m1, m2, sliders[2].val, sliders[3].val)
        chi2 = spin2z_from_mass1_mass2_chi_eff_chi_a(m1, m2, sliders[2].val, sliders[3].val)
    elif sliders[0].label.get_text() is chirp_label:
        m1 = mass1_from_mchirp_q(sliders[0].val, 1./sliders[1].val)
        m2 = mass2_from_mchirp_q(sliders[0].val, 1./sliders[1].val)
        chi1 = sliders[2].val
        chi2 = sliders[3].val
    elif sliders[2].label.get_text() is spin_plus_label:
        m1 = sliders[0].val
        m2 = sliders[1].val
        chi1 = spin1z_from_mass1_mass2_chi_eff_chi_a(m1, m2, sliders[2].val, sliders[3].val)
        chi2 = spin2z_from_mass1_mass2_chi_eff_chi_a(m1, m2, sliders[2].val, sliders[3].val)
    else:
        m1 = sliders[0].val
        m2 = sliders[1].val
        chi1 = sliders[2].val
        chi2 = sliders[3].val
    return np.array([m1, m2, chi1, chi2])


# function to get slider parameters from component parameters
def get_slider_params(params, checkboxes):
    # unpack parameter values
    m1, m2, chi1, chi2 = params.copy()
    # get status of checkboxes
    chirp_q_checked, plus_minus_checked, real_data_checked = checkboxes.get_status()
    if chirp_q_checked:
        params[0] = mchirp_from_mass1_mass2(m1, m2)
        params[1] = m2 / m1
    if plus_minus_checked:
        params[2] = chi_eff(m1, m2, chi1, chi2)
        params[3] = chi_a(m1, m2, chi1, chi2)
    return params


