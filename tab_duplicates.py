import tkinter as tk
from tkinter import ttk, messagebox
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from backend.algorithms import find_duplicates

BG    = "#F5F7FA"
CARD  = "#FFFFFF"
FG    = "#2C3E50"
ACC   = "#E67E22"
GREEN = "#27AE60"
RED   = "#E74C3C"
BLUE  = "#2980B9"
GREY  = "#95A5A6"
BORDER= "#D5D8DC"

class DuplicatesTab(ttk.Frame):
    def __init__(self, parent, data=None):
        super().__init__(parent)
        cpp = data or {}
        self._arr   = cpp.get("dup_input",  [4, 2, 7, 2, 9, 4, 1, 7, 3])
        self._steps = cpp.get("dup_steps",  [])
        self._cpp_dups = cpp.get("dup_result", [])
        self._step_idx = 0
        self._seen  = set()
        self._dups  = set()
        self._build()

    def _build(self):
        tk.Label(self, text="🔍  Duplicate Detection  (Hash Set)",
                 bg=BG, fg=FG, font=("Segoe UI", 15, "bold")).pack(anchor="w", padx=20, pady=(16,6))

        inp = tk.Frame(self, bg=BG)
        inp.pack(fill="x", padx=20, pady=4)
        tk.Label(inp, text="Array:", bg=BG, fg=FG,
                 font=("Segoe UI", 11)).pack(side="left")
        self.arr_var = tk.StringVar(value="4 2 7 2 9 4 1 7 3")
        tk.Entry(inp, textvariable=self.arr_var, width=28,
                 bg=CARD, fg=FG, insertbackground=FG,
                 font=("Consolas", 12), relief="solid", bd=1).pack(side="left", padx=10)
        for txt, cmd, color in [
            ("▶ Start",     self._start,    ACC),
            ("⏭ Next",      self._next,     BLUE),
            ("⚡ Auto Run", self._auto,     GREEN),
        ]:
            tk.Button(inp, text=txt, command=cmd,
                      bg=color, fg="white", font=("Segoe UI", 10, "bold"),
                      relief="flat", padx=10, pady=5, cursor="hand2").pack(side="left", padx=4)

        # array boxes
        tk.Label(self, text="Array", bg=BG, fg=FG,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=20, pady=(10,2))
        self.arr_canvas = tk.Canvas(self, bg=CARD, height=90,
                                    highlightthickness=1, highlightbackground=BORDER)
        self.arr_canvas.pack(fill="x", padx=20, pady=2)

        # hash set
        tk.Label(self, text="Hash Set  (seen elements)",
                 bg=BG, fg=FG, font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=20, pady=(8,2))
        self.set_canvas = tk.Canvas(self, bg=CARD, height=70,
                                    highlightthickness=1, highlightbackground=BORDER)
        self.set_canvas.pack(fill="x", padx=20, pady=2)

        self.result_lbl = tk.Label(self, text="Duplicates found: —",
                                   bg=BG, fg=RED, font=("Segoe UI", 12, "bold"))
        self.result_lbl.pack(anchor="w", padx=20, pady=6)

        frame = tk.Frame(self, bg=BG)
        frame.pack(fill="both", expand=True, padx=20, pady=(0,14))
        self.log = tk.Text(frame, bg=CARD, fg=FG, font=("Consolas", 10),
                           relief="solid", bd=1, state="disabled", height=7)
        sb = ttk.Scrollbar(frame, command=self.log.yview)
        self.log.configure(yscrollcommand=sb.set)
        self.log.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        self._start()

    def _start(self):
        try:
            self._arr = list(map(int, self.arr_var.get().split()))
        except ValueError:
            messagebox.showwarning("Input", "Enter integers separated by spaces.")
            return
        _, self._steps = find_duplicates(self._arr)
        self._seen = set(); self._dups = set()
        self._step_idx = 0
        self._clear_log()
        self._draw_array(-1); self._draw_set()
        self.result_lbl.config(text="Duplicates found: —")

    def _next(self):
        if self._step_idx >= len(self._steps):
            self._log_write("  ✓ Done.\n", GREEN); return
        kind, val = self._steps[self._step_idx]
        if kind == "CHECK":
            self._seen.add(val)
            self._log_write(f"  CHECK  {val}  → added to set\n", BLUE)
        else:
            self._dups.add(val)
            self._log_write(f"  FOUND  {val}  → DUPLICATE 🔴\n", RED)
        self._draw_array(self._step_idx)
        self._draw_set()
        self.result_lbl.config(
            text=f"Duplicates found: {sorted(self._dups) if self._dups else '—'}")
        self._step_idx += 1

    def _auto(self):
        self._start()
        def loop(i=0):
            if i < len(self._steps):
                self._next()
                self.after(480, lambda: loop(i+1))
        loop()

    def _draw_array(self, highlight):
        c = self.arr_canvas; c.delete("all")
        if not self._arr: return
        w = c.winfo_width() or 700
        box = min(58, (w - 30) // len(self._arr))
        x = 14
        for i, val in enumerate(self._arr):
            fill = (ACC if i == highlight else
                    RED if val in self._dups else
                    GREEN if val in self._seen else "#ECF0F1")
            c.create_rectangle(x, 12, x+box, 78,
                               fill=fill, outline=BORDER, width=1)
            c.create_text(x+box//2, 45, text=str(val),
                          fill="white" if fill != "#ECF0F1" else FG,
                          font=("Segoe UI", 12, "bold"))
            x += box + 3

    def _draw_set(self):
        c = self.set_canvas; c.delete("all")
        x = 14
        for val in sorted(self._seen):
            color = RED if val in self._dups else GREEN
            c.create_oval(x, 8, x+48, 56, fill=color, outline="white", width=1)
            c.create_text(x+24, 32, text=str(val),
                          fill="white", font=("Segoe UI", 11, "bold"))
            x += 56

    def _clear_log(self):
        self.log.config(state="normal"); self.log.delete("1.0","end")
        self.log.config(state="disabled")

    def _log_write(self, text, color=FG):
        self.log.config(state="normal")
        tag = f"t{color.replace('#','')}"
        self.log.tag_config(tag, foreground=color)
        self.log.insert("end", text, tag)
        self.log.see("end")
        self.log.config(state="disabled")
