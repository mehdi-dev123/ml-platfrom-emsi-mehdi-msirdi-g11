import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

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


class ClusteringTab:
    def __init__(self, parent):
        self.parent = parent
        self._build_ui()

    def _build_ui(self):
        controls, chart = create_tab_layout(self.parent)
        section_title(
            controls,
            "Clustering K-Means 3D",
            "Trois variables aleatoires, centres de clusters et score silhouette.",
        )

        self.x1_min = labeled_slider(controls, "X1 minimum", -20, 0, -10)
        self.x1_max = labeled_slider(controls, "X1 maximum", 1, 20, 10)
        self.x2_min = labeled_slider(controls, "X2 minimum", -10, 0, -5)
        self.x2_max = labeled_slider(controls, "X2 maximum", 1, 25, 15)
        self.x3_min = labeled_slider(controls, "X3 minimum", 0, 5, 0)
        self.x3_max = labeled_slider(controls, "X3 maximum", 10, 30, 20)
        self.k = labeled_slider(controls, "Nombre de clusters K", 2, 8, 3, 6)
        self.n = labeled_slider(controls, "Taille echantillon", 50, 500, 150, 45)

        primary_button(controls, "Generer et clusterer", self._run).pack(
            pady=(18, 12), padx=16, fill="x"
        )

        self.result_box = result_box(controls, height=170)
        self.result_box.pack(padx=16, pady=(0, 16), fill="x")

        self.fig = plt.figure(figsize=(8, 6))
        self.ax = self.fig.add_subplot(111, projection="3d")
        self.canvas = FigureCanvasTkAgg(self.fig, master=chart)
        add_canvas(self.canvas, chart)
        self.ax.set_title("Cliquez sur 'Generer et clusterer'")
        style_axes(self.ax)
        self.canvas.draw()

    def _run(self):
        k = int(self.k.get())
        n = int(self.n.get())
        ranges = [
            (int(self.x1_min.get()), int(self.x1_max.get())),
            (int(self.x2_min.get()), int(self.x2_max.get())),
            (int(self.x3_min.get()), int(self.x3_max.get())),
        ]
        data = generate_multivar(n, ranges)
        x = np.column_stack([data["X1"], data["X2"], data["X3"]])

        model = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = model.fit_predict(x)
        silhouette = silhouette_score(x, labels) if k > 1 else 0

        palette = [
            PLOT_COLORS["blue"],
            PLOT_COLORS["orange"],
            PLOT_COLORS["green"],
            PLOT_COLORS["purple"],
            PLOT_COLORS["red"],
            PLOT_COLORS["yellow"],
        ]

        self.ax.clear()
        for i in range(k):
            mask = labels == i
            self.ax.scatter(
                x[mask, 0],
                x[mask, 1],
                x[mask, 2],
                label=f"Cluster {i + 1}",
                color=palette[i % len(palette)],
                alpha=0.75,
                s=34,
            )

        self.ax.scatter(
            model.cluster_centers_[:, 0],
            model.cluster_centers_[:, 1],
            model.cluster_centers_[:, 2],
            s=220,
            marker="*",
            c="#f8fafc",
            edgecolors="#0f172a",
            linewidths=0.7,
            label="Centres",
        )

        self.ax.set_title(f"Clustering 3D K-Means (K={k})")
        self.ax.set_xlabel("X1")
        self.ax.set_ylabel("X2")
        self.ax.set_zlabel("X3")
        self.ax.legend(fontsize=8)
        self.ax.view_init(elev=25, azim=-48)
        style_axes(self.ax)
        self.canvas.draw()

        centers = "\n".join(
            f"C{i + 1}: [{c[0]:.1f}, {c[1]:.1f}, {c[2]:.1f}]"
            for i, c in enumerate(model.cluster_centers_)
        )
        write_results(
            self.result_box,
            f"Clusters : {k}\n"
            f"Score silhouette : {silhouette:.4f}\n"
            f"Points generes : {n}\n\n"
            f"Centres\n{centers}",
        )
