
"""
Compiles engine.cpp with g++, runs it, parses output.
Falls back to pure-Python algorithms if g++ is not installed.
"""
import subprocess, os, sys

BASE = os.path.dirname(os.path.dirname(__file__))
SRC  = os.path.join(BASE, "cpp", "engine.cpp")
BIN  = os.path.join(BASE, "cpp", "engine.exe" if sys.platform == "win32" else "engine")


def _compile():
    r = subprocess.run(["g++", "-o", BIN, SRC, "-std=c++17"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr)


def _run():
    r = subprocess.run([BIN], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr)
    return r.stdout


def _python_fallback():
    """Generate identical output using pure Python when g++ unavailable."""
    from backend.algorithms import (infix_to_postfix, infix_to_prefix,
                                     find_duplicates, bfs, dfs, DEFAULT_EDGES)
    lines = []
    expr = "A+B*(C-D)/E"
    lines.append(f"EXPR_INPUT {expr}")

    postfix, steps = infix_to_postfix(expr)
    lines.append("POSTFIX_STEPS")
    for op, token, out, _ in steps:
        lines.append(f"STEP {op} {token} {out}")
    lines.append(f"POSTFIX_RESULT {postfix}")
    lines.append("POSTFIX_STEPS_END")
    lines.append(f"PREFIX_RESULT {infix_to_prefix(expr)}")

    arr = [4, 2, 7, 2, 9, 4, 1, 7, 3]
    lines.append("DUP_INPUT " + " ".join(map(str, arr)))
    dups, dup_steps = find_duplicates(arr)
    lines.append("DUP_STEPS")
    for kind, val in dup_steps:
        lines.append(f"DUP_{'FOUND' if kind=='FOUND' else 'CHECK'} {val}")
    lines.append("DUP_STEPS_END")
    lines.append("DUP_RESULT " + " ".join(map(str, dups)))

    lines.append("GRAPH_EDGES")
    for u, v in DEFAULT_EDGES:
        lines.append(f"{u} {v}")
    lines.append("GRAPH_EDGES_END")

    for step in bfs(DEFAULT_EDGES):
        if step[0] == "START":   lines.append(f"BFS_START {step[1]}")
        elif step[0] == "VISIT": lines.append(f"VISIT {step[1]}")
        elif step[0] == "EDGE":  lines.append(f"EDGE {step[1]} {step[2]}")
    lines.append("BFS_END")

    for step in dfs(DEFAULT_EDGES):
        if step[0] == "START":   lines.append(f"DFS_START {step[1]}")
        elif step[0] == "VISIT": lines.append(f"VISIT {step[1]}")
        elif step[0] == "EDGE":  lines.append(f"EDGE {step[1]} {step[2]}")
    lines.append("DFS_END")

    return "\n".join(lines)


def get_output():
    try:
        _compile()
        print("[✓] C++ engine compiled and running.")
        return _run()
    except Exception as e:
        print(f"[!] C++ unavailable: {e}\n    Falling back to Python engine.")
        return _python_fallback()


def parse(raw: str):
    lines = raw.strip().splitlines()
    data = {
        "expr_input": "", "postfix_steps": [],
        "postfix_result": "", "prefix_result": "",
        "dup_input": [], "dup_steps": [], "dup_result": [],
        "graph_edges": [], "bfs_steps": [], "dfs_steps": [],
    }
    mode = None
    for line in lines:
        line = line.strip()
        if not line: continue

        if line.startswith("EXPR_INPUT"):
            data["expr_input"] = line.split(" ", 1)[1]
        elif line == "POSTFIX_STEPS":       mode = "postfix"
        elif line == "POSTFIX_STEPS_END":   mode = None
        elif line.startswith("POSTFIX_RESULT"):
            data["postfix_result"] = line.split(" ", 1)[1]
        elif line.startswith("PREFIX_RESULT"):
            data["prefix_result"] = line.split(" ", 1)[1]
        elif line.startswith("DUP_INPUT"):
            data["dup_input"] = list(map(int, line.split()[1:]))
        elif line == "DUP_STEPS":           mode = "dup"
        elif line == "DUP_STEPS_END":       mode = None
        elif line.startswith("DUP_RESULT"):
            vals = line.split()[1:]
            data["dup_result"] = list(map(int, vals)) if vals else []
        elif line == "GRAPH_EDGES":         mode = "edges"
        elif line == "GRAPH_EDGES_END":     mode = None
        elif line.startswith("BFS_START"):
            mode = "bfs"
            data["bfs_steps"].append(("START", int(line.split()[1])))
        elif line == "BFS_END":             mode = None
        elif line.startswith("DFS_START"):
            mode = "dfs"
            data["dfs_steps"].append(("START", int(line.split()[1])))
        elif line == "DFS_END":             mode = None

        elif mode == "postfix" and line.startswith("STEP"):
            parts = line.split()          # STEP OP TOKEN OUTPUT
            op     = parts[1]
            token  = parts[2]
            output = parts[3] if len(parts) > 3 else ""
            data["postfix_steps"].append((op, token, output, []))
        elif mode == "dup":
            if line.startswith("DUP_CHECK"):
                data["dup_steps"].append(("CHECK", int(line.split()[1])))
            elif line.startswith("DUP_FOUND"):
                data["dup_steps"].append(("FOUND", int(line.split()[1])))
        elif mode == "edges":
            u, v = map(int, line.split())
            data["graph_edges"].append((u, v))
        elif mode in ("bfs", "dfs"):
            key = "bfs_steps" if mode == "bfs" else "dfs_steps"
            if line.startswith("VISIT"):
                data[key].append(("VISIT", int(line.split()[1])))
            elif line.startswith("EDGE"):
                _, u, v = line.split()
                data[key].append(("EDGE", int(u), int(v)))

    return data
