# Ramsey lower bounds

I started Codex, OpenAI's coding agent (GPT-6.1 Sol, reasoning effort "Extra
High"), in an empty project and asked it to improve any of the open lower bounds
for the classical Ramsey numbers R(r,s) with r, s ≤ 10. To my surprise, less
than two hours later, running on the standard €23/month subscription, it had
found and verified a graph that raises the lower bound for R(8,10) from 343 to
344. All of its code ran locally on my desktop, an AMD Ryzen 9 5900X (12 cores).
The search that found the graph used a single core for about half an hour.

I then upgraded to the Pro subscription. In a new chat in the ChatGPT web
interface, I sent GPT-6 Pro a single prompt: "Improve the Ramsey lower bound for R(8, 10)".
It found a different graph that proves the same bound, running its search in
ChatGPT's own code environment. To check that this was
not a fluke, I gave the same prompt in two more new chats. Both succeeded too,
each with yet another graph: 3 out of 3.

After its first success, I let Codex continue on most of the 27 open cases with
r, s ≤ 10, at times with up to ten agents in parallel, using more than a
billion tokens in total. Despite this much larger effort, it found no further
improvement.

Each graph below is a complete, machine-checkable proof of the bound.

| Bound | Previous bound | Witness | Found by | SHA-256 |
| --- | --- | --- | --- | --- |
| R(8,10) ≥ 344 | 343 (Kuznetsov 2016) | [`R8_10/n343-gpt-6.1-sol.txt`](R8_10/n343-gpt-6.1-sol.txt) | Codex, GPT-6.1 Sol, 3 Oct 2026 | `f53fa7d45f427f16a159660194cf2de5b875fa0153660eb0fe348984e450095b` |
| | | [`R8_10/n343-gpt-6-pro-1.txt`](R8_10/n343-gpt-6-pro-1.txt) | ChatGPT, GPT-6 Pro, run 1, 4 Oct 2026 | `b913b14121c880a55f957947451cb42bcf1cf02ee3bc4fb40a6eb44d7661e0e1` |
| | | [`R8_10/n343-gpt-6-pro-2.txt`](R8_10/n343-gpt-6-pro-2.txt) | ChatGPT, GPT-6 Pro, run 2, 4 Oct 2026 | `4c0c0b7b4df4cd4040e20bca7c724a790e9ed35ae05aafdc30f2192806e840ec` |
| | | [`R8_10/n343-gpt-6-pro-3.txt`](R8_10/n343-gpt-6-pro-3.txt) | ChatGPT, GPT-6 Pro, run 3, 4 Oct 2026 | `a762539bb9d8543fb1313139c9b87e3e5ee04530aaa2faffa84aa5b9ed6c4263` |

The previous bound is the one given in Radziszowski's dynamic survey
[*Small Ramsey Numbers*](https://www.cs.rit.edu/~spr/ElJC/ejcram18.pdf), revision 18 (2026).

## Verify

```sh
pip install networkx
python verify.py
```

This takes a few minutes. Each witness should end with

```
  OK: no K_8 and no independent 10-set, hence R(8,10) >= 344
```

Cliquer 1.21 and igraph give the same clique numbers.

## Format

Each witness is stored twice:
- `R{r}_{s}/n{n}*.txt` is the adjacency matrix of a graph G on n vertices: n
  lines of n characters `0`/`1`, symmetric, with zero diagonal.
- `R{r}_{s}/n{n}*.g6` is the same graph in
  [graph6](https://users.cecs.anu.edu.au/~bdm/data/formats.txt) format, which
  nauty, SageMath and NetworkX read directly. `verify.py` checks that the two
  files agree.

G contains no clique of size r and no independent set of size s. Equivalently,
coloring the edges of K_n red (edges of G) and blue (non-edges) avoids a red K_r
and a blue K_s. This proves R(r,s) ≥ n + 1.

## How the graphs were constructed

All four runs took the same route:
1. Start from Kuznetsov's circulant (8,10)-graph on 342 vertices
   ([arXiv:1505.07186](https://arxiv.org/abs/1505.07186), Table 2).
2. Add a copy of vertex 0 that is not adjacent to it.
3. Repair the result by tabu-style local search, which may change edges
   anywhere in the graph.

The Codex graph differs from this starting graph in 874 vertex pairs. The three
GPT-6 Pro graphs differ from it in 565, 579 and 591 pairs. No two of the four
graphs are isomorphic; no two even have the same degree sequence. The Codex
agent and the first GPT-6 Pro run also searched for a graph on 344 vertices,
without success.

## How to cite

If you use or refer to these results, please cite:

> F. Cremer, *Ramsey lower bounds*, GitHub repository (2026),
> https://github.com/fritzcremer/ramsey-lower-bounds

```bibtex
@misc{cremer2026ramsey,
  author       = {Cremer, Fritz},
  title        = {Ramsey lower bounds},
  year         = {2026},
  howpublished = {\url{https://github.com/fritzcremer/ramsey-lower-bounds}},
  note         = {Witness graphs for $R(8,10) \ge 344$}
}
```

GitHub's "Cite this repository" button gives the same information from
[`CITATION.cff`](CITATION.cff).

## License

The contents of this repository are licensed under
[CC BY 4.0](LICENSE).
