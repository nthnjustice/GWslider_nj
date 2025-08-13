'''Main python file to run GW slider.'''
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
from widgets import *
from matched_filter import *
from GW_class import *

# setup main plot
fig, ax = plt.subplots(figsize=(12, 8))

# adjust plot area
fig.subplots_adjust(left=0.3, bottom=0.3, right=0.95, top=0.95)

# make checkboxes
checkboxes, buttons, buttons1, buttons2, buttons3, buttons4, buttons5, buttons6, buttons7 = make_checkboxes(fig)

# start off using simulated data
GW_signal = GW_simulated
# start off with Hanford detector 
det = 'H1'
# make sliders
slider_axes, sliders = make_sliders(fig, checkboxes, GW_signal.comp_params)

# make button to go to reference parameters
button = make_button(fig)

# get initial parameters
init_params = get_comp_params(sliders)

# plot data and fit
fit, data, times, SNRmax, amp, phase = wrapped_matched_filter(init_params, GW_signal, det)
residuals= residual_func(data, fit)
data_line, = ax.plot(times, data, color='Black', label=f'{det} data', alpha=0.5)
fit_line, = ax.plot(times, fit, color='C2', label='fit')
residual_line, = ax.plot(times, residuals, color= 'steelblue', alpha= 0.8,label= 'residual')
residual_line.set_visible(False)
ax.set_xlabel('time [s]')
ax.set_ylabel('strain')
ax.legend(loc='upper left')
ax.set_xlim(-0.15, 0.)

# make error message if spins are outside domain
error_text = fig.text(0.05, 0.1, 'Spins not in domain.', transform=ax.transAxes, fontsize=10)
error_text.set_visible(False)

#chi-squared text box 
chi_text = fig.text(0.35, 0.35, rf'$\rho = {round(SNRmax, 3)}$')

# function to handle checkbox changes
def checkbox_update(val):
    # store current parameter values
    global slider_axes, sliders
    # remove old sliders
    remove_sliders(slider_axes, sliders)
    # store current detector 
    global det, data_line, residual_line
    # checkbox that switches detector data
    det = 'L1' if checkboxes.get_status()[3] else 'H1'
     # update label
    data_line.set_label(f'{det} data')
    # check if using real data or not
    real_data_checked = checkboxes.get_status()[2]
    residuals_checked= checkboxes.get_status()[4]
    if not real_data_checked:
        global GW_signal
        GW_signal = GW_simulated
        fit, data, times, SNRmax, amp, phase = wrapped_matched_filter(init_params, GW_signal, det)
        data_line.set_xdata(times)
        data_line.set_ydata(data)
        ymax = np.max(np.abs(data))
        ax.set_xlim(-0.15, 0.)
        ax.set_ylim(-1.1 * ymax, 1.1 * ymax)
    if residuals_checked:
        fit, data, times, SNRmax, amp, phase = wrapped_matched_filter(init_params, GW_signal, det)
        residuals= residual_func(data, fit)
        residual_line.set_xdata(times)
        residual_line.set_ydata(residuals)
        residual_line.set_visible(True)
    else:   
        residual_line.set_visible(False)  

    # update data which is plotted
    fit, data, times, SNRmax, amp, phase = wrapped_matched_filter(init_params, GW_signal, det)
    data_line.set_xdata(times)
    data_line.set_ydata(data)
    ymax = np.max(np.abs(data))
    ax.set_ylim(-1.1 * ymax, 1.1 * ymax)
    # Rebuild legend in same location
    ax.legend(loc='upper left')
    # make new sliders
    slider_axes, sliders = make_sliders(fig, checkboxes, GW_signal.comp_params)
    # remove initial position ticks on each slider
    for slider in sliders:
        slider.ax.get_lines()[0].set_visible(False)
    # reattach slider_update to the new sliders
    sliders[0].on_changed(slider_update)
    sliders[1].on_changed(slider_update)
    sliders[2].on_changed(slider_update)
    sliders[3].on_changed(slider_update)
    # update data plotted
    # error_text.set_visible(True)
    slider_update(val)
    fig.canvas.draw_idle()
    return

