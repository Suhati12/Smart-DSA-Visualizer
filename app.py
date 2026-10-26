import tkinter as tk
from tkinter import ttk
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from gui.tab_expression import ExpressionTab
from gui.tab_duplicates  import DuplicatesTab
from gui.tab_graph       import GraphTab

BG     = "#F5F7FA"
CARD   = "#FFFFFF"
FG     = "#2C3E50"
ACC    = "#E67E22"
BORDER = "#D5D8DC"

TABS = [
    ("📐  Expression",  ExpressionTab),
    ("🔍  Duplicates",  DuplicatesTab),
    ("🕸️  Graph",       GraphTab),
]

def build_styles():
    s = ttk.Style()
    s.theme_use("clam")
    s.configure("TNotebook",
                background=BG, borderwidth=0, tabmargins=[0,0,0,0])
    s.configure("TNotebook.Tab",
                background="#E8ECF0", foreground=FG,
                font=("Segoe UI", 10, "bold"), padding=[16, 7])
    s.map("TNotebook.Tab",
          background=[("selected", CARD)],
          foreground=[("selected", ACC)])
    s.configure("Light.TFrame", background=BG)
    s.configure("TScrollbar",
                background=BORDER, troughcolor=BG,
                arrowcolor=FG, borderwidth=0, relief="flat")
    s.configure("TCombobox",
                fieldbackground=CARD, background=CARD,
                foreground=FG, selectbackground=ACC)
    s.configure("TPanedwindow", background=BG)


class App(tk.Tk):
    def __init__(self, data=None):
        super().__init__()
        self._data = data or {}
        self.title("Smart DSA Visualizer")
        self.geometry("1120x740")
        self.minsize(900, 620)
        self.configure(bg=BG)
        build_styles()
        self._build()

    def _build(self):
        # top bar
        bar = tk.Frame(self, bg=CARD, height=52, relief="flat")
        bar.pack(fill="x")
        bar.pack_propagate(False)
        tk.Frame(bar, bg=ACC, width=5).pack(side="left", fill="y")
        tk.Label(bar, text="⚡  Smart Data Structures Visualizer",
                 bg=CARD, fg=FG, font=("Segoe UI", 14, "bold")).pack(side="left", padx=16)
        tk.Label(bar, text="C++ Engine  ·  BFS  ·  DFS  ·  Infix → Postfix/Prefix  ·  Duplicate Detection",
                 bg=CARD, fg=BORDER, font=("Segoe UI", 9)).pack(side="right", padx=16)

        # separator
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")

        # notebook
        nb = ttk.Notebook(self, style="TNotebook")
        nb.pack(fill="both", expand=True, padx=0, pady=0)

        for label, TabClass in TABS:
            frame = TabClass(nb, self._data)
            frame.configure(style="Light.TFrame")
            nb.add(frame, text=label)
