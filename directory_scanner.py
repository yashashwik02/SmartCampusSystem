"""
directory_scanner.py  —  Lab 7
"""
import tkinter as tk
from tkinter import filedialog, messagebox
import os

BG = "#0d1117"; CARD = "#161b22"; ACCENT = "#00c8ff"
TEXT = "#e6edf3"; MUTED = "#8b949e"; FONT_MONO = "Courier New"

def open_directory_scanner():
    win = tk.Toplevel()
    win.title("Lab 7 — Directory Scanner")
    win.geometry("740x540")
    win.configure(bg=BG)
    win.resizable(False, False)

    tk.Frame(win, bg=ACCENT, height=4).pack(fill="x")
    tk.Label(win, text="DIRECTORY SCANNER",
             font=(FONT_MONO, 17, "bold"), fg=ACCENT, bg=BG).pack(pady=(14,4))

    path_var = tk.StringVar(value=os.getcwd())
    bar = tk.Frame(win, bg=BG)
    bar.pack(pady=6, padx=24, fill="x")

    path_entry = tk.Entry(bar, textvariable=path_var, width=55,
                          font=(FONT_MONO, 10), bg="#1c2333", fg="white",
                          insertbackground=ACCENT, relief="flat",
                          highlightthickness=1, highlightcolor=ACCENT,
                          highlightbackground="#30363d")
    path_entry.pack(side="left", ipady=4)

    def browse():
        d = filedialog.askdirectory(parent=win)
        if d:
            path_var.set(d)

    tk.Button(bar, text="Browse", command=browse,
              font=(FONT_MONO, 10, "bold"), bg=ACCENT, fg=BG,
              relief="flat", padx=10, pady=4, cursor="hand2").pack(side="left", padx=8)

    out = tk.Text(win, font=(FONT_MONO, 9), bg=CARD, fg="#c9d1d9",
                  relief="flat", padx=12, pady=10)
    out.pack(padx=24, pady=8, fill="both", expand=True)

    stat_var = tk.StringVar()
    tk.Label(win, textvariable=stat_var, font=(FONT_MONO, 10),
             fg=ACCENT, bg=BG).pack(pady=4)

    def scan():
        out.config(state="normal")
        out.delete("1.0", tk.END)
        path = path_var.get().strip()
        if not os.path.isdir(path):
            messagebox.showerror("Invalid", "Path is not a valid directory.", parent=win)
            return

        total_files = total_dirs = total_size = 0
        try:
            for root_dir, dirs, files in os.walk(path):
                level = root_dir.replace(path, "").count(os.sep)
                indent = "  │  " * level + "  ├─ "
                rel = os.path.relpath(root_dir, path)
                out.insert(tk.END, f"{indent}📁 {rel if rel != '.' else os.path.basename(path)}/\n")
                total_dirs += len(dirs)
                sub = "  │  " * (level+1) + "  ├─ "
                for f in files:
                    fpath = os.path.join(root_dir, f)
                    try:
                        sz = os.path.getsize(fpath)
                        total_size += sz
                        out.insert(tk.END, f"{sub}📄 {f}  ({sz:,} bytes)\n")
                    except Exception:
                        out.insert(tk.END, f"{sub}📄 {f}  (? bytes)\n")
                    total_files += 1
        except PermissionError as e:
            out.insert(tk.END, f"\n  ⚠ Permission denied: {e}\n")

        out.config(state="disabled")
        stat_var.set(f"  Dirs: {total_dirs}   Files: {total_files}   Total size: {total_size:,} bytes")

    tk.Button(win, text="  Scan Directory  ", command=scan,
              font=(FONT_MONO, 11, "bold"), bg=ACCENT, fg=BG,
              relief="flat", padx=18, pady=8, cursor="hand2").pack(pady=4)