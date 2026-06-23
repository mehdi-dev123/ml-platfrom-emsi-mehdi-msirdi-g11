import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

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


class CrossValidationTab:
    def __init__(self, parent):
        self.parent = parent
        self._build_ui()

    def _build_ui(self):
        controls, chart = create_tab_layout(self.parent)
        section_title(
            controls,
            "Validation croisee",
            "Comparaison de quatre modeles avec cross_val_score.",
        )

        self.x1_min = labeled_slider(controls, "X1 minimum", -20, 0, -10)
        self.x1_max = labeled_slider(controls, "X1 maximum", 1, 20, 10)
        self.x2_min = labeled_slider(controls, "X2 minimum", -10, 0, -5)
        self.x2_max = labeled_slider(controls, "X2 maximum", 1, 25, 15)
        self.x3_min = labeled_slider(controls, "X3 minimum", 0, 5, 0)
        self.x3_max = labeled_slider(controls, "X3 maximum", 10, 30, 20)
        self.folds = labeled_slider(controls, "Nombre de folds", 2, 10, 5, 8)
        self.n_data = labeled_slider(controls, "Taille dataset", 100, 500, 200, 40)

        primary_button(controls, "Comparer les modeles", self._run).pack(
            pady=(18, 12), padx=16, fill="x"
        )

        self.result_box = result_box(controls, height=230)
        self.result_box.pack(padx=16, pady=(0, 16), fill="x")

        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(10, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=chart)
        add_canvas(self.canvas, chart)
        self.ax1.set_title("Accuracy moyenne")
        self.ax2.set_title("Evolution par fold")
        style_axes(self.ax1, self.ax2)
        self.canvas.draw()

    def _run(self):
        x1_min = int(self.x1_min.get())
        x1_max = int(self.x1_max.get())
        x2_min = int(self.x2_min.get())
        x2_max = int(self.x2_max.get())
        x3_min = int(self.x3_min.get())
        x3_max = int(self.x3_max.get())
        folds = int(self.folds.get())
        n = int(self.n_data.get())

        if x1_min >= x1_max or x2_min >= x2_max or x3_min >= x3_max:
            write_results(
                self.result_box,
                "Erreur : chaque minimum doit etre inferieur au maximum correspondant.",
            )
            return

        data = generate_multivar(n, [(x1_min, x1_max), (x2_min, x2_max), (x3_min, x3_max)])
        x = np.column_stack([data[key] for key in data])
        y = np.random.randint(0, 3, n)

        models = {
            "Random Forest": RandomForestClassifier(n_estimators=50, random_state=42),
            "Reseau NN": MLPClassifier(max_iter=300, random_state=42),
            "SVM": SVC(random_state=42),
            "Arbre": DecisionTreeClassifier(random_state=42),
        }

        scores = {
            name: cross_val_score(model, x, y, cv=folds, scoring="accuracy")
            for name, model in models.items()
        }
        names = list(scores.keys())
        means = [score.mean() for score in scores.values()]
        stds = [score.std() for score in scores.values()]
        colors = [
            PLOT_COLORS["blue"],
            PLOT_COLORS["orange"],
            PLOT_COLORS["green"],
            PLOT_COLORS["purple"],
        ]

        self.ax1.clear()
        self.ax1.bar(names, means, yerr=stds, capsize=5, color=colors, alpha=0.9)
        self.ax1.set_title("Accuracy moyenne")
        self.ax1.set_ylabel("Accuracy")
        self.ax1.set_ylim(0, 1.05)
        self.ax1.tick_params(axis="x", rotation=12)

        self.ax2.clear()
        for i, (name, score) in enumerate(scores.items()):
            self.ax2.plot(
                range(1, folds + 1),
                score,
                marker="o",
                linewidth=2,
                label=name,
                color=colors[i],
            )
        self.ax2.set_title("Evolution par fold")
        self.ax2.set_xlabel("Fold")
        self.ax2.set_ylabel("Accuracy")
        self.ax2.set_ylim(0, 1.05)
        self.ax2.legend(fontsize=8)
        style_axes(self.ax1, self.ax2)
        self.fig.tight_layout()
        self.canvas.draw()

        best = names[int(np.argmax(means))]
        rows = [
            f"{name}: {score.mean():.4f} +/- {score.std():.4f}"
            for name, score in scores.items()
        ]
        write_results(
            self.result_box,
            "Scores moyens\n"
            + "\n".join(rows)
            + f"\n\nMeilleur modele : {best}\nFolds : {folds}\nObservations : {n}",
        )
