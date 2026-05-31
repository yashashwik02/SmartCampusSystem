import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk
import os

from student_registration import open_registration
from course_enrollment import open_course_enrollment
from student_records import open_student_records
from search_sort import open_search_sort
from fee_calculation import open_fee_calculation
from file_manager import open_file_manager
from directory_scanner import open_directory_scanner
from performance_analytics import open_performance_analytics

# ─────────────────────────────────────────
#  MAIN WINDOW
# ─────────────────────────────────────────
root = tk.Tk()
root.title("Smart Campus Information System")
root.geometry("1000x750")
root.resizable(False, False)
root.configure(bg="#2b2b2b")

# ─────────────────────────────────────────
#  BACKGROUND IMAGE (optional – skip if missing)
# ─────────────────────────────────────────
if os.path.exists("background.jpg"):
    bg_image = Image.open("background.jpg").resize((1000, 750))
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    # dark overlay so text stays readable
    overlay = tk.Frame(root, bg="#2b2b2b")
    overlay.place(x=0, y=0, relwidth=1, relheight=1)
    overlay.configure(bg="#2b2b2b")   # semi-transparent via alpha trick below

# ─────────────────────────────────────────
#  CANVAS + GRADIENT OVERLAY
# ─────────────────────────────────────────
canvas = tk.Canvas(root, width=1000, height=750, highlightthickness=0)
canvas.place(x=0, y=0)

# Draw subtle gradient strips for depth
for i in range(750):
    ratio = i / 750
    r = int(10 + ratio * 5)
    g = int(15 + ratio * 8)
    b = int(30 + ratio * 20)
    color = f"#{r:02x}{g:02x}{b:02x}"
    canvas.create_line(0, i, 1000, i, fill=color)

# Decorative accent lines
canvas.create_line(0, 0, 1000, 0, fill="#00c8ff", width=3)
canvas.create_line(0, 749, 1000, 749, fill="#00c8ff", width=3)
canvas.create_line(0, 0, 0, 750, fill="#00c8ff", width=3)
canvas.create_line(999, 0, 999, 750, fill="#00c8ff", width=3)

# Glow circle background effect
canvas.create_oval(300, 50, 700, 300, outline="#00c8ff", width=60)
canvas.create_oval(350, 80, 650, 270, outline="#00c8ff", width=30)

# ─────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────
header_frame = tk.Frame(root, bg="#000000")
header_frame.place(relx=0.5, y=30, anchor="n")

tk.Label(
    header_frame,
    text="◈  SMART CAMPUS  ◈",
    font=("Courier New", 13, "bold"),
    fg="#00c8ff",
    bg="#2b2b2b",
    
).pack()

tk.Label(
    header_frame,
    text="INFORMATION SYSTEM",
    font=("Courier New", 30, "bold"),
    fg="#ffffff",
    bg="#2b2b2b"
).pack()

tk.Label(
    header_frame,
    text="Department of CSE  ·  DSCE",
    font=("Courier New", 10),
    fg="#6699aa",
    bg="#2b2b2b"
).pack(pady=(2, 0))

# Divider line
divider = tk.Frame(root, height=2, bg="#00c8ff", width=500)
divider.place(relx=0.5, y=145, anchor="center")

# ─────────────────────────────────────────
#  SCROLLABLE BUTTON AREA
# ─────────────────────────────────────────
container = tk.Frame(root, bg="#2b2b2b")
container.place(relx=0.5, y=170, anchor="n", width=600, height=550)

# Lab data: (label, command)
labs = [
    ("Lab 1  —  Student Registration",    open_registration),
    ("Lab 2  —  Course Enrollment",        open_course_enrollment),
    ("Lab 3  —  Student Records",          open_student_records),
    ("Lab 4  —  Search & Sort",            open_search_sort),
    ("Lab 5  —  Fee Calculation",          open_fee_calculation),
    ("Lab 6  —  File Manager",             open_file_manager),
    ("Lab 7  —  Directory Scanner",        open_directory_scanner),
    ("Lab 8  —  Performance Analytics",    open_performance_analytics),
]

def on_enter(e, btn):
    btn.config(bg="#00c8ff", fg="#0a0f1e")

def on_leave(e, btn):
    btn.config(bg="#111827", fg="#00c8ff")

for label, cmd in labs:
    btn = tk.Button(
        container,
        text=label,
        width=48,
        font=("Courier New", 12, "bold"),
        bg="#111827",
        fg="#00c8ff",
        activebackground="#00c8ff",
        activeforeground="#0a0f1e",
        relief="flat",
        bd=0,
        pady=12,
        cursor="hand2",
        command=cmd
    )
    btn.pack(pady=6, fill="x")
    btn.bind("<Enter>", lambda e, b=btn: on_enter(e, b))
    btn.bind("<Leave>", lambda e, b=btn: on_leave(e, b))

# Footer
tk.Label(
    root,
    text="Mini Project Integration  ·  Labs 1–10",
    font=("Courier New", 9),
    fg="#334455",
    bg="#2b2b2b"
).place(relx=0.5, rely=1.0, anchor="s", y=-8)

# ─────────────────────────────────────────
root.mainloop()