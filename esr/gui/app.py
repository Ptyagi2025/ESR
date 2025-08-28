"""Simple Tkinter-based GUI for tunneling junction analysis.

This module wires together the data loading, model selection, and fitting
utilities into a minimal graphical interface.  It is intentionally
light‑weight, focusing on clarity over features.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

from .. import data, fitting

matplotlib.use("Agg")  # ensure a non-interactive backend by default


class AnalyzerApp(tk.Tk):
    """Main application window."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Tunneling Junction Analyzer")
        self.geometry("800x600")

        self._build_ui()

        self.df = None  # loaded data
        self.figure = plt.Figure(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # ------------------------------------------------------------------
    def _build_ui(self) -> None:
        """Create and place all widgets."""

        toolbar = tk.Frame(self)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        load_btn = tk.Button(toolbar, text="Load CSV", command=self.load_data)
        load_btn.pack(side=tk.LEFT)

        self.model_var = tk.StringVar(value="simmons")
        model_menu = ttk.OptionMenu(
            toolbar, self.model_var, "simmons", "simmons", "bdr"
        )
        model_menu.pack(side=tk.LEFT, padx=5)

        fit_btn = tk.Button(toolbar, text="Fit", command=self.run_fit)
        fit_btn.pack(side=tk.LEFT, padx=5)

        self.result_var = tk.StringVar(value="No results yet")
        result_label = tk.Label(self, textvariable=self.result_var)
        result_label.pack(side=tk.TOP, fill=tk.X, pady=5)

        self.plot_frame = tk.Frame(self)
        self.plot_frame.pack(fill=tk.BOTH, expand=True)

    # ------------------------------------------------------------------
    def load_data(self) -> None:
        """Load I–V data from a CSV file."""

        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not path:
            return
        try:
            self.df = data.load_iv_csv(path)
            self.result_var.set(f"Loaded {len(self.df)} rows from {path}")
            self._plot_raw()
        except Exception as exc:  # pragma: no cover - GUI feedback
            messagebox.showerror("Error", str(exc))

    # ------------------------------------------------------------------
    def _plot_raw(self) -> None:
        if self.df is None:
            return
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(self.df.iloc[:, 0], self.df.iloc[:, 1], "o", label="data")
        ax.set_xlabel("Voltage")
        ax.set_ylabel("Current / Current density")
        ax.legend()
        self.canvas.draw()

    # ------------------------------------------------------------------
    def run_fit(self) -> None:
        """Run the selected model fit on the loaded data."""

        if self.df is None:
            messagebox.showinfo("No data", "Please load a CSV file first")
            return

        V = self.df.iloc[:, 0].to_numpy(dtype=float)
        J = self.df.iloc[:, 1].to_numpy(dtype=float)

        model_name = self.model_var.get()
        try:
            if model_name == "simmons":
                params, _ = fitting.fit_simmons(V, J)
                desc = f"Simmons fit: phi={params[0]:.3g} eV, s={params[1]:.3g} nm"
                fitted = fitting.models.simmons_current_density(V, *params)
            else:
                params, _ = fitting.fit_bdr(V, J)
                desc = (
                    f"BDR fit: phi={params[0]:.3g} eV, s={params[1]:.3g} nm, Δϕ={params[2]:.3g} eV"
                )
                fitted = fitting.models.bdr_current_density(V, *params)

            self.result_var.set(desc)
            self._plot_raw()
            ax = self.figure.axes[0]
            ax.plot(V, fitted, label="fit")
            ax.legend()
            self.canvas.draw()
        except Exception as exc:  # pragma: no cover - GUI feedback
            messagebox.showerror("Fit error", str(exc))


# ----------------------------------------------------------------------------

def main() -> None:
    """Entry point for launching the GUI."""

    app = AnalyzerApp()
    app.mainloop()


if __name__ == "__main__":  # pragma: no cover
    main()
