"""
Edu Revolution — Attendance Percentage Calculator
A beginner-friendly desktop GUI built with Python's standard Tkinter library.
Run: python attendance_calculator.py
"""

import tkinter as tk
import math
from tkinter import ttk, messagebox

APP_NAME = "Edu Revolution | Attendance Calculator"
BG = "#0b1220"
PANEL = "#111c2e"
PANEL_ALT = "#17243a"
TEXT = "#edf3ff"
MUTED = "#9aabc4"
ACCENT = "#55d6be"
BLUE = "#7aa7ff"
RED = "#ff7b89"
YELLOW = "#ffd166"


class AttendanceCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("760x690")
        self.root.minsize(650, 620)
        self.root.configure(bg=BG)

        self.total_var = tk.StringVar()
        self.attended_var = tk.StringVar()
        self.target_var = tk.StringVar(value="75")
        self.subject_var = tk.StringVar(value="My Subject")

        self._configure_styles()
        self._build_ui()
        self.root.bind("<Return>", lambda _event: self.calculate())

    def _configure_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure(
            "Attendance.Horizontal.TProgressbar",
            troughcolor=PANEL_ALT,
            background=ACCENT,
            bordercolor=PANEL_ALT,
            lightcolor=ACCENT,
            darkcolor=ACCENT,
            thickness=12,
        )

    def _label(self, parent, text, **kwargs):
        return tk.Label(parent, text=text, bg=kwargs.pop("bg", PANEL),
                        fg=kwargs.pop("fg", TEXT), font=kwargs.pop("font", ("Segoe UI", 10)),
                        **kwargs)

    def _entry(self, parent, variable, width=18):
        return tk.Entry(
            parent, textvariable=variable, width=width,
            bg="#0b1424", fg=TEXT, insertbackground=TEXT,
            relief="flat", highlightthickness=1,
            highlightbackground="#2a3a55", highlightcolor=ACCENT,
            font=("Segoe UI", 11)
        )

    def _build_ui(self):
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=28, pady=(24, 12))
        self._label(header, "EDU REVOLUTION", bg=BG, fg=ACCENT,
                    font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self._label(header, "Attendance Calculator", bg=BG,
                    font=("Segoe UI", 25, "bold")).pack(anchor="w", pady=(3, 2))
        self._label(header, "Know your percentage. Plan your next classes.", bg=BG,
                    fg=MUTED, font=("Segoe UI", 11)).pack(anchor="w")

        form = tk.Frame(self.root, bg=PANEL, highlightbackground="#263650",
                        highlightthickness=1)
        form.pack(fill="x", padx=28, pady=10)
        form.grid_columnconfigure(0, weight=1)
        form.grid_columnconfigure(1, weight=1)

        self._label(form, "SUBJECT / COURSE NAME", fg=MUTED,
                    font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", padx=20, pady=(18, 6))
        self._label(form, "TARGET ATTENDANCE (%)", fg=MUTED,
                    font=("Segoe UI", 9, "bold")).grid(row=0, column=1, sticky="w", padx=20, pady=(18, 6))

        self._entry(form, self.subject_var, 24).grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 16), ipady=8)
        self._entry(form, self.target_var, 12).grid(row=1, column=1, sticky="ew", padx=20, pady=(0, 16), ipady=8)

        self._label(form, "TOTAL CLASSES HELD", fg=MUTED,
                    font=("Segoe UI", 9, "bold")).grid(row=2, column=0, sticky="w", padx=20, pady=(0, 6))
        self._label(form, "CLASSES ATTENDED", fg=MUTED,
                    font=("Segoe UI", 9, "bold")).grid(row=2, column=1, sticky="w", padx=20, pady=(0, 6))
        self._entry(form, self.total_var).grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 20), ipady=8)
        self._entry(form, self.attended_var).grid(row=3, column=1, sticky="ew", padx=20, pady=(0, 20), ipady=8)

        actions = tk.Frame(self.root, bg=BG)
        actions.pack(fill="x", padx=28, pady=(4, 12))
        tk.Button(actions, text="Calculate Attendance", command=self.calculate,
                  bg=ACCENT, fg="#06221d", activebackground="#7be6d2",
                  activeforeground="#06221d", relief="flat", cursor="hand2",
                  font=("Segoe UI", 11, "bold"), padx=18, pady=11).pack(side="left")
        tk.Button(actions, text="Reset", command=self.reset,
                  bg=PANEL_ALT, fg=TEXT, activebackground="#263650",
                  relief="flat", cursor="hand2", font=("Segoe UI", 10),
                  padx=18, pady=11).pack(side="left", padx=10)

        results = tk.Frame(self.root, bg=PANEL, highlightbackground="#263650",
                           highlightthickness=1)
        results.pack(fill="both", expand=True, padx=28, pady=(0, 18))
        self._label(results, "YOUR ATTENDANCE OVERVIEW", fg=MUTED,
                    font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=20, pady=(18, 10))

        self.percent_label = self._label(results, "--%", font=("Segoe UI", 34, "bold"), fg=ACCENT)
        self.percent_label.pack(anchor="w", padx=20)
        self.status_label = self._label(results, "Enter your class details and calculate.", fg=MUTED,
                                        font=("Segoe UI", 10))
        self.status_label.pack(anchor="w", padx=20, pady=(0, 12))

        self.progress = ttk.Progressbar(results, style="Attendance.Horizontal.TProgressbar",
                                        maximum=100, mode="determinate")
        self.progress.pack(fill="x", padx=20, pady=(0, 16))

        grid = tk.Frame(results, bg=PANEL)
        grid.pack(fill="x", padx=12, pady=(0, 8))
        for col in range(2):
            grid.grid_columnconfigure(col, weight=1)

        self.needed_value = self._result_card(grid, 0, 0, "CLASSES NEEDED", "—")
        self.miss_value = self._result_card(grid, 0, 1, "CLASSES YOU CAN MISS", "—")
        self.attended_value = self._result_card(grid, 1, 0, "CLASSES ATTENDED", "—")
        self.held_value = self._result_card(grid, 1, 1, "TOTAL CLASSES HELD", "—")

        self._label(results, "Tip: This calculator assumes every future class has equal weight.",
                    fg=MUTED, font=("Segoe UI", 9), wraplength=620,
                    justify="left").pack(anchor="w", padx=20, pady=(10, 16))

        footer = self._label(self.root, "Made for students • Edu Revolution", bg=BG,
                             fg="#647793", font=("Segoe UI", 9))
        footer.pack(pady=(0, 12))

    def _result_card(self, parent, row, col, title, value):
        card = tk.Frame(parent, bg=PANEL_ALT)
        card.grid(row=row, column=col, sticky="nsew", padx=8, pady=6)
        self._label(card, title, bg=PANEL_ALT, fg=MUTED,
                    font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=12, pady=(10, 4))
        value_label = self._label(card, value, bg=PANEL_ALT,
                                  font=("Segoe UI", 16, "bold"))
        value_label.pack(anchor="w", padx=12, pady=(0, 10))
        return value_label

    def calculate(self):
        try:
            total_text = self.total_var.get().strip()
            attended_text = self.attended_var.get().strip()
            target_text = self.target_var.get().strip()

            if not total_text or not attended_text or not target_text:
                raise ValueError("Please fill in total classes, attended classes, and target percentage.")

            total = int(total_text)
            attended = int(attended_text)
            target = float(target_text)

            if total <= 0:
                raise ValueError("Total classes held must be greater than zero.")
            if attended < 0 or attended > total:
                raise ValueError("Classes attended must be between 0 and total classes held.")
            if not 0 < target <= 100:
                raise ValueError("Target attendance must be greater than 0 and at most 100.")

        except ValueError as exc:
            messagebox.showerror("Check your input", str(exc))
            return

        percentage = attended / total * 100
        self.percent_label.config(text=f"{percentage:.2f}%")
        self.progress["value"] = min(percentage, 100)
        self.attended_value.config(text=str(attended))
        self.held_value.config(text=str(total))

        if percentage >= target:
            # Maximum future classes that can be missed while staying at/above target.
            can_miss = int((attended / (target / 100)) - total)
            can_miss = max(0, can_miss)
            self.needed_value.config(text="0")
            self.miss_value.config(text=str(can_miss))
            self.status_label.config(
                text=f"You're meeting your {target:g}% target. Keep it up!",
                fg=ACCENT
            )
        else:
            # Smallest n satisfying attended / (total + n) >= target.
            needed = max(0, int((attended / (target / 100) - total) * -1))
            # More robust integer formula for the smallest number of consecutive classes needed.
            if target < 100:
                numerator = target * total - 100 * attended
                denominator = 100 - target
                needed = max(0, math.ceil(numerator / denominator))
            else:
                needed = max(0, total - attended)
            while (attended + needed) / (total + needed) * 100 < target:
                needed += 1
            self.needed_value.config(text=str(needed))
            self.miss_value.config(text="0")
            self.status_label.config(
                text=f"You're below your {target:g}% target. Attend the next {needed} classes consecutively to reach it.",
                fg=YELLOW
            )

        subject = self.subject_var.get().strip() or "Your subject"
        self.root.title(f"{subject} — {APP_NAME}")

    def reset(self):
        self.total_var.set("")
        self.attended_var.set("")
        self.target_var.set("75")
        self.subject_var.set("My Subject")
        self.percent_label.config(text="--%", fg=ACCENT)
        self.status_label.config(text="Enter your class details and calculate.", fg=MUTED)
        self.progress["value"] = 0
        self.needed_value.config(text="—")
        self.miss_value.config(text="—")
        self.attended_value.config(text="—")
        self.held_value.config(text="—")
        self.root.title(APP_NAME)


def main():
    root = tk.Tk()
    AttendanceCalculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
