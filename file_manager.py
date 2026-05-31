"""
file_manager.py  —  Lab 6
"""
import tkinter as tk
from tkinter import messagebox, filedialog
import os, shutil, datetime

BG = "#0d1117"; CARD = "#161b22"; ACCENT = "#00c8ff"
TEXT = "#e6edf3"; MUTED = "#8b949e"; FONT_MONO = "Courier New"

def open_file_manager():
    cwd = [os.getcwd()]

    win = tk.Toplevel()
    win.title("Lab 6 — File Manager")
    win.geometry("760x540")
    win.configure(bg=BG)
    win.resizable(False, False)

    tk.Frame(win, bg=ACCENT, height=4).pack(fill="x")
    tk.Label(win, text="FILE MANAGER",
             font=(FONT_MONO, 17, "bold"), fg=ACCENT, bg=BG).pack(pady=(12,2))

    path_var = tk.StringVar(value=cwd[0])
    tk.Label(win, textvariable=path_var, font=(FONT_MONO, 9),
             fg=MUTED, bg=BG).pack()

    # File listbox
    list_frame = tk.Frame(win, bg=CARD)
    list_frame.pack(padx=24, pady=10, fill="both", expand=True)

    listbox = tk.Listbox(list_frame, font=(FONT_MONO, 10),
                         bg=CARD, fg=TEXT, selectbackground=ACCENT,
                         selectforeground=BG, relief="flat",
                         highlightthickness=0, activestyle="none")
    sb = tk.Scrollbar(list_frame, orient="vertical", command=listbox.yview)
    listbox.configure(yscrollcommand=sb.set)
    listbox.pack(side="left", fill="both", expand=True)
    sb.pack(side="right", fill="y")

    def refresh():
        listbox.delete(0, tk.END)
        path_var.set(cwd[0])
        try:
            items = sorted(os.listdir(cwd[0]))
            for item in items:
                full = os.path.join(cwd[0], item)
                prefix = "📁 " if os.path.isdir(full) else "📄 "
                listbox.insert(tk.END, prefix + item)
        except PermissionError:
            listbox.insert(tk.END, "  ⚠ Permission denied")

    def open_selected(event=None):
        sel = listbox.curselection()
        if not sel: return
        name = listbox.get(sel[0]).replace("📁 ", "").replace("📄 ", "")
        full = os.path.join(cwd[0], name)
        if os.path.isdir(full):
            cwd[0] = full
            refresh()
        else:
            try:
                with open(full) as f:
                    content = f.read(4000)
                popup = tk.Toplevel(win)
                popup.title(name)
                popup.geometry("600x400")
                popup.configure(bg=BG)
                txt = tk.Text(popup, font=(FONT_MONO, 10), bg=CARD, fg=TEXT, relief="flat")
                txt.insert("1.0", content)
                txt.config(state="disabled")
                txt.pack(fill="both", expand=True, padx=10, pady=10)
            except Exception as ex:
                messagebox.showerror("Error", str(ex), parent=win)

    def go_up():
        parent = os.path.dirname(cwd[0])
        if parent != cwd[0]:
            cwd[0] = parent
            refresh()

    def create_file_here():
        fname = tk.simpledialog.askstring("New File", "File name:", parent=win)
        if fname:
            path = os.path.join(cwd[0], fname)
            open(path, "w").close()
            refresh()

    def delete_selected():
        sel = listbox.curselection()
        if not sel: return
        name = listbox.get(sel[0]).replace("📁 ", "").replace("📄 ", "")
        full = os.path.join(cwd[0], name)
        if messagebox.askyesno("Delete", f"Delete {name}?", parent=win):
            try:
                if os.path.isdir(full): shutil.rmtree(full)
                else: os.remove(full)
                refresh()
            except Exception as ex:
                messagebox.showerror("Error", str(ex), parent=win)

    listbox.bind("<Double-Button-1>", open_selected)

    btn_row = tk.Frame(win, bg=BG)
    btn_row.pack(pady=8)
    for txt, cmd in [("⬆ Up", go_up), ("Open", open_selected), ("Delete", delete_selected), ("Refresh", refresh)]:
        tk.Button(btn_row, text=txt, command=cmd,
                  font=(FONT_MONO, 10, "bold"),
                  bg=ACCENT, fg=BG, relief="flat", padx=14, pady=6,
                  cursor="hand2").pack(side="left", padx=5)

    refresh()

    # Need simpledialog for create
    from tkinter import simpledialog