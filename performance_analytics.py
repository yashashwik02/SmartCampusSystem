"""
performance_analytics.py  —  Lab 8
"""
import tkinter as tk
from tkinter import messagebox
import json, os

BG = "#0d1117"; CARD = "#161b22"; ACCENT = "#00c8ff"
TEXT = "#e6edf3"; MUTED = "#8b949e"; FONT_MONO = "Courier New"
DB_FILE = "student_records_db.json"

def _load():
    if os.path.exists(DB_FILE):
        with open(DB_FILE) as f:
            return json.load(f)
    return []

def open_performance_analytics():
    try:
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        HAS_LIBS = True
    except ImportError:
        HAS_LIBS = False

    records = _load()

    win = tk.Toplevel()
    win.title("Lab 8 — Performance Analytics")
    win.geometry("900x640")
    win.configure(bg=BG)
    win.resizable(False, False)

    tk.Frame(win, bg=ACCENT, height=4).pack(fill="x")
    tk.Label(win, text="PERFORMANCE ANALYTICS",
             font=(FONT_MONO, 17, "bold"), fg=ACCENT, bg=BG).pack(pady=(12,2))

    if not records:
        tk.Label(win, text="No student records found.\nAdd records via Lab 3 first.",
                 font=(FONT_MONO, 13), fg=MUTED, bg=BG).pack(expand=True)
        return

    # Extract data
    names, marks = [], []
    for r in records:
        try:
            m = float(r.get("marks", 0))
            names.append(r.get("name", "?")[:10])
            marks.append(m)
        except Exception:
            pass

    if not marks:
        tk.Label(win, text="No numeric marks found in records.",
                 font=(FONT_MONO, 12), fg=MUTED, bg=BG).pack(expand=True)
        return

    # Stats panel
    import statistics
    stat_frame = tk.Frame(win, bg=CARD, padx=20, pady=12)
    stat_frame.pack(padx=24, pady=8, fill="x")

    stats = {
        "Total Students": len(marks),
        "Average Marks":  f"{statistics.mean(marks):.1f}",
        "Highest Marks":  f"{max(marks):.1f}",
        "Lowest Marks":   f"{min(marks):.1f}",
        "Pass (≥40)":     sum(1 for m in marks if m >= 40),
        "Fail (<40)":     sum(1 for m in marks if m < 40),
    }
    cols = tk.Frame(stat_frame, bg=CARD)
    cols.pack()
    for k, v in stats.items():
        box = tk.Frame(cols, bg="#1c2333", padx=14, pady=10)
        box.pack(side="left", padx=8)
        tk.Label(box, text=str(v), font=(FONT_MONO, 16, "bold"),
                 fg=ACCENT, bg="#1c2333").pack()
        tk.Label(box, text=k, font=(FONT_MONO, 8),
                 fg=MUTED, bg="#1c2333").pack()

    if not HAS_LIBS:
        tk.Label(win, text="Install matplotlib & pandas for charts:\n  pip install matplotlib pandas numpy",
                 font=(FONT_MONO, 11), fg=MUTED, bg=BG).pack(pady=20)
        return

    # Charts
    fig, axes = plt.subplots(1, 2, figsize=(8.5, 3.5))
    fig.patch.set_facecolor("#161b22")

    # Bar chart
    ax1 = axes[0]
    ax1.set_facecolor("#0d1117")
    bars = ax1.bar(names, marks, color=ACCENT, edgecolor="#0d1117")
    ax1.set_title("Marks per Student", color=TEXT, fontsize=10)
    ax1.set_xlabel("Student", color=MUTED, fontsize=8)
    ax1.set_ylabel("Marks", color=MUTED, fontsize=8)
    ax1.tick_params(colors=MUTED, labelsize=7)
    ax1.spines[:].set_color("#30363d")
    for bar, m in zip(bars, marks):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                 f"{m:.0f}", ha="center", va="bottom", fontsize=7, color=TEXT)
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=30, ha="right")

    # Pie chart — grade distribution
    grades = {"O(≥90)":0, "A+(80)":0, "A(70)":0, "B+(60)":0, "B(50)":0, "C(40)":0, "F":0}
    for m in marks:
        if m>=90: grades["O(≥90)"]+=1
        elif m>=80: grades["A+(80)"]+=1
        elif m>=70: grades["A(70)"]+=1
        elif m>=60: grades["B+(60)"]+=1
        elif m>=50: grades["B(50)"]+=1
        elif m>=40: grades["C(40)"]+=1
        else: grades["F"]+=1
    non_zero = {k:v for k,v in grades.items() if v > 0}
    colors = ["#00c8ff","#0099cc","#007ea7","#005f80","#003f55","#002233","#ff4455"]
    ax2 = axes[1]
    ax2.set_facecolor("#161b22")
    ax2.pie(non_zero.values(), labels=non_zero.keys(),
            colors=colors[:len(non_zero)], autopct="%1.0f%%",
            textprops={"color": TEXT, "fontsize": 8},
            startangle=90)
    ax2.set_title("Grade Distribution", color=TEXT, fontsize=10)

    fig.tight_layout(pad=2)
    canvas_widget = FigureCanvasTkAgg(fig, master=win)
    canvas_widget.draw()
    canvas_widget.get_tk_widget().pack(padx=24, pady=8, fill="both", expand=True)