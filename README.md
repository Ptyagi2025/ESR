# Barrier Property
ESR peak analysis
# Tunneling Junction Analyzer

Estimate **barrier height** and **barrier thickness** from I–V data of metal–insulator–metal (MIM) tunneling junctions using the
 **Simmons** and **Brinkman–Dynes–Rowell (BDR)** models.

---

## ✨ Features

- Fit experimental **I–V** (or **J–V**) data to:
  - **Simmons (1963)** rectangular, symmetric barrier
  - **Brinkman–Dynes–Rowell (1970)** slightly **asymmetric** trapezoidal barrier
- Extract barrier **height(s)** (eV) and **thickness** (nm)
- Choose **nonlinear least-squares** or **robust** (Huber/Tukey) regression
- Automatic **unit handling** (A vs mA, cm² vs m², etc.)
- Export **fit reports**, **parameter covariance**, and **publication-ready plots**
- CLI **and** Python API
- Simple **Tkinter GUI** for quick interaction

---

## 📦 Installation

```bash
# Recommended: create a fresh environment
python -m venv .venv && source .venv/bin/activate   # (Windows: .venv\Scripts\activate)

pip install -U pip
pip install -r requirements.txt
```

---

## 🖥️ Graphical Interface

Launch the GUI with:

```bash
python -m esr.gui
```

Load a CSV file containing voltage and current (or current density) columns,
select a model, and click **Fit** to estimate barrier parameters.
