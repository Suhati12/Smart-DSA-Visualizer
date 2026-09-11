"""
Smart Data Structures Visualizer
C++ engine (g++) + Python GUI (Tkinter)

Run:
    python smart_dsa_visualizer/main.py

Requirements:
    g++     (optional — falls back to Python if missing)
    tkinter (built into Python)
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from backend.cpp_bridge import get_output, parse
from gui.app import App

if __name__ == "__main__":
    print("[*] Starting C++ engine…")
    data = parse(get_output())
    print(f"    Postfix : {data['postfix_result']}")
    print(f"    Prefix  : {data['prefix_result']}")
    print(f"    Dups    : {data['dup_result']}")
    print(f"    Edges   : {data['graph_edges']}")
    print("[*] Launching GUI…\n")
    App(data).mainloop()
