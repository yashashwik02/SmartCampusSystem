import tkinter as tk
from tkinter import messagebox
import datetime

def compute_grade(marks):
    if marks >= 90: return "O", 10
    if marks >= 80: return "A+", 9
    if marks >= 70: return "A", 8
    if marks >= 60: return "B+", 7
    if marks >= 50: return "B", 6
    if marks >= 40: return "C", 5
    return "F", 0

def open_registration():
    win = tk.Toplevel()
    win.title("Lab 1 - Student Registration")
    win.geometry("500x520")
    win.configure(bg="#2b2b2b")
    win.resizable(False, False)
    tk.Label(win, text="STUDENT REGISTRATION",
             font=("Courier New", 16, "bold"),
             fg="#00c8ff", bg="#2b2b2b").pack(pady=(20,5))
    form = tk.Frame(win, bg="#2b2b2b")
    form.pack(padx=40, fill="x")
    fields = {}
    for label, key in [("Student Name","name"),("USN","usn"),("Department","dept"),("Semester","sem"),("Marks 0-100","marks")]:
        tk.Label(form, text=label, font=("Courier New",10,"bold"),
                 fg="white", bg="#2b2b2b").pack(anchor="w", pady=(8,2))
        e = tk.Entry(form, font=("Courier New",12),
                     bg="white", fg="black",
                     insertbackground="black",
                     relief="solid", bd=2)
        e.pack(fill="x", ipady=7)
        fields[key] = e
    def generate():
        vals = {k: v.get().strip() for k,v in fields.items()}
        if not all(vals.values()):
            messagebox.showerror("Error","Fill ALL fields!",parent=win); return
        try:
            m = float(vals["marks"])
            assert 0 <= m <= 100
        except:
            messagebox.showerror("Error","Marks must be 0-100!",parent=win); return
        g, gp = compute_grade(m)
        report = f"Name: {vals['name']}\nUSN: {vals['usn']}\nDept: {vals['dept']}\nSem: {vals['sem']}\nMarks: {m}\nGrade: {g}\nStatus: {'PASS' if g!='F' else 'FAIL'}"
        messagebox.showinfo("Report", report, parent=win)
        with open(f"{vals['usn']}_report.txt","w") as f: f.write(report)
    def clear():
        for e in fields.values(): e.delete(0, tk.END)
    bf = tk.Frame(win, bg="#2b2b2b")
    bf.pack(pady=20)
    tk.Button(bf, text="Generate Report", command=generate,
              font=("Courier New",11,"bold"), bg="#00c8ff", fg="black",
              relief="flat", padx=20, pady=8).pack(side="left", padx=10)
    tk.Button(bf, text="Clear", command=clear,
              font=("Courier New",11,"bold"), bg="#555555", fg="white",
              relief="flat", padx=20, pady=8).pack(side="left", padx=10)
