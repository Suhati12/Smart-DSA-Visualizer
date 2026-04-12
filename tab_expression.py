import tkinter as tk
from tkinter import ttk, messagebox
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from backend.algorithms import infix_to_postfix, infix_to_prefix

BG    = "#F5F7FA"
CARD  = "#FFFFFF"
FG    = "#2C3E50"
ACC   = "#E67E22"
GREEN = "#27AE60"
RED   = "#E74C3C"
BLUE  = "#2980B9"
GREY  = "#BDC3C7"
BORDER= "#D5D8DC"

class ExpressionTab(ttk.Frame):
    def __init__(self, parent, data=None):
        super().__init__(parent)
        self._cpp_data = data or {}
        self._build()
        # pre-load results from C++ engine
        pf = self._cpp_data.get("postfix_result", "")
        pr = self._cpp_data.get("prefix_result", "")
        if pf: self.postfix_card._value_label.config(text=pf)
        if pr: self.prefix_card._value_label.config(text=pr)
        steps = self._cpp_data.get("postfix_steps", [])
        if steps: self._draw_steps(steps)

    def _build(self):
        tk.Label(self, text="📐  Infix → Postfix / Prefix",
                 bg=BG, fg=FG, font=("Segoe UI", 15, "bold")).pack(anchor="w", padx=20, pady=(16,6))

        # input row
        inp = tk.Frame(self, bg=BG)
        inp.pack(fill="x", padx=20, pady=4)
        tk.Label(inp, text="Expression:", bg=BG, fg=FG,
                 font=("Segoe UI", 11)).pack(side="left")
        self.expr_var = tk.StringVar(value="A+B*(C-D)/E")
        tk.Entry(inp, textvariable=self.expr_var, width=28,
                 bg=CARD, fg=FG, insertbackground=FG,
                 font=("Consolas", 12), relief="solid", bd=1).pack(side="left", padx=10)
        tk.Button(inp, text="▶  Convert", command=self._run,
                  bg=ACC, fg="white", font=("Segoe UI", 10, "bold"),
                  relief="flat", padx=14, pady=5, cursor="hand2",
                  activebackground="#D35400").pack(side="left")

        # result cards
        res = tk.Frame(self, bg=BG)
        res.pack(fill="x", padx=20, pady=8)
        self.postfix_card = self._result_card(res, "Postfix", "—", GREEN)
        self.postfix_card.pack(side="left", padx=(0,12))
        self.prefix_card  = self._result_card(res, "Prefix",  "—", BLUE)
        self.prefix_card.pack(side="left")

        # stack visualizer
        tk.Label(self, text="Step-by-Step Stack Trace",
                 bg=BG, fg=FG, font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=20, pady=(8,2))
        self.canvas = tk.Canvas(self, bg=CARD, height=130,
                                highlightthickness=1, highlightbackground=BORDER)
        self.canvas.pack(fill="x", padx=20, pady=2)

        # log
        tk.Label(self, text="Operation Log",
                 bg=BG, fg=FG, font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=20, pady=(8,2))
        frame = tk.Frame(self, bg=BG)
        frame.pack(fill="both", expand=True, padx=20, pady=(0,14))
        self.log = tk.Text(frame, bg=CARD, fg=FG, font=("Consolas", 10),
                           relief="solid", bd=1, state="disabled", height=9)
        sb = ttk.Scrollbar(frame, command=self.log.yview)
        self.log.configure(yscrollcommand=sb.set)
        self.log.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

    def _result_card(self, parent, label, value, color):
        f = tk.Frame(parent, bg=CARD, relief="solid", bd=1)
        tk.Label(f, text=label, bg=CARD, fg=GREY,
                 font=("Segoe UI", 9)).pack(anchor="w", padx=10, pady=(6,0))
        lbl = tk.Label(f, text=value, bg=CARD, fg=color,
                       font=("Consolas", 14, "bold"), width=22, anchor="w")
        lbl.pack(padx=10, pady=(0,8))
        f._value_label = lbl
        return f

    def _run(self):
        expr = self.expr_var.get().strip()
        if not expr:
            messagebox.showwarning("Input", "Enter an expression.")
            return
        postfix, steps = infix_to_postfix(expr)
        prefix          = infix_to_prefix(expr)
        self.postfix_card._value_label.config(text=postfix)
        self.prefix_card._value_label.config(text=prefix)
        self._clear_log()
        self._animate(steps)

    def _animate(self, steps):
        for i, step in enumerate(steps):
            self.after(i * 380, lambda s=step: self._draw_step(s))

    def _draw_steps(self, steps):
        for step in steps:
            self._draw_step(step)

    def _draw_step(self, step):
        op, token, output, stack = step
        color = {
            "OPERAND": GREEN, "OPERATOR": ACC,
            "PUSH_PAREN": BLUE, "POP_PAREN": RED
        }.get(op, FG)

        # canvas
        c = self.canvas
        c.delete("all")
        c.create_text(12, 18, anchor="w", text=f"Token: {token}",
                      fill=color, font=("Consolas", 11, "bold"))
        c.create_text(12, 42, anchor="w", text=f"Output: {output}",
                      fill=GREEN, font=("Consolas", 11))
        c.create_text(12, 66, anchor="w", text=f"Stack:  {stack}",
                      fill=BLUE, font=("Consolas", 11))
        c.create_text(12, 90, anchor="w", text=f"Step:   {op}",
                      fill=FG, font=("Consolas", 10))

        self._log_write(f"  {op:<14}  token={token:<4}  output={output}  stack={stack}\n", color)

    def _clear_log(self):
        self.log.config(state="normal")
        self.log.delete("1.0", "end")
        self.log.config(state="disabled")

    def _log_write(self, text, color=FG):
        self.log.config(state="normal")
        tag = f"t{color.replace('#','')}"
        self.log.tag_config(tag, foreground=color)
        self.log.insert("end", text, tag)
        self.log.see("end")
        self.log.config(state="disabled")
