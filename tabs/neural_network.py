import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.metrics import mean_squared_error
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler

from utils.data_generator import generate_data
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


class NeuralNetworkTab:
    def __init__(self, parent):
        self.parent = parent
        self._build_ui()

    def _build_ui(self):
        controls, chart = create_tab_layout(self.parent)
        section_title(
            controls,
            "Reseau de neurones",
            "MLPRegressor sur donnees aleatoires avec suivi de la courbe de perte.",
        )

        self.x_min = labeled_slider(controls, "X minimum", -20, 0, -10, 20)
        self.x_max = labeled_slider(controls, "X maximum", 1, 30, 10, 29)
        self.neurons = labeled_slider(controls, "Neurones par couche", 5, 100, 50, 95)
        self.layers = labeled_slider(controls, "Nombre de couches", 1, 5, 2, 4)
        self.n_pts = labeled_slider(controls, "Nombre de points", 50, 500, 150, 45)

        primary_button(controls, "Entrainer le reseau", self._run).pack(
            pady=(18, 12), padx=16, fill="x"
        )

        self.result_box = result_box(controls, height=145)
        self.result_box.pack(padx=16, pady=(0, 16), fill="x")

        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(10, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=chart)
        add_canvas(self.canvas, chart)
        self.ax1.set_title("Ajustement du reseau")
        self.ax2.set_title("Courbe de perte")
        style_axes(self.ax1, self.ax2)
        self.canvas.draw()

    def _run(self):
        x_min = int(self.x_min.get())
        x_max = int(self.x_max.get())
        n = int(self.n_pts.get())
        neurons = int(self.neurons.get())
        layers = int(self.layers.get())

        if x_min >= x_max:
            write_results(self.result_box, "Erreur : X minimum doit etre inferieur a X maximum.")
            return

        x, y = generate_data(n, x_min, x_max, noise=2.0)
        x_reshaped = x.reshape(-1, 1)
        scaler = StandardScaler()
        x_scaled = scaler.fit_transform(x_reshaped)

        hidden = tuple([neurons] * layers)
        model = MLPRegressor(
            hidden_layer_sizes=hidden,
            max_iter=500,
            random_state=42,
            learning_rate_init=0.01,
        )
        model.fit(x_scaled, y)
        y_pred = model.predict(x_scaled)
        rmse = mean_squared_error(y, y_pred) ** 0.5

        idx = np.argsort(x)
        self.ax1.clear()
        self.ax1.scatter(
            x,
            y,
            alpha=0.45,
            label="Donnees reelles",
            color=PLOT_COLORS["blue"],
            s=34,
        )
        self.ax1.plot(
            x[idx],
            y_pred[idx],
            color=PLOT_COLORS["red"],
            linewidth=2.2,
            label="Prediction NN",
        )
        self.ax1.set_title("Ajustement du reseau")
        self.ax1.set_xlabel("X")
        self.ax1.set_ylabel("Y")
        self.ax1.legend()

        self.ax2.clear()
        self.ax2.plot(model.loss_curve_, color=PLOT_COLORS["purple"], linewidth=2)
        self.ax2.set_title("Courbe de perte")
        self.ax2.set_xlabel("Iteration")
        self.ax2.set_ylabel("Loss")
        style_axes(self.ax1, self.ax2)
        self.fig.tight_layout()
        self.canvas.draw()

        write_results(
            self.result_box,
            f"Architecture : {layers} couches x {neurons} neurones\n"
            f"RMSE : {rmse:.4f}\n"
            f"Iterations : {model.n_iter_}\n"
            f"Points generes : {n}",
        )
