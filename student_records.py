import tkinter as tk
from tkinter import ttk, messagebox
import json, os

BG        = "#0d1117"
CARD      = "#161b22"
ACCENT    = "#00c8ff"
TEXT      = "#e6edf3"
MUTED     = "#8b949e"
FONT_MONO = "Courier New"
DB_FILE   = "student_records_db.json"

def _load():
    if os.path.exists(DB_FILE):
        with open(DB_FILE) as f:
            return json.load(f)
    return []

def _save(records):
    with open(DB_FILE, "w") as f:
        json.dump(records, f, indent=2)

def _entry(parent, width=28):
    return tk.Entry(
        parent, width=width,
        font=(FONT_MONO, 10),
        bg="#1c2333", fg="#ffffff",
        insertbackground=ACCENT,
        relief="flat",
        highlightthickness=1,
        highlightcolor=ACCENT,
        highlightbackground="#30363d"
    )

def open_student_records():
    records = _load()

    win = tk.Toplevel()
    win.title("Lab 3 — Student Records")
    win.geometry("900x620")
    win.configure(bg=BG)
    win.resizable(False, False)

    tk.Frame(win, bg=ACCENT, height=4).pack(fill="x")
    tk.Label(win, text="STUDENT RECORDS",
             font=(FONT_MONO, 18, "bold"), fg=ACCENT, bg=BG).pack(pady=(14, 2))
    tk.Label(win, text="Add, view and manage student records",
             font=(FONT_MONO, 10), fg=MUTED, bg=BG).pack()

    # ── input card ────────────────────────────────────────────────────────────
    card = tk.Frame(win, bg=CARD, padx=24, pady=16)
    card.pack(padx=24, pady=12, fill="x")

    fields = {}
    grid_data = [
        ("Name",       "name",   0, 0),
        ("USN",        "usn",    0, 2),
        ("Department", "dept",   1, 0),
        ("Semester",   "sem",    1, 2),
        ("Marks",      "marks",  2, 0),
        ("GPA",        "gpa",    2, 2),
    ]
    for label, key, row, col in grid_data:
        tk.Label(card, text=label+":", font=(FONT_MONO, 10),
                 fg=MUTED, bg=CARD).grid(row=row, column=col, sticky="w", padx=(0,4), pady=4)
        e = _entry(card)
        e.grid(row=row, column=col+1, sticky="w", padx=(0,16), pady=4, ipady=3)
        fields[key] = e

    def add_record():
        vals = {k: v.get().strip() for k, v in fields.items()}
        if not vals["name"] or not vals["usn"]:
            messagebox.showerror("Missing", "Name and USN are required.", parent=win)
            return
        records.append(vals)
        _save(records)
        refresh_table()
        for e in fields.values():
            e.delete(0, tk.END)
        messagebox.showinfo("Added", f"Record for {vals['name']} added.", parent=win)

    def delete_selected():
        sel = table.selection()
        if not sel:
            messagebox.showwarning("None selected", "Select a row to delete.", parent=win)
            return
        idx = table.index(sel[0])
        records.pop(idx)
        _save(records)
        refresh_table()

    btn_row = tk.Frame(card, bg=CARD)
    btn_row.grid(row=3, column=0, columnspan=4, pady=10)

    for txt, cmd, acc in [
        ("  Add Record  ", add_record, True),
        ("  Delete Selected  ", delete_selected, False)
    ]:
        bg = ACCENT if acc else "#21262d"
        fg = BG    if acc else TEXT
        b = tk.Button(btn_row, text=txt, command=cmd,
                      font=(FONT_MONO, 10, "bold"),
                      bg=bg, fg=fg, relief="flat", padx=14, pady=6, cursor="hand2")
        b.pack(side="left", padx=6)

    # ── table ─────────────────────────────────────────────────────────────────
    cols = ("Name", "USN", "Dept", "Sem", "Marks", "GPA")
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Custom.Treeview",
                    background=CARD, foreground=TEXT,
                    fieldbackground=CARD, rowheight=28,
                    font=(FONT_MONO, 10))
    style.configure("Custom.Treeview.Heading",
                    background="#21262d", foreground=ACCENT,
                    font=(FONT_MONO, 10, "bold"))

    tbl_frame = tk.Frame(win, bg=BG)
    tbl_frame.pack(padx=24, fill="both", expand=True)

    table = ttk.Treeview(tbl_frame, columns=cols, show="headings",
                         style="Custom.Treeview", height=10)
    for col in cols:
        table.heading(col, text=col)
        table.column(col, width=140, anchor="center")
    table.pack(side="left", fill="both", expand=True)

    sb = ttk.Scrollbar(tbl_frame, orient="vertical", command=table.yview)
    table.configure(yscrollcommand=sb.set)
    sb.pack(side="right", fill="y")

    def refresh_table():
        for row in table.get_children():
            table.delete(row)
        for r in records:
            table.insert("", "end", values=(
                r.get("name",""), r.get("usn",""), r.get("dept",""),
                r.get("sem",""), r.get("marks",""), r.get("gpa","")
            ))

    refresh_table()