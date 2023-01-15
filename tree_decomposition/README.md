# Tree Decomposition

Implementation of graph and tree decomposition algorithm.

## Definition

A tree decomposition is a mapping of a graph $G = (V,E)$ to a tree $T$, where each node of $T$ is a set of vertices in $V$.
Formally, the decomposed tree $T$ has the following properties:

1. **Node Coverage** Every node of $G$ belongs to at least one node in $T$.
2. **Edge Coverage** For every edge $(u, v)$ in the graph $G$, there exists at least one tree node that contains both $u$ and $v$.
3. **Coherence** If node $X_i$ and $X_j$ both contain a vertex $v$, then all nodes $X_k$ along the (unique) path between $X_i$ and $X_j$ contain $v$ as well.

Note a graph can have multiple tree decompositions.

- The _width_ of a tree decomposition is defined as the maximum degree minus one taken over all nodes of $T$
- The _tree width_ $\text{tw}(G)$ of a graph $G$ is the minimum width taken over all its tree decompositions

## Properties

Many NP-hard graph problems are polynomially solvable on trees, and are thus FPT (Fixed Parameter Tractable) with parameter tree width.

There are two general methods to solving such problems in FPT

1. **Dynamic programming:** compute local information in a bottom-up fashion along a tree decomposition
2. **Monadic Second Order Logic:** express graph problem in some logic formalism and use a meta-algorithm

## Format

Note that the input and output format complies with the standards found [here](https://pacechallenge.wordpress.com/pace-2017/track-a-treewidth/).

## Running
