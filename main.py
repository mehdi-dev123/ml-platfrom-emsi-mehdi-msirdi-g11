import sys
from pathlib import Path

import customtkinter as ctk
import matplotlib
from PIL import Image

matplotlib.use("TkAgg")

# Tab modules (and their heavy sklearn/statsmodels dependencies) are imported
# lazily when the user opens the workspace, so the home screen appears instantly
# instead of waiting ~3s for those libraries to load at startup.
from utils.ui import COLORS, refresh_appearance, setup_app_theme


setup_app_theme()


def resource_path(relative_path):
    base_path = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return base_path / relative_path


class MLApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Plateforme IA - Machine Learning")
        self.minsize(1050, 680)
        self._center_window(1280, 780)
        self.configure(fg_color=COLORS["bg"])

        self.header = None
        self.tabs = None
        self._build_home()

    def _center_window(self, width, height):
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = max(0, (screen_width - width) // 2)
        y = max(0, (screen_height - height) // 3)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _build_home(self):
        self.home = ctk.CTkFrame(self, fg_color=COLORS["bg"])
        self.home.pack(fill="both", expand=True)
        self.home.grid_columnconfigure(0, weight=1)
        self.home.grid_rowconfigure(0, weight=1)

        content = ctk.CTkFrame(
            self.home,
            width=760,
            height=560,
            fg_color=COLORS["panel"],
            corner_radius=8,
            border_width=1,
            border_color=COLORS["border"],
        )
        content.grid(row=0, column=0, padx=32, pady=32)
        content.grid_propagate(False)
        content.grid_columnconfigure(0, weight=1)

        logo_path = resource_path("assets/emsi_logo.png")
        if logo_path.exists():
            logo_image = Image.open(logo_path)
            self.home_logo_image = ctk.CTkImage(
                light_image=logo_image,
                dark_image=logo_image,
                size=(250, 70),
            )
            ctk.CTkLabel(content, image=self.home_logo_image, text="").grid(
                row=0, column=0, pady=(44, 20)
            )

        ctk.CTkLabel(
            content,
            text="Plateforme IA - Machine Learning",
            font=ctk.CTkFont(size=34, weight="bold"),
            text_color=COLORS["text"],
        ).grid(row=1, column=0, padx=36, pady=(6, 8))
        ctk.CTkLabel(
            content,
            text="Application interactive pour explorer les modeles d'apprentissage automatique",
            font=ctk.CTkFont(size=15),
            text_color=COLORS["muted"],
            wraplength=620,
            justify="center",
        ).grid(row=2, column=0, padx=36, pady=(0, 30))

        info = ctk.CTkFrame(content, fg_color=COLORS["surface"], corner_radius=8)
        info.grid(row=3, column=0, sticky="ew", padx=56, pady=(0, 30))
        info.grid_columnconfigure(0, weight=1)
        info.grid_columnconfigure(1, weight=1)

        self._home_info_item(info, "Realise par", "MSIRDI Mahdi", 0)
        self._home_info_item(info, "Encadre par", "EL MKHALET MOUNA", 1)

        ctk.CTkLabel(
            content,
            text="Cliquez ici pour acceder aux onglets de l'application",
            font=ctk.CTkFont(size=13),
            text_color=COLORS["muted"],
        ).grid(row=4, column=0, pady=(0, 10))
        ctk.CTkButton(
            content,
            text="ACCEDER AUX ONGLETS",
            height=58,
            width=320,
            corner_radius=8,
            font=ctk.CTkFont(size=17, weight="bold"),
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            text_color="#07111f",
            command=self._show_application,
        ).grid(row=5, column=0, pady=(0, 44))

    def _home_info_item(self, parent, label, value, column):
        item = ctk.CTkFrame(parent, fg_color="transparent")
        item.grid(row=0, column=column, sticky="ew", padx=20, pady=18)
        ctk.CTkLabel(
            item,
            text=label,
            font=ctk.CTkFont(size=12),
            text_color=COLORS["muted"],
        ).pack(anchor="center")
        ctk.CTkLabel(
            item,
            text=value,
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLORS["text"],
        ).pack(anchor="center", pady=(5, 0))

    def _show_application(self):
        self.home.destroy()
        self._show_loading()
        # Let the loading screen paint before the blocking import/build work.
        self.after(50, lambda: self._build_application_step(0))

    def _show_loading(self):
        self.loading = ctk.CTkFrame(self, fg_color=COLORS["bg"])
        self.loading.pack(fill="both", expand=True)
        self.loading.grid_columnconfigure(0, weight=1)
        self.loading.grid_rowconfigure(0, weight=1)

        box = ctk.CTkFrame(self.loading, fg_color="transparent")
        box.grid(row=0, column=0)

        logo_path = resource_path("assets/emsi_logo.png")
        if logo_path.exists():
            logo_image = Image.open(logo_path)
            self.loading_logo_image = ctk.CTkImage(
                light_image=logo_image,
                dark_image=logo_image,
                size=(214, 58),
            )
            ctk.CTkLabel(box, image=self.loading_logo_image, text="").pack(pady=(0, 26))

        ctk.CTkLabel(
            box,
            text="Preparation de la plateforme",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COLORS["text"],
        ).pack()
        self.loading_status = ctk.CTkLabel(
            box,
            text="Initialisation...",
            font=ctk.CTkFont(size=13),
            text_color=COLORS["muted"],
        )
        self.loading_status.pack(pady=(6, 22))

        self.loading_bar = ctk.CTkProgressBar(
            box,
            width=320,
            height=10,
            corner_radius=6,
            fg_color=COLORS["panel_light"],
            progress_color=COLORS["accent"],
        )
        self.loading_bar.set(0)
        self.loading_bar.pack()

    def _set_loading(self, fraction, status):
        self.loading_bar.set(fraction)
        self.loading_status.configure(text=status)
        self.loading_bar.update_idletasks()

    def _build_application_step(self, index):
        if index == 0:
            self._set_loading(0.08, "Chargement des bibliotheques ML...")
            from tabs.clustering import ClusteringTab
            from tabs.cross_validation import CrossValidationTab
            from tabs.neural_network import NeuralNetworkTab
            from tabs.random_forest import RandomForestTab
            from tabs.regression import RegressionTab
            from tabs.time_series import TimeSeriesTab

            self._tab_specs = [
                ("Regression", RegressionTab),
                ("Clustering 3D", ClusteringTab),
                ("Random Forest", RandomForestTab),
                ("Series temp.", TimeSeriesTab),
                ("Reseau neuronal", NeuralNetworkTab),
                ("Validation croisee", CrossValidationTab),
            ]
            self._build_tabview()
            self._set_loading(0.2, "Construction de l'interface...")
            self.after(20, lambda: self._build_application_step(1))
            return

        spec_index = index - 1
        if spec_index < len(self._tab_specs):
            name, tab_class = self._tab_specs[spec_index]
            self._set_loading(
                0.2 + 0.8 * spec_index / len(self._tab_specs),
                f"Preparation : {name}",
            )
            self.tabs.add(name)
            tab_class(self.tabs.tab(name))
            self.after(20, lambda: self._build_application_step(index + 1))
            return

        self._set_loading(1.0, "Pret")
        self.loading.destroy()
        self._build_header()
        self.tabs.pack(padx=24, pady=(8, 20), fill="both", expand=True)

    def _build_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        self.header = header
        header.pack(fill="x", padx=24, pady=(18, 8))
        header.grid_columnconfigure(1, weight=1)

        logo_path = resource_path("assets/emsi_logo.png")
        if logo_path.exists():
            logo_image = Image.open(logo_path)
            self.logo_image = ctk.CTkImage(
                light_image=logo_image,
                dark_image=logo_image,
                size=(178, 48),
            )
            ctk.CTkLabel(header, image=self.logo_image, text="").grid(
                row=0, column=0, sticky="w", padx=(0, 18)
            )

        title_block = ctk.CTkFrame(header, fg_color="transparent")
        title_block.grid(row=0, column=1, sticky="w")

        ctk.CTkLabel(
            title_block,
            text="Plateforme d'analyse intelligente",
            font=ctk.CTkFont(size=25, weight="bold"),
            text_color=COLORS["text"],
        ).pack(anchor="w")
        ctk.CTkLabel(
            title_block,
            text="Generation aleatoire de donnees, modeles ML et visualisations interactives",
            font=ctk.CTkFont(size=13),
            text_color=COLORS["muted"],
        ).pack(anchor="w", pady=(2, 0))

        self.mode_switch = ctk.CTkSegmentedButton(
            header,
            values=["Sombre", "Clair"],
            command=self._change_mode,
            selected_color=COLORS["accent"],
            selected_hover_color=COLORS["accent_hover"],
            unselected_color=COLORS["panel"],
            unselected_hover_color=COLORS["panel_light"],
        )
        self.mode_switch.set("Sombre")
        self.mode_switch.grid(row=0, column=2, sticky="e", padx=(16, 0))

    def _build_tabview(self):
        # Created unpacked; tabs are added incrementally during loading and the
        # whole view is packed only once everything is ready.
        self.tabs = ctk.CTkTabview(
            self,
            fg_color=COLORS["panel"],
            segmented_button_fg_color=COLORS["surface"],
            segmented_button_selected_color=COLORS["accent"],
            segmented_button_selected_hover_color=COLORS["accent_hover"],
            segmented_button_unselected_color=COLORS["surface"],
            segmented_button_unselected_hover_color=COLORS["panel_light"],
            text_color=COLORS["text"],
            corner_radius=8,
        )

    def _change_mode(self, value):
        refresh_appearance("light" if value == "Clair" else "dark")


if __name__ == "__main__":
    app = MLApp()
    app.mainloop()
