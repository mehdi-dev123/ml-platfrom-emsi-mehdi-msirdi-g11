import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from utils.data_generator import generate_multivar
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


class RandomForestTab:
    def __init__(self, parent):
        self.parent = parent
        self._build_ui()

    def _build_ui(self):
        controls, chart = create_tab_layout(self.parent)
        section_title(
            controls,
            "Random Forest",
            "Classification aleatoire et lecture des variables les plus importantes.",
        )

        self.x1_min = labeled_slider(controls, "X1 minimum", -20, 0, -10)
        self.x1_max = labeled_slider(controls, "X1 maximum", 1, 20, 10)
        self.x2_min = labeled_slider(controls, "X2 minimum", -10, 0, -5)
        self.x2_max = labeled_slider(controls, "X2 maximum", 1, 20, 15)
        self.x3_min = labeled_slider(controls, "X3 minimum", 0, 5, 0)
        self.x3_max = labeled_slider(controls, "X3 maximum", 10, 30, 20)
        self.n_trees = labeled_slider(controls, "Nombre d'arbres", 10, 200, 100, 19)
        self.n_classes = labeled_slider(controls, "Nombre de classes", 2, 5, 3, 3)

        primary_button(controls, "Generer et predire", self._run).pack(
            pady=(18, 12), padx=16, fill="x"
        )

        self.result_box = result_box(controls, height=175)
        self.result_box.pack(padx=16, pady=(0, 16), fill="x")

        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(10, 5))
        self.colorbar = None
        self.canvas = FigureCanvasTkAgg(self.fig, master=chart)
        add_canvas(self.canvas, chart)
        self.ax1.set_title("Importance des variables")
        self.ax2.set_title("Predictions")
        style_axes(self.ax1, self.ax2)
        self.canvas.draw()

    def _run(self):
        n_trees = int(self.n_trees.get())
        n_classes = int(self.n_classes.get())
        ranges = [
            (int(self.x1_min.get()), int(self.x1_max.get())),
            (int(self.x2_min.get()), int(self.x2_max.get())),
            (int(self.x3_min.get()), int(self.x3_max.get())),
        ]

        data = generate_multivar(240, ranges)
        x = np.column_stack([data[key] for key in data])
        y = np.random.randint(0, n_classes, 240)

        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.22, random_state=42
        )
        model = RandomForestClassifier(n_estimators=n_trees, random_state=42)
        model.fit(x_train, y_train)
        y_pred = model.predict(x_test)
        accuracy = accuracy_score(y_test, y_pred)
        importances = model.feature_importances_

        self.ax1.clear()
        self.ax1.bar(
            ["X1", "X2", "X3"],
            importances,
            color=[PLOT_COLORS["blue"], PLOT_COLORS["orange"], PLOT_COLORS["green"]],
        )
        self.ax1.set_title("Importance des variables")
        self.ax1.set_ylabel("Importance")
        self.ax1.set_ylim(0, max(0.45, importances.max() + 0.12))

        self.ax2.clear()
        scatter = self.ax2.scatter(
            x_test[:, 0],
            x_test[:, 1],
            c=y_pred,
            cmap="viridis",
            alpha=0.78,
            s=42,
            edgecolors="#0f172a",
            linewidths=0.3,
        )
        self.ax2.set_title("Predictions (X1 vs X2)")
        self.ax2.set_xlabel("X1")
        self.ax2.set_ylabel("X2")
        if self.colorbar is not None:
            self.colorbar.remove()
        self.colorbar = self.fig.colorbar(
            scatter, ax=self.ax2, fraction=0.046, pad=0.04, label="Classe"
        )
        self.colorbar.ax.yaxis.label.set_color("#e5e7eb")
        self.colorbar.ax.tick_params(colors="#94a3b8")
        style_axes(self.ax1, self.ax2)
        self.fig.tight_layout()
        self.canvas.draw()

        write_results(
            self.result_box,
            "Resultats du modele\n"
            f"Accuracy : {accuracy:.4f}\n"
            f"Arbres : {n_trees}\n"
            f"Classes : {n_classes}\n\n"
            "Poids des variables\n"
            f"X1 : {importances[0]:.2%}\n"
            f"X2 : {importances[1]:.2%}\n"
            f"X3 : {importances[2]:.2%}",
        )
