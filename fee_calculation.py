"""
fee_calculation.py  —  Lab 5
"""
import tkinter as tk
from tkinter import messagebox
import datetime

BG = "#0d1117"; CARD = "#161b22"; ACCENT = "#00c8ff"
TEXT = "#e6edf3"; MUTED = "#8b949e"; FONT_MONO = "Courier New"

FEE_STRUCTURE = {
    "CSE":     125000,
    "ECE":     115000,
    "ME":      110000,
    "Civil":   105000,
    "Other":   100000,
}

def _entry(parent, width=30):
    return tk.Entry(parent, width=width, font=(FONT_MONO, 11),
                    bg="#1c2333", fg="white", insertbackground=ACCENT,
                    relief="flat", highlightthickness=1,
                    highlightcolor=ACCENT, highlightbackground="#30363d")

def open_fee_calculation():
    win = tk.Toplevel()
    win.title("Lab 5 — Fee Calculation")
    win.geometry("640x560")
    win.configure(bg=BG)
    win.resizable(False, False)

    tk.Frame(win, bg=ACCENT, height=4).pack(fill="x")
    tk.Label(win, text="FEE CALCULATION",
             font=(FONT_MONO, 17, "bold"), fg=ACCENT, bg=BG).pack(pady=(14,6))

    card = tk.Frame(win, bg=CARD, padx=28, pady=20)
    card.pack(padx=28, fill="x")

    fields = {}
    for label, key in [("Student Name", "name"), ("USN", "usn")]:
        tk.Label(card, text=label+":", font=(FONT_MONO, 10), fg=MUTED, bg=CARD).pack(anchor="w", pady=(6,0))
        e = _entry(card)
        e.pack(anchor="w", pady=(2,0), ipady=4)
        fields[key] = e

    # Department dropdown
    tk.Label(card, text="Department:", font=(FONT_MONO, 10), fg=MUTED, bg=CARD).pack(anchor="w", pady=(10,0))
    dept_var = tk.StringVar(value="CSE")
    dept_menu = tk.OptionMenu(card, dept_var, *FEE_STRUCTURE.keys())
    dept_menu.config(font=(FONT_MONO, 10), bg="#1c2333", fg="white",
                     activebackground=ACCENT, relief="flat")
    dept_menu.pack(anchor="w", pady=(2,0))

    # Scholarship
    tk.Label(card, text="Scholarship % (0-100):", font=(FONT_MONO, 10), fg=MUTED, bg=CARD).pack(anchor="w", pady=(10,0))
    sch_entry = _entry(card, width=10)
    sch_entry.pack(anchor="w", pady=(2,0), ipady=4)

    result_var = tk.StringVar(value="")
    tk.Label(win, textvariable=result_var, font=(FONT_MONO, 12, "bold"),
             fg=ACCENT, bg=BG, justify="left").pack(pady=14, padx=28, anchor="w")

    def calculate():
        name = fields["name"].get().strip()
        usn  = fields["usn"].get().strip()
        dept = dept_var.get()
        sch_str = sch_entry.get().strip() or "0"

        if not name or not usn:
            messagebox.showerror("Missing", "Name and USN required.", parent=win); return
        try:
            sch = float(sch_str)
            if not (0 <= sch <= 100): raise ValueError
        except ValueError:
            messagebox.showerror("Invalid", "Scholarship must be 0–100.", parent=win); return

        base = FEE_STRUCTURE[dept]
        discount = base * sch / 100
        total = base - discount
        now = datetime.datetime.now().strftime("%d-%m-%Y")

        report = (
            f"FEE RECEIPT\n{'='*40}\n"
            f"  Date         : {now}\n"
            f"  Name         : {name}\n"
            f"  USN          : {usn}\n"
            f"  Department   : {dept}\n"
            f"{'='*40}\n"
            f"  Base Fee     : ₹{base:,.0f}\n"
            f"  Scholarship  : {sch}%  (-₹{discount:,.0f})\n"
            f"  Total Fee    : ₹{total:,.0f}\n"
            f"{'='*40}"
        )
        result_var.set(f"  Total Payable: ₹{total:,.0f}")

        fname = f"{usn}_fee_receipt.txt"
        with open(fname, "w") as fh:
            fh.write(report)
        messagebox.showinfo("Done", f"Fee = ₹{total:,.0f}\nSaved to {fname}", parent=win)

    tk.Button(win, text="  Calculate Fee  ", command=calculate,
              font=(FONT_MONO, 11, "bold"), bg=ACCENT, fg=BG,
              relief="flat", padx=18, pady=8, cursor="hand2").pack(pady=6)