import tkinter as tk
from tkinter import messagebox
import datetime

BG        = "#0d1117"
CARD      = "#161b22"
ACCENT    = "#00c8ff"
TEXT      = "#e6edf3"
MUTED     = "#8b949e"
FONT_MONO = "Courier New"

COURSES = [
    "CS101 - Python Programming",
    "CS102 - Data Structures",
    "CS103 - Computer Networks",
    "CS104 - Database Systems",
    "CS105 - Operating Systems",
    "CS106 - Machine Learning",
    "CS107 - Cybersecurity Basics",
    "CS108 - IoT Fundamentals",
]

def _entry(parent, width=40):
    return tk.Entry(
        parent, width=width,
        font=(FONT_MONO, 11),
        bg="#1c2333", fg="#ffffff",
        insertbackground=ACCENT,
        relief="flat",
        highlightthickness=1,
        highlightcolor=ACCENT,
        highlightbackground="#30363d"
    )

def _button(parent, text, cmd, accent=True):
    bg = ACCENT if accent else "#21262d"
    fg = BG    if accent else TEXT
    b = tk.Button(parent, text=text, command=cmd,
                  font=(FONT_MONO, 11, "bold"),
                  bg=bg, fg=fg,
                  activebackground="#007ea7", activeforeground="white",
                  relief="flat", padx=18, pady=8, cursor="hand2")
    b.bind("<Enter>", lambda e: b.config(bg="#007ea7", fg="white"))
    b.bind("<Leave>", lambda e: b.config(bg=bg, fg=fg))
    return b

def open_course_enrollment():
    win = tk.Toplevel()
    win.title("Lab 2 — Course Enrollment")
    win.geometry("680x640")
    win.configure(bg=BG)
    win.resizable(False, False)

    tk.Frame(win, bg=ACCENT, height=4).pack(fill="x")
    tk.Label(win, text="COURSE ENROLLMENT",
             font=(FONT_MONO, 18, "bold"), fg=ACCENT, bg=BG).pack(pady=(18, 2))
    tk.Label(win, text="Select courses and enroll student",
             font=(FONT_MONO, 10), fg=MUTED, bg=BG).pack(pady=(0, 14))

    card = tk.Frame(win, bg=CARD, padx=30, pady=20)
    card.pack(padx=30, fill="x")

    # Student details
    fields = {}
    for label, key in [("Student Name", "name"), ("USN / Roll No", "usn")]:
        tk.Label(card, text=f"{label}:", font=(FONT_MONO, 10),
                 fg=TEXT, bg=CARD).pack(anchor="w", pady=(6,0))
        e = _entry(card)
        e.pack(anchor="w", pady=(2,0), ipady=4)
        fields[key] = e

    # Course checkboxes
    tk.Label(card, text="Select Courses:", font=(FONT_MONO, 10, "bold"),
             fg=ACCENT, bg=CARD).pack(anchor="w", pady=(16, 4))

    selected = []
    for course in COURSES:
        var = tk.BooleanVar()
        cb = tk.Checkbutton(
            card, text=course, variable=var,
            font=(FONT_MONO, 10),
            fg=TEXT, bg=CARD,
            selectcolor="#1c2333",
            activebackground=CARD,
            activeforeground=ACCENT
        )
        cb.pack(anchor="w", pady=1)
        selected.append((course, var))

    btn_row = tk.Frame(win, bg=BG)
    btn_row.pack(pady=16)

    def enroll():
        name = fields["name"].get().strip()
        usn  = fields["usn"].get().strip()
        chosen = [c for c, v in selected if v.get()]

        if not name or not usn:
            messagebox.showerror("Missing", "Enter Name and USN.", parent=win)
            return
        if not chosen:
            messagebox.showerror("No Course", "Select at least one course.", parent=win)
            return

        now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        lines = "\n".join(f"  • {c}" for c in chosen)
        report = (
            f"COURSE ENROLLMENT CONFIRMATION\n"
            f"{'='*46}\n"
            f"  Date   : {now}\n"
            f"  Name   : {name}\n"
            f"  USN    : {usn}\n"
            f"{'='*46}\n"
            f"  Enrolled Courses ({len(chosen)}):\n{lines}\n"
            f"{'='*46}"
        )
        popup = tk.Toplevel(win)
        popup.title("Enrollment Confirmation")
        popup.geometry("500x380")
        popup.configure(bg=BG)
        tk.Label(popup, text="ENROLLMENT REPORT", font=(FONT_MONO, 13, "bold"),
                 fg=ACCENT, bg=BG).pack(pady=(12,6))
        txt = tk.Text(popup, font=(FONT_MONO, 10), bg=CARD, fg="#c9d1d9",
                      relief="flat", padx=10, pady=10)
        txt.insert("1.0", report)
        txt.config(state="disabled")
        txt.pack(padx=20, fill="both", expand=True)
        _button(popup, "Close", popup.destroy, accent=False).pack(pady=10)

        fname = f"{usn}_enrollment.txt"
        with open(fname, "w") as f:
            f.write(report)
        messagebox.showinfo("Saved", f"Saved to {fname}", parent=win)

    _button(btn_row, "  Enroll  ", enroll).pack(side="left", padx=10)
    _button(btn_row, "  Close  ", win.destroy, accent=False).pack(side="left", padx=10)