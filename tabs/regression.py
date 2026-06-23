import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

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


class RegressionTab:
    def __init__(self, parent):
        self.parent = parent
        self._build_ui()

    def _build_ui(self):
        controls, chart = create_tab_layout(self.parent)
        section_title(
            controls,
            "Regression lineaire multiple",
            "Deux variables explicatives aleatoires et un plan de regression en 3D.",
        )

        self.x1_range = labeled_slider(controls, "Amplitude X1", 5, 50, 15, 45)
        self.x2_range = labeled_slider(controls, "Amplitude X2", 5, 50, 15, 45)
        self.noise_slider = labeled_slider(
            controls,
            "Bruit aleatoire",
            0,
            20,
            5,
            20,
            value_format=lambda v: f"{v:.1f}",
        )

        primary_button(controls, "Generer et analyser", self._run).pack(
            pady=(18, 12), padx=16, fill="x"
        )

        self.result_box = result_box(controls, height=190)
        self.result_box.pack(padx=16, pady=(0, 16), fill="x")

        self.fig = plt.figure(figsize=(8, 6))
        self.ax = self.fig.add_subplot(111, projection="3d")
        self.canvas = FigureCanvasTkAgg(self.fig, master=chart)
        add_canvas(self.canvas, chart)
        self.ax.set_title("Cliquez sur 'Generer et analyser'")
        style_axes(self.ax)
        self.canvas.draw()

    def _run(self):
        n = 140
        r1 = int(self.x1_range.get())
        r2 = int(self.x2_range.get())
        noise_level = self.noise_slider.get()

        x1 = np.random.uniform(-r1, r1, n)
        x2 = np.random.uniform(-r2, r2, n)
        y = 2.39 * x1 - 1.44 * x2 + 5.25 + np.random.normal(0, noise_level, n)
        x = np.column_stack((x1, x2))

        model = LinearRegression()
        model.fit(x, y)
        y_pred = model.predict(x)

        r2_score_value = r2_score(y, y_pred)
        rmse = mean_squared_error(y, y_pred) ** 0.5
        coef_x1, coef_x2 = model.coef_
        intercept = model.intercept_

        self.ax.clear()
        self.ax.scatter(
            x1,
            x2,
            y,
            c=y,
            cmap="viridis",
            alpha=0.78,
            edgecolors="#e5e7eb",
            linewidths=0.25,
            s=34,
        )

        x1_grid, x2_grid = np.meshgrid(
            np.linspace(-r1, r1, 22), np.linspace(-r2, r2, 22)
        )
        y_grid = coef_x1 * x1_grid + coef_x2 * x2_grid + intercept
        self.ax.plot_surface(
            x1_grid,
            x2_grid,
            y_grid,
            color=PLOT_COLORS["red"],
            alpha=0.22,
            linewidth=0,
        )

        self.ax.set_title("Regression lineaire multiple")
        self.ax.set_xlabel("X1")
        self.ax.set_ylabel("X2")
        self.ax.set_zlabel("Y")
        self.ax.view_init(elev=24, azim=-58)
        style_axes(self.ax)
        self.canvas.draw()

        write_results(
            self.result_box,
            "Equation du modele\n"
            f"Y = {coef_x1:.2f} X1 + {coef_x2:.2f} X2 + {intercept:.2f}\n\n"
            "Metriques\n"
            f"R2   : {r2_score_value:.4f}\n"
            f"RMSE : {rmse:.4f}\n"
            f"Points generes : {n}",
        )
