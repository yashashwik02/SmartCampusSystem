"""
search_sort.py  —  Lab 4
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

def open_search_sort():
    records = _load()
    win = tk.Toplevel()
    win.title("Lab 4 — Search & Sort")
    win.geometry("700x520")
    win.configure(bg=BG)
    win.resizable(False, False)

    tk.Frame(win, bg=ACCENT, height=4).pack(fill="x")
    tk.Label(win, text="SEARCH & SORT STUDENTS",
             font=(FONT_MONO, 17, "bold"), fg=ACCENT, bg=BG).pack(pady=(14,6))

    # Search bar
    bar = tk.Frame(win, bg=BG)
    bar.pack(pady=10)
    tk.Label(bar, text="Search by Name / USN:", font=(FONT_MONO, 10),
             fg=MUTED, bg=BG).pack(side="left", padx=6)
    search_var = tk.StringVar()
    e = tk.Entry(bar, textvariable=search_var, width=28,
                 font=(FONT_MONO, 11), bg="#1c2333", fg="white",
                 insertbackground=ACCENT, relief="flat",
                 highlightthickness=1, highlightcolor=ACCENT,
                 highlightbackground="#30363d")
    e.pack(side="left", ipady=4, padx=4)

    # Output box
    out = tk.Text(win, font=(FONT_MONO, 10), bg=CARD, fg="#c9d1d9",
                  relief="flat", padx=12, pady=12, height=18)
    out.pack(padx=24, fill="both", expand=True)

    def show(data):
        out.config(state="normal")
        out.delete("1.0", tk.END)
        if not data:
            out.insert("1.0", "  No records found.")
        else:
            for r in data:
                out.insert(tk.END,
                    f"  {r.get('name','?'):<20} USN: {r.get('usn','?'):<14}"
                    f" Dept: {r.get('dept','?'):<12} Marks: {r.get('marks','?')}\n")
        out.config(state="disabled")

    def search():
        q = search_var.get().strip().lower()
        result = [r for r in records
                  if q in r.get("name","").lower() or q in r.get("usn","").lower()]
        show(result)

    def sort_name():  show(sorted(records, key=lambda r: r.get("name","").lower()))
    def sort_marks():
        try:    show(sorted(records, key=lambda r: float(r.get("marks",0)), reverse=True))
        except: show(records)

    btn_row = tk.Frame(win, bg=BG)
    btn_row.pack(pady=8)
    for txt, cmd in [("Search", search), ("Sort by Name", sort_name), ("Sort by Marks ↓", sort_marks)]:
        tk.Button(btn_row, text=txt, command=cmd,
                  font=(FONT_MONO, 10, "bold"),
                  bg=ACCENT, fg=BG, relief="flat", padx=14, pady=6,
                  cursor="hand2").pack(side="left", padx=6)

    show(records)