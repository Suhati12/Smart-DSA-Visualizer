import tkinter as tk
from tkinter import ttk
import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from backend.algorithms import bfs, dfs, DEFAULT_EDGES

BG    = "#F5F7FA"
CARD  = "#FFFFFF"
FG    = "#2C3E50"
ACC   = "#E67E22"
GREEN = "#27AE60"
RED   = "#E74C3C"
BLUE  = "#2980B9"
GREY  = "#AED6F1"
BORDER= "#D5D8DC"

class GraphTab(ttk.Frame):
    def __init__(self, parent, data=None):
        super().__init__(parent)
        self._cpp_data = data or {}
        self._mode = "BFS"
        self._steps = []
        self._step_idx = 0
        self._node_colors = {}
        self._active_edges = set()
        self._visited_order = []
        self._positions = {}
        self._prev_node = None
        self._build()

    def _build(self):
        tk.Label(self, text="🕸️  Graph Traversal — BFS & DFS",
                 bg=BG, fg=FG, font=("Segoe UI", 15, "bold")).pack(anchor="w", padx=20, pady=(16,6))

        ctrl = tk.Frame(self, bg=BG)
        ctrl.pack(fill="x", padx=20, pady=4)
        self.mode_var = tk.StringVar(value="BFS")
        for m in ("BFS", "DFS"):
            tk.Radiobutton(ctrl, text=m, variable=self.mode_var, value=m,
                           bg=BG, fg=FG, selectcolor=CARD, activebackground=BG,
                           font=("Segoe UI", 11, "bold"),
                           command=self._reset).pack(side="left", padx=6)
        for txt, cmd, color in [
            ("▶ Start",    self._reset, ACC),
            ("⏭ Next",    self._next,  BLUE),
            ("⚡ Auto",    self._auto,  GREEN),
        ]:
            tk.Button(ctrl, text=txt, command=cmd,
                      bg=color, fg="white", font=("Segoe UI", 10, "bold"),
                      relief="flat", padx=10, pady=5, cursor="hand2").pack(side="left", padx=4)

        self.canvas = tk.Canvas(self, bg=CARD, height=310,
                                highlightthickness=1, highlightbackground=BORDER)
        self.canvas.pack(fill="x", padx=20, pady=6)
        self.canvas.bind("<Configure>", lambda e: self._draw())

        self.order_lbl = tk.Label(self, text="Traversal order: —",
                                  bg=BG, fg=GREEN, font=("Segoe UI", 11, "bold"))
        self.order_lbl.pack(anchor="w", padx=20)

        frame = tk.Frame(self, bg=BG)
        frame.pack(fill="both", expand=True, padx=20, pady=(4,14))
        self.log = tk.Text(frame, bg=CARD, fg=FG, font=("Consolas", 10),
                           relief="solid", bd=1, state="disabled", height=6)
        sb = ttk.Scrollbar(frame, command=self.log.yview)
        self.log.configure(yscrollcommand=sb.set)
        self.log.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        self._reset()

    def _reset(self):
        self._mode = self.mode_var.get()
        edges = self._cpp_data.get("graph_edges") or DEFAULT_EDGES
        self._edges = edges
        if self._mode == "BFS":
            self._steps = self._cpp_data.get("bfs_steps") or bfs(edges)
        else:
            self._steps = self._cpp_data.get("dfs_steps") or dfs(edges)
        nodes = set()
        for u, v in edges: nodes.add(u); nodes.add(v)
        self._nodes = sorted(nodes)
        self._node_colors = {n: GREY for n in self._nodes}
        self._active_edges = set()
        self._visited_order = []
        self._step_idx = 0
        self._prev_node = None
        self._compute_positions()
        self._draw()
        self._clear_log()
        self.order_lbl.config(text="Traversal order: —")

    def _compute_positions(self):
        n = len(self._nodes)
        if not n: return
        w = self.canvas.winfo_width() or 700
        h = 300
        cx, cy, r = w // 2, h // 2, min(w, h) // 2 - 50
        for i, node in enumerate(self._nodes):
            angle = 2 * math.pi * i / n - math.pi / 2
            self._positions[node] = (cx + r * math.cos(angle),
                                     cy + r * math.sin(angle))

    def _draw(self):
        c = self.canvas; c.delete("all")
        if not self._positions: self._compute_positions()
        R = 22
        for u, v in self._edges:
            if u not in self._positions or v not in self._positions: continue
            x1, y1 = self._positions[u]
            x2, y2 = self._positions[v]
            active = (u, v) in self._active_edges or (v, u) in self._active_edges
            c.create_line(x1, y1, x2, y2,
                          fill=RED if active else "#BDC3C7",
                          width=3 if active else 1.5)
        for node in self._nodes:
            if node not in self._positions: continue
            x, y = self._positions[node]
            fill = self._node_colors.get(node, GREY)
            c.create_oval(x-R, y-R, x+R, y+R,
                          fill=fill, outline="#7F8C8D", width=2)
            c.create_text(x, y, text=str(node),
                          fill="white", font=("Segoe UI", 12, "bold"))
        # legend
        for i, (lbl, col) in enumerate([("Unvisited", GREY),
                                         ("Current",   ACC),
                                         ("Visited",   GREEN)]):
            c.create_oval(10, 10+i*22, 26, 26+i*22, fill=col, outline="#7F8C8D")
            c.create_text(32, 18+i*22, anchor="w", text=lbl,
                          fill=FG, font=("Segoe UI", 9))

    def _next(self):
        if self._step_idx >= len(self._steps):
            self._log_write("  ✓ Traversal complete.\n", GREEN); return
        step = self._steps[self._step_idx]
        if step[0] == "START":
            self._node_colors[step[1]] = ACC
            self._log_write(f"  Start node: {step[1]}\n", ACC)
        elif step[0] == "VISIT":
            node = step[1]
            if self._prev_node is not None:
                self._node_colors[self._prev_node] = GREEN
            self._node_colors[node] = ACC
            self._visited_order.append(node)
            self._prev_node = node
            self._log_write(f"  VISIT  {node}\n", ACC)
            self.order_lbl.config(
                text="Traversal order: " + " → ".join(map(str, self._visited_order)))
        elif step[0] == "EDGE":
            _, u, v = step
            self._active_edges.add((u, v))
            self._log_write(f"  EDGE   {u} → {v}\n", BLUE)
        self._draw()
        self._step_idx += 1

    def _auto(self):
        self._reset()
        def loop(i=0):
            if i < len(self._steps):
                self._next()
                self.after(580, lambda: loop(i+1))
            else:
                if self._prev_node is not None:
                    self._node_colors[self._prev_node] = GREEN
                self._draw()
        loop()

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
