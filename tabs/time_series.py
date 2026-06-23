import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from statsmodels.tsa.arima.model import ARIMA

from utils.data_generator import generate_time_series
from utils.ui import (
    PLOT_COLORS,
    add_canvas,
    create_tab_layout,
    labeled_slider,
    primary_button,
    result_box,
    section_title,
    style_axes,
    write_results,
)


class TimeSeriesTab:
    def __init__(self, parent):
        self.parent = parent
        self._build_ui()

    def _build_ui(self):
        controls, chart = create_tab_layout(self.parent)
        section_title(
            controls,
            "Series temporelles ARIMA",
            "Marche aleatoire bornee, apprentissage sur 160 points et prevision.",
        )

        self.p_val = labeled_slider(controls, "p (AR)", 0, 5, 1, 5)
        self.d_val = labeled_slider(controls, "d (difference)", 0, 2, 1, 2)
        self.q_val = labeled_slider(controls, "q (MA)", 0, 5, 1, 5)
        self.n_forecast = labeled_slider(controls, "Previsions futures", 5, 50, 20, 45)
        self.y_min = labeled_slider(controls, "Y minimum", -20, 0, -5, 20)
        self.y_max = labeled_slider(controls, "Y maximum", 1, 30, 15, 29)

        primary_button(controls, "Analyser et prevoir", self._run).pack(
            pady=(18, 12), padx=16, fill="x"
        )

        self.result_box = result_box(controls, height=140)
        self.result_box.pack(padx=16, pady=(0, 16), fill="x")

        self.fig, self.ax = plt.subplots(figsize=(8, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=chart)
        add_canvas(self.canvas, chart)
        self.ax.set_title("Cliquez sur 'Analyser et prevoir'")
        style_axes(self.ax)
        self.canvas.draw()

    def _run(self):
        p = int(self.p_val.get())
        d = int(self.d_val.get())
        q = int(self.q_val.get())
        n_forecast = int(self.n_forecast.get())
        y_min = int(self.y_min.get())
        y_max = int(self.y_max.get())

        if y_min >= y_max:
            write_results(self.result_box, "Erreur : Y minimum doit etre inferieur a Y maximum.")
            return

        serie = generate_time_series(200, y_min, y_max)
        train = serie[:160]
        test = serie[160:]

        try:
            model = ARIMA(train, order=(p, d, q))
            result = model.fit()
            forecast = result.forecast(steps=n_forecast)
            compare_len = min(len(test), len(forecast))
            rmse = np.sqrt(np.mean((test[:compare_len] - forecast[:compare_len]) ** 2))
        except Exception as exc:
            write_results(self.result_box, f"Erreur ARIMA\n{exc}")
            return

        t_train = np.arange(len(train))
        t_test = np.arange(len(train), len(train) + len(test))
        t_forecast = np.arange(len(train), len(train) + n_forecast)

        self.ax.clear()
        self.ax.plot(t_train, train, label="Entrainement", color=PLOT_COLORS["blue"], linewidth=2)
        self.ax.plot(
            t_test,
            test,
            label="Test reel",
            color=PLOT_COLORS["green"],
            linestyle="--",
            linewidth=1.8,
        )
        self.ax.plot(
            t_forecast,
            forecast,
            label="Prevision ARIMA",
            color=PLOT_COLORS["red"],
            linewidth=2,
        )
        self.ax.axvline(x=len(train), color="#64748b", linestyle=":", label="Debut test")
        self.ax.set_title(f"Serie temporelle ARIMA({p},{d},{q})")
        self.ax.set_xlabel("Temps")
        self.ax.set_ylabel("Valeur")
        self.ax.legend()
        style_axes(self.ax)
        self.fig.tight_layout()
        self.canvas.draw()

        write_results(
            self.result_box,
            f"Modele : ARIMA({p},{d},{q})\n"
            f"RMSE : {rmse:.4f}\n"
            f"AIC : {result.aic:.2f}\n"
            f"Previsions : {n_forecast}",
        )
