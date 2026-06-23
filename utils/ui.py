import customtkinter as ctk
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt


# Each entry is (light_mode, dark_mode). CustomTkinter resolves the tuple
# automatically based on the active appearance mode, so a single definition
# drives both themes and the dark/light toggle works for the whole UI.
COLORS = {
    "bg": ("#eef2f7", "#0f172a"),
    "surface": ("#ffffff", "#111827"),
    "panel": ("#f8fafc", "#172033"),
    "panel_light": ("#e2e8f0", "#1f2937"),
    "border": ("#cbd5e1", "#334155"),
    "text": ("#0f172a", "#e5e7eb"),
    "muted": ("#64748b", "#94a3b8"),
    "accent": ("#0ea5e9", "#38bdf8"),
    "accent_hover": ("#0284c7", "#0ea5e9"),
    "success": ("#16a34a", "#22c55e"),
    "warning": ("#d97706", "#f59e0b"),
    "danger": ("#dc2626", "#ef4444"),
}


def resolve(name):
    """Return the color for the current appearance mode (for matplotlib)."""
    light, dark = COLORS[name]
    return light if ctk.get_appearance_mode() == "Light" else dark


PLOT_COLORS = {
    "blue": "#38bdf8",
    "green": "#22c55e",
    "orange": "#f97316",
    "red": "#ef4444",
    "purple": "#a78bfa",
    "yellow": "#facc15",
}


def apply_matplotlib_theme():
    """Sync matplotlib rcParams with the active appearance mode."""
    plt.rcParams.update(
        {
            "figure.facecolor": resolve("surface"),
            "axes.facecolor": resolve("surface"),
            "axes.edgecolor": resolve("border"),
            "axes.labelcolor": resolve("text"),
            "axes.titlecolor": resolve("text"),
            "xtick.color": resolve("muted"),
            "ytick.color": resolve("muted"),
            "grid.color": resolve("border"),
            "text.color": resolve("text"),
            "legend.facecolor": resolve("panel"),
            "legend.edgecolor": resolve("border"),
        }
    )


def setup_app_theme():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    apply_matplotlib_theme()


def refresh_appearance(mode):
    """Switch theme and restyle existing matplotlib figures to match."""
    ctk.set_appearance_mode(mode)
    apply_matplotlib_theme()
    for num in plt.get_fignums():
        fig = plt.figure(num)
        fig.set_facecolor(resolve("surface"))
        for ax in fig.get_axes():
            _restyle_axis(ax)
        fig.canvas.draw_idle()


def create_tab_layout(parent):
    parent.grid_columnconfigure(1, weight=1)
    parent.grid_rowconfigure(0, weight=1)

    controls = ctk.CTkScrollableFrame(
        parent,
        width=300,
        fg_color=COLORS["panel"],
        corner_radius=8,
        border_width=1,
        border_color=COLORS["border"],
    )
    controls.grid(row=0, column=0, sticky="nsw", padx=(12, 8), pady=12)

    chart = ctk.CTkFrame(
        parent,
        fg_color=COLORS["surface"],
        corner_radius=8,
        border_width=1,
        border_color=COLORS["border"],
    )
    chart.grid(row=0, column=1, sticky="nsew", padx=(8, 12), pady=12)
    chart.grid_columnconfigure(0, weight=1)
    chart.grid_rowconfigure(0, weight=1)
    return controls, chart


def section_title(parent, title, subtitle=None):
    ctk.CTkLabel(
        parent,
        text=title,
        font=ctk.CTkFont(size=16, weight="bold"),
        text_color=COLORS["text"],
    ).pack(anchor="w", padx=16, pady=(16, 2))
    if subtitle:
        ctk.CTkLabel(
            parent,
            text=subtitle,
            font=ctk.CTkFont(size=12),
            text_color=COLORS["muted"],
            wraplength=250,
            justify="left",
        ).pack(anchor="w", padx=16, pady=(0, 12))