# function to handle slider changes
def slider_update(val):
    chirp_q_checked, plus_minus_checked, real_data_checked, det_checked, residual_checked= checkboxes.get_status()
    # get component parameters
    params = get_comp_params(sliders)
    # check if spins are in domain
    if params[2] < chi1_min or params[2] > chi1_max or params[3] < chi2_min or params[3] > chi2_max:
        fit, data, times, SNRmax, amp, phase = wrapped_matched_filter(init_params, GW_signal, det)
        zero_fit = np.zeros_like(data)
        fit_line.set_data(times, zero_fit)
        residuals = residual_func(data, zero_fit)
        residual_line.set_data(times, residuals)
        error_text.set_visible(True)
        chi_text.set_visible(False)
    elif real_data_checked:
        fit, data, times, SNRmax, amp, phase = wrapped_matched_filter(params, GW_signal, det)
        residuals = residual_func(data, fit)
        sliders[4].set_val(amp)
        sliders[5].set_val(phase)
        fit_line.set_ydata(fit)
        residual_line.set_ydata(residuals)
        chi_text.set_visible(True)
        error_text.set_visible(False)
        chi_text.set_text(rf'$\rho = {round(SNRmax, 3)}$')
    else:
        fit, data, times, SNRmax, amp, phase = wrapped_matched_filter(params, GW_signal, det)
        residuals= residual_func(data, fit)
        sliders[4].set_val(amp)
        sliders[5].set_val(phase)
        fit_line.set_ydata(fit)
        residual_line.set_ydata(residuals)
        chi_text.set_visible(True)
        error_text.set_visible(False)
        chi_text.set_text(rf'$\rho = {round(SNRmax, 3)}$')
    fig.canvas.draw_idle()
    return


# function to send sliders to reference parameters
def button_push(event):
    # get status of checkboxes
    chirp_q_checked, plus_minus_checked, real_data_checked, det_checked, residual_checked = checkboxes.get_status()
    # move sliders to injected value
    if chirp_q_checked:
        sliders[0].set_val(GW_signal.chirp)
        sliders[1].set_val(GW_signal.ratio)
    else:
        sliders[0].set_val(GW_signal.mass1)
        sliders[1].set_val(GW_signal.mass2)

    if plus_minus_checked:
        sliders[2].set_val(GW_signal.chiPlus)
        sliders[3].set_val(GW_signal.chiMinus)
    else:
        sliders[2].set_val(GW_signal.chi1)
        sliders[3].set_val(GW_signal.chi2)
    slider_update(event)
    fig.canvas.draw_idle()
    return

def button_push_signals(event):
    global GW_signal
    GW_signal =  GW150914
    on_button_click(event, buttons)
    fit, data, times, SNRmax, amp, phase = wrapped_matched_filter(init_params, GW_signal, det)
    residuals= residual_func(data, fit)
    data_line.set_xdata(times)
    data_line.set_ydata(data)
    residual_line.set_xdata(times)
    residual_line.set_ydata(residuals)
    button_push(event)
    checkbox_update(event)
    ymax = np.max(np.abs(data))
    ax.set_xlim(0.30, 0.46)
    ax.set_ylim(-1.1 * ymax, 1.1 * ymax)
    fig.canvas.draw_idle()
    return 

def button_push_signals1(event):
    global GW_signal
    GW_signal=  GW190521
    on_button_click(event, buttons1)
    fit, data, times, SNRmax, amp, phase = wrapped_matched_filter(init_params, GW_signal, det)
    residuals= residual_func(data, fit)
    residual_line.set_xdata(times)
    residual_line.set_ydata(residuals)
    data_line.set_xdata(times)
    data_line.set_ydata(data)
    button_push(event)
    checkbox_update(event)
    ymax = np.max(np.abs(data))
    ax.set_xlim(-0.05, 0.15)
    ax.set_ylim(-1.1 * ymax, 1.1 * ymax)
    fig.canvas.draw_idle()
    return 

def button_push_signals2(event):
    global GW_signal
    GW_signal = GW200129
    on_button_click(event, buttons2)
    fit, data, times, SNRmax, amp, phase = wrapped_matched_filter(init_params, GW_signal, det)
    data_line.set_xdata(times)
    data_line.set_ydata(data)
    residuals= residual_func(data, fit)
    residual_line.set_xdata(times)
    residual_line.set_ydata(residuals)
    button_push(event)
    checkbox_update(event)
    ymax = np.max(np.abs(data))
    ax.set_xlim(-0.10, 0.10)
    ax.set_ylim(-1.1 * ymax, 1.1 * ymax)
    fig.canvas.draw_idle()
    return 

