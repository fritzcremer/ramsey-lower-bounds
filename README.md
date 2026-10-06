# Ramsey lower bounds

**Current results: R(6,8) ≥ 135 and R(8,10) ≥ 345.** Explicit witness graphs
are included below.

I started Codex, OpenAI's coding agent (GPT-6.1 Sol, reasoning effort "Extra
High"), in an empty project and asked it to improve any of the open lower bounds
for the classical Ramsey numbers R(r,s) with r, s ≤ 10. To my surprise, less
than two hours later, running on my €23/month subscription, it had
found and verified a graph that raises the lower bound for R(8,10) from 343 to
344. All of its code ran locally on my desktop, an AMD Ryzen 9 5900X (12 cores).
The full search used a single core for about half an hour.

I then upgraded to the Pro subscription. In a new chat in the ChatGPT web
interface, I sent GPT-6 Pro a single prompt: "Improve the Ramsey lower bound for R(8, 10)".
It found a different graph that proves the same bound, running its search in
ChatGPT's own code environment. To check that this was
not a fluke, I gave the same prompt in two more new chats. Both succeeded too,
each with yet another graph: 3 out of 3.

After its first success, I let Codex continue on most of the 27 open cases with
r, s ≤ 10, at times with up to ten agents in parallel. About 1.5 billion further
tokens later, according to my OpenAI usage page, there had been no further
improvement. This was effort across the project, not just R(8,10).

I then became more involved in proposing ideas and directing the search, with
shorter, more varied experiments, shared checkpoints, and C++ searches. Across
the project, we have used up to 76 CPU cores at a time. This produced two
344-vertex witnesses proving **R(8,10) ≥ 345**, followed by a
134-vertex witness proving **R(6,8) ≥ 135**. The method contributions are described
briefly below.

Each graph below is a complete, machine-checkable proof of the bound.

| Bound | Previous bound | Witness | Found by | SHA-256 |
| --- | --- | --- | --- | --- |
| R(6,8) ≥ 135 | 134 (Exoo–Tatarevic 2015) | [`R6_8/n134-gpt-6.1-sol.txt`](R6_8/n134-gpt-6.1-sol.txt) | Codex-directed CPU search, 6 Oct 2026 | `8ef378ad4d66478c33939e438d3a64572ec2cf7d1647ae29d3568817fedfc982` |
| R(8,10) ≥ 345 | 344 (our first result below); survey: 343 | [`R8_10/n344-gpt-6.1-sol-1.txt`](R8_10/n344-gpt-6.1-sol-1.txt) | Codex-directed CPU search, 6 Oct 2026 | `17881b78e3d8b55372995f4e53ac068ca22560cf30b291c1e649eacaef21c21d` |
| | | [`R8_10/n344-gpt-6.1-sol-2.txt`](R8_10/n344-gpt-6.1-sol-2.txt) | Codex-directed CPU search, 6 Oct 2026 | `fd3c5a55434179a596dacd9f94a1208211e3ce0da7eee9502c640a3b1860ad89` |
| R(8,10) ≥ 344 | 343 (Kuznetsov 2016) | [`R8_10/n343-gpt-6.1-sol.txt`](R8_10/n343-gpt-6.1-sol.txt) | Codex, GPT-6.1 Sol, 3 Oct 2026 | `f53fa7d45f427f16a159660194cf2de5b875fa0153660eb0fe348984e450095b` |
| | | [`R8_10/n343-gpt-6-pro-1.txt`](R8_10/n343-gpt-6-pro-1.txt) | ChatGPT, GPT-6 Pro, run 1, 4 Oct 2026 | `b913b14121c880a55f957947451cb42bcf1cf02ee3bc4fb40a6eb44d7661e0e1` |
| | | [`R8_10/n343-gpt-6-pro-2.txt`](R8_10/n343-gpt-6-pro-2.txt) | ChatGPT, GPT-6 Pro, run 2, 4 Oct 2026 | `4c0c0b7b4df4cd4040e20bca7c724a790e9ed35ae05aafdc30f2192806e840ec` |
| | | [`R8_10/n343-gpt-6-pro-3.txt`](R8_10/n343-gpt-6-pro-3.txt) | ChatGPT, GPT-6 Pro, run 3, 4 Oct 2026 | `a762539bb9d8543fb1313139c9b87e3e5ee04530aaa2faffa84aa5b9ed6c4263` |

Radziszowski's dynamic survey
[*Small Ramsey Numbers*](https://www.cs.rit.edu/~spr/ElJC/ejcram18.pdf), revision 18
(24 April 2026), lists the lower bounds R(6,8) ≥ 134 and R(8,10) ≥ 343.

## Verify

```sh
pip install networkx
python verify.py
```

The verifier checks that each matrix and graph6 file agree, then checks the
largest clique and independent set. The new witnesses prove R(6,8) ≥ 135 and
R(8,10) ≥ 345. All seven witnesses also passed two independent exhaustive C++
checkers during the research.

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

The four original 343-vertex runs took the same route:

1. Start from Kuznetsov's circulant (8,10)-graph on 342 vertices
   ([arXiv:1505.07186](https://arxiv.org/abs/1505.07186), Table 2).
2. Add a copy of vertex 0 that is not adjacent to it.
3. Repair the result by tabu-style local search, which may change edges
   anywhere in the graph.

The Codex graph differs from this starting graph in 874 vertex pairs. The three
GPT-6 Pro graphs differ from it in 565, 579 and 591 pairs. No two of the four
graphs are isomorphic; no two even have the same degree sequence. The Codex
agent and the first GPT-6 Pro run also initially searched for a graph on 344
vertices without success.

The later **R(8,10) ≥ 345** witnesses extend the first Codex graph by another
vertex. I suggested Jeroen Cottaar's winning [Santa 2025 packing approach](https://www.kaggle.com/competitions/santa-2025/writeups/1st-place-genetic-algorithm-and-gpu-relaxation)
as inspiration: section mutation/crossover followed by repair. One successful
run copied 26 donor edges; the other applied a four-edge patch. Both then used
unrestricted global repair, producing two nonisomorphic graphs.

For **R(6,8) ≥ 135**, short trials combined risk chains, patches, rectangle and
block moves, and global repair, sharing promising checkpoints. The campaign
best fell from 6 to 5, 4, 2, 1 and finally 0 forbidden cliques.

I also suggested looking beyond just counting forbidden cliques and trying to
ease the pressure around them. My loss function adds up, for each edge, the size
of the largest monochromatic clique containing it. With this loss function, we
found a graph whose remaining conflicts were easier to repair, which became a
stepping stone toward the R(6,8) improvement.

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
  note         = {Witness graphs for $R(6,8) \ge 135$ and $R(8,10) \ge 345$}
}
```

GitHub's "Cite this repository" button uses the metadata in
[`CITATION.cff`](CITATION.cff).

## License

The contents of this repository are licensed under
[CC BY 4.0](LICENSE).