def labeled_slider(parent, label, from_, to, default, steps=None, value_format=None):
    row = ctk.CTkFrame(parent, fg_color="transparent")
    row.pack(fill="x", padx=16, pady=(8, 0))
    row.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(row, text=label, text_color=COLORS["text"]).grid(row=0, column=0, sticky="w")
    value_var = ctk.StringVar(value=_format_value(default, value_format))
    value = ctk.CTkEntry(
        row,
        textvariable=value_var,
        width=54,
        height=24,
        fg_color=COLORS["panel_light"],
        corner_radius=6,
        text_color=COLORS["accent"],
        font=ctk.CTkFont(size=12, weight="bold"),
        justify="center",
        border_width=1,
        border_color=COLORS["border"],
    )
    value.grid(row=0, column=1, sticky="e")

    slider = ctk.CTkSlider(
        parent,
        from_=from_,
        to=to,
        number_of_steps=steps if steps is not None else max(1, abs(int(to - from_))),
        button_color=COLORS["accent"],
        button_hover_color=COLORS["accent_hover"],
        progress_color=COLORS["accent"],
    )
    slider.set(default)
    slider.pack(fill="x", padx=16, pady=(4, 2))

    range_row = ctk.CTkFrame(parent, fg_color="transparent")
    range_row.pack(fill="x", padx=16, pady=(0, 6))
    range_row.grid_columnconfigure(1, weight=1)
    ctk.CTkLabel(
        range_row,
        text=f"Min: {_format_value(from_, value_format)}",
        font=ctk.CTkFont(size=11),
        text_color=COLORS["muted"],
    ).grid(row=0, column=0, sticky="w")
    ctk.CTkLabel(
        range_row,
        text=f"Max: {_format_value(to, value_format)}",
        font=ctk.CTkFont(size=11),
        text_color=COLORS["muted"],
    ).grid(row=0, column=2, sticky="e")

    def sync_entry(raw_value):
        value_var.set(_format_value(raw_value, value_format))

    def apply_entry(_event=None):
        try:
            raw_value = float(value_var.get().replace(",", "."))
        except ValueError:
            sync_entry(slider.get())
            return

        clamped = min(max(raw_value, from_), to)
        if steps is not None and steps > 0:
            step_size = (to - from_) / steps
            clamped = from_ + round((clamped - from_) / step_size) * step_size
        slider.set(clamped)
        sync_entry(clamped)

    slider.configure(command=sync_entry)
    value.bind("<Return>", apply_entry)
    value.bind("<FocusOut>", apply_entry)
    return slider


def primary_button(parent, text, command, busy_text="Calcul en cours..."):
    button = ctk.CTkButton(
        parent,
        text=text,
        height=38,
        corner_radius=8,
        font=ctk.CTkFont(size=13, weight="bold"),
        fg_color=COLORS["accent"],
        hover_color=COLORS["accent_hover"],
        text_color="#07111f",
    )

    def run_with_feedback():
        # Disable and relabel before the (blocking) computation so the user
        # gets immediate feedback instead of a frozen, silent UI.
        button.configure(text=busy_text, state="disabled")
        button.update_idletasks()
        try:
            command()
        finally:
            button.configure(text=text, state="normal")

    button.configure(command=run_with_feedback)
    return button


def result_box(parent, height=150):
    box = ctk.CTkTextbox(
        parent,
        height=height,
        corner_radius=8,
        fg_color=COLORS["surface"],
        border_width=1,
        border_color=COLORS["border"],
        text_color=COLORS["text"],
    )
    return box


def add_canvas(canvas, parent):
    widget = canvas.get_tk_widget()
    widget.configure(highlightthickness=0, bd=0)
    widget.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)


def _restyle_axis(ax):
    ax.set_facecolor(resolve("surface"))
    for spine in ax.spines.values():
        spine.set_color(resolve("border"))
    ax.tick_params(colors=resolve("muted"))
    ax.xaxis.label.set_color(resolve("text"))
    ax.yaxis.label.set_color(resolve("text"))
    ax.title.set_color(resolve("text"))
    ax.grid(color=resolve("border"), alpha=0.25)


def style_axes(*axes):
    for ax in axes:
        _restyle_axis(ax)
        ax.grid(True)


def write_results(box, text):
    box.configure(state="normal")
    box.delete("1.0", "end")
    box.insert("end", text)
    box.configure(state="disabled")


def _format_value(value, value_format):
    if value_format:
        return value_format(value)
    if float(value).is_integer():
        return str(int(value))
    return f"{value:.1f}"