def button_push_signals3(event):
    global GW_signal
    GW_signal = GW200224
    on_button_click(event, buttons3)
    fit, data, times, SNRmax, amp, phase = wrapped_matched_filter(init_params, GW_signal, det)
    residuals= residual_func(data, fit)
    data_line.set_xdata(times)
    data_line.set_ydata(data)
    residual_line.set_xdata(times)
    residual_line.set_ydata(residuals)
    button_push(event)
    checkbox_update(event)
    ymax = np.max(np.abs(data))
    ax.set_xlim(-0.10, 0.10)
    ax.set_ylim(-1.1 * ymax, 1.1 * ymax)
    fig.canvas.draw_idle()
    return 

def button_push_signals4(event):
    global GW_signal
    GW_signal = GW200311
    on_button_click(event, buttons4)
    fit, data, times, SNRmax, amp, phase = wrapped_matched_filter(init_params, GW_signal, det)
    residuals= residual_func(data, fit)
    residual_line.set_xdata(times)
    residual_line.set_ydata(residuals)
    data_line.set_xdata(times)
    data_line.set_ydata(data)
    button_push(event)
    checkbox_update(event)
    ymax = np.max(np.abs(data))
    ax.set_xlim(-0.10, 0.2)
    ax.set_ylim(-1.1 * ymax, 1.1 * ymax)
    fig.canvas.draw_idle()
    return 

def button_push_signals5(event):
    global GW_signal
    GW_signal = GW191109
    on_button_click(event, buttons5)
    fit, data, times, SNRmax, amp, phase = wrapped_matched_filter(init_params, GW_signal, det)
    residuals= residual_func(data, fit)
    data_line.set_xdata(times)
    data_line.set_ydata(data)
    residual_line.set_xdata(times)
    residual_line.set_ydata(residuals)
    button_push(event)
    checkbox_update(event)
    ymax = np.max(np.abs(data))
    ax.set_xlim(-0.10, 0.10)
    ax.set_ylim(-1.1 * ymax, 1.1 * ymax)
    fig.canvas.draw_idle()
    return 

def button_push_signals6(event):
    global GW_signal
    GW_signal = GW190828
    on_button_click(event, buttons6)
    fit, data, times, SNRmax, amp, phase = wrapped_matched_filter(init_params, GW_signal, det)
    residuals= residual_func(data, fit)
    data_line.set_xdata(times)
    residual_line.set_xdata(times)
    residual_line.set_ydata(residuals)
    button_push(event)
    checkbox_update(event)
    ymax = np.max(np.abs(data))
    ax.set_xlim(-0.15, 0.15)
    ax.set_ylim(-1.1 * ymax, 1.1 * ymax)
    fig.canvas.draw_idle()
    return 

def button_push_signals7(event):
    global GW_signal
    GW_signal = GW190519
    on_button_click(event, buttons7)
    fit, data, times, SNRmax, amp, phase = wrapped_matched_filter(init_params, GW_signal, det)
    residuals= residual_func(data, fit)
    data_line.set_xdata(times)
    data_line.set_ydata(data)
    residual_line.set_xdata(times)
    residual_line.set_ydata(residuals)
    button_push(event)
    checkbox_update(event)
    ymax = np.max(np.abs(data))
    ax.set_xlim(-0.05, 0.2)
    ax.set_ylim(-1.1 * ymax, 1.1 * ymax)
    fig.canvas.draw_idle()
    return 



# update plot as sliders move
sliders[0].on_changed(slider_update)
sliders[1].on_changed(slider_update)
sliders[2].on_changed(slider_update)
sliders[3].on_changed(slider_update)

# update plots when checkboxes changed
checkboxes.on_clicked(checkbox_update)

def btn_push_sig(event, signal):
    data_line.set_xdata(times)
    data_line.set_ydata(data)
    residual_line.set_xdata(times)
    residual_line.set_ydata(residuals)
        
    checkbox_update(event)
    fig.canvas.draw_idle()
    return



button.on_clicked(button_push)
buttons.on_clicked(button_push_signals)
buttons1.on_clicked(button_push_signals1)
buttons2.on_clicked(button_push_signals2)
buttons3.on_clicked(button_push_signals3)
buttons4.on_clicked(button_push_signals4)
buttons5.on_clicked(button_push_signals5)
buttons6.on_clicked(button_push_signals6)
buttons7.on_clicked(button_push_signals7)
signal_buttons = [buttons, buttons1, buttons2, buttons3, buttons4, buttons5, buttons6, buttons7]


# function to have buttons change color when clicked 
def on_button_click(event, button_to_change):
    for button_obj in signal_buttons:
        button_obj.color = '0.97'
    
    button_to_change.color = 'C2' 
    fig.canvas.draw_idle() 
    return
plt.show()

