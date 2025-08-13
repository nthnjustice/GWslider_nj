from pathlib import Path

import shinyswatch
from shiny import App, ui, render
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

css_file = Path(__file__).parent / "styles.css"

app_ui = ui.page_navbar(
    ui.nav_panel(
        "",
        ui.row(
            ui.column(
                2,
                ui.card(
                    ui.input_checkbox_group(
                        "options",
                        "",
                        choices={
                            "chirp_and_q": "Use 𝑀 and 𝑞",
                            "chi_and_chi": "Use 𝜒₊ and 𝜒₋",
                            "real_data": "Use Real Data",
                            "detector": "Toggle Detector (L1, H1)",
                            "residuals": "Residuals",
                        },
                    ),
                ),
                ui.input_task_button(
                    "go_to_ref_params",
                    "Go to Reference Parameters",
                    width="100%",
                ),
            ),
            ui.column(
                10,
                ui.card(
                    ui.output_plot("plot", width="100%", height="600px"),
                ),
            ),
        ),
        ui.row(
            ui.column(
                12,
                ui.card(
                    ui.input_slider(
                        "slider0",
                        "Slider0",
                        min=0,
                        max=100,
                        value=50,
                        step=1,
                        width="100%",
                    ),
                    ui.input_slider(
                        "slider1",
                        "Slider1",
                        min=0,
                        max=100,
                        value=50,
                        step=1,
                        width="100%",
                    ),
                    ui.input_slider(
                        "slider2",
                        "Slider2",
                        min=0,
                        max=100,
                        value=50,
                        step=1,
                        width="100%",
                    ),
                    ui.input_slider(
                        "slider3",
                        "Slider3",
                        min=0,
                        max=100,
                        value=50,
                        step=1,
                        width="100%",
                    ),
                    ui.input_slider(
                        "slider4",
                        "Slider4",
                        min=0,
                        max=100,
                        value=50,
                        step=1,
                        width="100%",
                    ),
                    ui.input_slider(
                        "slider5",
                        "Slider5",
                        min=0,
                        max=100,
                        value=50,
                        step=1,
                        width="100%",
                    ),
                ),
            ),
        ),
    ),
    title="GWslider",
    fillable=True,
    theme=shinyswatch.theme.spacelab,
    header=ui.tags.head(
        ui.include_css(css_file),
        ui.tags.link(
            rel="stylesheet",
            href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css",
        ),
    ),
    navbar_options=ui.navbar_options(theme="dark")
)


def app_server(input, output, session):
    @render.plot
    def plot():
        days = 365
        trend = 0.1 
        noise_level = 5
        start_date = datetime(2023, 1, 1)
        dates = [start_date + timedelta(days=i) for i in range(days)]
        t = np.arange(days)
        trend_component = trend * t
        seasonal_component = 10 * np.sin(2 * np.pi * t / 365.25) + 5 * np.sin(2 * np.pi * t / 30.4)
        noise = np.random.normal(0, noise_level, days)
        values = 100 + trend_component + seasonal_component + noise
        
        df = pd.DataFrame({
            'date': dates,
            'value': values
        })
        
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(df['date'], df['value'], linewidth=1.5, color='#2E86C1')
        ax.set_title('Time Series Data', fontsize=16, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Value', fontsize=12)
        ax.grid(True, alpha=0.3)
        
        ax.tick_params(axis='x', rotation=45)
        plt.tight_layout()
        
        return fig

app = App(app_ui, app_server)