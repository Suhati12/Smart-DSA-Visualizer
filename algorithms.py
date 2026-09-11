
"""
Pure Python implementations of all DSA algorithms.
"""
from collections import deque


# ── Infix → Postfix / Prefix ──────────────────────────────────────────────────

def precedence(op):
    return {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}.get(op, 0)

def is_operator(c):
    return c in "+-*/^"

def infix_to_postfix(expr):
    """Returns (postfix_string, steps_list)"""
    stack, output, steps = [], [], []
    for c in expr.replace(" ", ""):
        if c.isalnum():
            output.append(c)
            steps.append(("OPERAND", c, "".join(output), list(stack)))
        elif c == '(':
            stack.append(c)
            steps.append(("PUSH_PAREN", c, "".join(output), list(stack)))
        elif c == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if stack:
                stack.pop()
            steps.append(("POP_PAREN", c, "".join(output), list(stack)))
        elif is_operator(c):
            while stack and precedence(stack[-1]) >= precedence(c):
                output.append(stack.pop())
            stack.append(c)
            steps.append(("OPERATOR", c, "".join(output), list(stack)))
    while stack:
        output.append(stack.pop())
    return "".join(output), steps

def infix_to_prefix(expr):
    rev = expr[::-1]
    rev = rev.replace('(', 'TEMP').replace(')', '(').replace('TEMP', ')')
    stack, output = [], []
    for c in rev.replace(" ", ""):
        if c.isalnum():
            output.append(c)
        elif c == '(':
            stack.append(c)
        elif c == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if stack:
                stack.pop()
        elif is_operator(c):
            while stack and precedence(stack[-1]) > precedence(c):
                output.append(stack.pop())
            stack.append(c)
    while stack:
        output.append(stack.pop())
    return "".join(reversed(output))


# ── Duplicate Detection ───────────────────────────────────────────────────────

def find_duplicates(arr):
    """Returns (duplicates_set, steps_list)"""
    seen, dups, steps = set(), set(), []
    for x in arr:
        if x in seen:
            dups.add(x)
            steps.append(("FOUND", x))
        else:
            seen.add(x)
            steps.append(("CHECK", x))
    return sorted(dups), steps


# ── Graph BFS / DFS ───────────────────────────────────────────────────────────

DEFAULT_EDGES = [(0,1),(0,2),(1,3),(1,4),(2,5),(2,6)]

def bfs(edges, start=0):
    adj = {}
    for u, v in edges:
        adj.setdefault(u, []).append(v)
        adj.setdefault(v, []).append(u)
    visited, steps = set(), [("START", start)]
    q = deque([start])
    visited.add(start)
    while q:
        node = q.popleft()
        steps.append(("VISIT", node))
        for nb in adj.get(node, []):
            if nb not in visited:
                visited.add(nb)
                steps.append(("EDGE", node, nb))
                q.append(nb)
    return steps

def dfs(edges, start=0):
    adj = {}
    for u, v in edges:
        adj.setdefault(u, []).append(v)
        adj.setdefault(v, []).append(u)
    visited, steps = set(), [("START", start)]
    stack = [start]
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        steps.append(("VISIT", node))
        for nb in adj.get(node, []):
            if nb not in visited:
                steps.append(("EDGE", node, nb))
                stack.append(nb)
    return steps


# ── LRU Cache ─────────────────────────────────────────────────────────────────

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = []   # list of [key, val], index 0 = MRU
        self.steps = []

    def get(self, key):
        for i, (k, v) in enumerate(self.cache):
            if k == key:
                self.cache.pop(i)
                self.cache.insert(0, [key, v])
                self.steps.append(("OP", "GET_HIT", key, v, [list(x) for x in self.cache]))
                return v
        self.steps.append(("OP", "GET_MISS", key, -1, [list(x) for x in self.cache]))
        return -1

    def put(self, key, value):
        for i, (k, _) in enumerate(self.cache):
            if k == key:
                self.cache.pop(i)
                self.cache.insert(0, [key, value])
                self.steps.append(("OP", "PUT_UPDATE", key, value, [list(x) for x in self.cache]))
                return
        if len(self.cache) >= self.capacity:
            evicted = self.cache.pop()
            self.steps.append(("EVICT", evicted[0]))
        self.cache.insert(0, [key, value])
        self.steps.append(("OP", "PUT_NEW", key, value, [list(x) for x in self.cache]))

def default_lru_demo():
    lru = LRUCache(3)
    lru.put(1, 10); lru.put(2, 20); lru.put(3, 30)
    lru.get(1)
    lru.put(4, 40)
    lru.get(2)
    lru.get(3)
    lru.put(5, 50)
    lru.get(1)
    return lru.steps, 3
