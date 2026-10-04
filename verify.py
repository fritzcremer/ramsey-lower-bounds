#!/usr/bin/env python3
"""Verify the Ramsey lower-bound witnesses in this repository.

A file R{r}_{s}/n{n}*.txt is a graph G on n vertices with no clique of size r
and no independent set of size s. Such a graph proves R(r,s) >= n+1. If a
graph6 file with the same name exists, it is checked to encode the same graph.

    pip install networkx
    python verify.py            # all witnesses
    python verify.py FILE ...   # selected witnesses
"""
import hashlib
import re
import sys
import time
from pathlib import Path

import networkx as nx


def load(path):
    rows = path.read_text().split()
    n = len(rows)
    if any(len(row) != n or set(row) - {"0", "1"} for row in rows):
        sys.exit(f"{path}: not an n x n matrix of 0/1 entries")
    if any(rows[i][i] != "0" for i in range(n)):
        sys.exit(f"{path}: nonzero diagonal")
    if any(rows[i][j] != rows[j][i] for i in range(n) for j in range(i)):
        sys.exit(f"{path}: matrix is not symmetric")
    graph = nx.Graph()
    graph.add_nodes_from(range(n))
    graph.add_edges_from((i, j) for i in range(n) for j in range(i + 1, n) if rows[i][j] == "1")
    sha256 = hashlib.sha256("".join(row + "\n" for row in rows).encode()).hexdigest()
    return graph, sha256


def largest_clique(graph):
    clique, size = nx.max_weight_clique(graph, weight=None)  # exact branch and bound
    if any(not graph.has_edge(u, v) for u in clique for v in clique if u != v):
        sys.exit("internal error: returned set is not a clique")
    return size, sorted(clique)


def verify(path):
    r, s = map(int, re.fullmatch(r"R(\d+)_(\d+)", path.parent.name).groups())
    graph, sha256 = load(path)
    n = graph.number_of_nodes()
    print(f"{path}: {n} vertices, SHA-256 {sha256}")
    g6 = path.with_suffix(".g6")
    if g6.exists():
        other = nx.from_graph6_bytes(g6.read_bytes().strip())
        if other.number_of_nodes() != n or {frozenset(e) for e in other.edges()} != {
            frozenset(e) for e in graph.edges()
        }:
            print(f"  FAILED: {g6} does not encode the same graph")
            return False
        print(f"  {g6.name} encodes the same graph")
    start = time.time()
    omega, clique = largest_clique(graph)
    print(f"  largest clique:          {omega}  e.g. {clique}  ({time.time() - start:.0f} s)")
    start = time.time()
    alpha, independent = largest_clique(nx.complement(graph))
    print(f"  largest independent set: {alpha}  e.g. {independent}  ({time.time() - start:.0f} s)")
    if omega < r and alpha < s:
        print(f"  OK: no K_{r} and no independent {s}-set, hence R({r},{s}) >= {n + 1}")
        return True
    print(f"  FAILED: this graph does not prove R({r},{s}) >= {n + 1}")
    return False


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    files = [Path(f) for f in sys.argv[1:]] or [
        p.relative_to(here) if Path.cwd().resolve() == here else p
        for p in sorted(here.glob("R*_*/n*.txt"))
    ]
    results = [verify(f) for f in files]
    sys.exit(0 if results and all(results) else 1)
