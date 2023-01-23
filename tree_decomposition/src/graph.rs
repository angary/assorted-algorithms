#![allow(unused_variables, dead_code, unused_macros)]

use std::collections::{HashSet, VecDeque};

use crate::tree::Tree;

#[derive(Debug, Clone)]
pub struct Graph {
    matrix: Vec<Vec<bool>>,
    num_edges: u32,
}

/// Macro for generating a new directed graph
#[macro_export]
macro_rules! graph {
    () => {
        Graph::new()
    };
    ($n:expr) => {{
        let mut graph = Graph::new();
        for _ in 0..$n {
            graph.add_vertex();
        }
        graph
    }};
}

impl Graph {
    pub fn new() -> Self {
        Self {
            matrix: vec![],
            num_edges: 0,
        }
    }

    /// Return the vertices
    pub fn vertices(&self) -> Vec<usize> {
        (0..self.num_vertices()).collect()
    }

    /// Return the number of vertices
    pub fn num_vertices(&self) -> usize {
        self.matrix.len()
    }

    /// Add a new vertex and return it's index
    pub fn add_vertex(&mut self) -> usize {
        // Add a new vertex
        self.matrix.push(vec![false; self.matrix.len() + 1]);
        // Add a new row to each of the other vertex
        for u in 0..self.num_vertices() - 1 {
            self.matrix[u].push(false);
        }
        self.num_vertices() - 1
    }

    /// Return a vec of the edges represented as tuples
    pub fn edges(&self) -> Vec<(usize, usize)> {
        let mut res = vec![];
        for v in self.vertices() {
            for u in self.vertices() {
                if u != v && self.matrix[u][v] {
                    res.push((u, v));
                }
            }
        }
        res
    }

    /// Return the number of edges
    pub fn num_edges(&self) -> u32 {
        self.num_edges
    }

    /// Add a new edge between the two vertices
    pub fn add_edge(&mut self, u: usize, v: usize) {
        if !self.matrix[u][v] {
            self.matrix[u][v] = true;
            self.num_edges += 1;
        }
    }

    /// Add a new bidirectional edge between the two vertices
    pub fn add_bi_edge(&mut self, u: usize, v: usize) {
        self.add_edge(u, v);
        self.add_edge(v, u);
    }

    /// Given a list of edges add all of them to the graph
    pub fn add_edges(&mut self, edges: Vec<(usize, usize)>) {
        edges.iter().for_each(|(u, v)| self.add_edge(*u, *v));
    }

    /// Remove the edge between the two vertices if it exists
    pub fn del_edge(&mut self, u: usize, v: usize) {
        if self.matrix[u][v] {
            self.matrix[u][v] = false;
            self.num_edges -= 1;
        }
    }

    /// Remove all incoming or outgoing edges from a vertex
    pub fn disconnect_vertex(&mut self, u: usize) {
        for v in self.vertices() {
            self.del_edge(u, v);
            self.del_edge(v, u);
        }
    }
    /// Return a list of the vertices that the given vertex has edges to
    pub fn outgoing(&self, u: usize) -> Vec<usize> {
        self.matrix[u]
            .iter()
            .enumerate()
            .filter(|(i, v)| **v)
            .map(|(i, v)| i)
            .collect()
    }

    /// Return a list of vertices that have outgoing edges to the given vertex
    pub fn incoming(&self, u: usize) -> Vec<usize> {
        self.matrix
            .iter()
            .enumerate()
            .filter(|(i, row)| row[u])
            .map(|(i, row)| i)
            .collect()
    }

    /// Perform a breath first search from the given vertex
    pub fn bfs(&self, u: usize) -> Vec<usize> {
        let mut res = vec![u];
        let mut seen = HashSet::from([u]);
        let mut queue = VecDeque::from([u]);
        // Loop through the queue
        while !queue.is_empty() {
            let v = queue.pop_front().expect("Queue should not be empty");
            for w in self.outgoing(v) {
                if !seen.contains(&w) {
                    seen.insert(w);
                    queue.push_back(w);
                    res.push(w);
                }
            }
        }
        res
    }

    /// Perform a depth first search from the given vertex
    pub fn dfs(&self, u: usize) -> Vec<usize> {
        let mut res = vec![];
        let mut seen = HashSet::from([u]);
        let mut stack = VecDeque::from([u]);
        // Loop through the stack
        while !stack.is_empty() {
            let v = stack.pop_back().expect("Stack should not be empty");
            res.push(v);
            for w in self.outgoing(v).iter().rev() {
                if !seen.contains(w) {
                    seen.insert(*w);
                    stack.push_back(*w);
                }
            }
        }
        res
    }

    /// Perform a topological sort of the vertices if possible, else return None
    pub fn topological_sort(&self) -> Option<Vec<usize>> {
        // Find all vertices with no incoming edge
        let mut graph = self.clone();
        graph.no_incoming().iter().for_each(|u| {
            graph
                .outgoing(*u)
                .iter()
                .for_each(|v| graph.del_edge(*u, *v));
        });
        let mut res = vec![];
        let mut no_incoming = VecDeque::from(graph.no_incoming());
        while !no_incoming.is_empty() {
            println!("res: {:?}", res);
            // Remove first vertex of the queue and add it to
            let u = no_incoming.pop_front().unwrap();
            res.push(u);
            graph.outgoing(u).iter().for_each(|v| graph.del_edge(u, *v));
            no_incoming = graph
                .no_incoming()
                .into_iter()
                .filter(|v| !res.contains(v))
                .collect();
        }
        if res.len() == graph.num_vertices() {
            return Some(res);
        }
        None
    }

    /// Return a list of all the vertices with no incoming edges
    pub fn no_incoming(&self) -> Vec<usize> {
        self.vertices()
            .iter()
            .filter(|u| self.incoming(**u).is_empty())
            .copied()
            .collect()
    }

    /// Checks that the set of vertices is a connected component of the graph
    pub fn is_connected_component(&self, vs: Vec<usize>) -> bool {
        let set: HashSet<usize> = HashSet::from_iter(vs.iter().cloned());
        let mut graph = self.clone();
        graph
            .vertices()
            .iter()
            .filter(|u| !set.contains(u))
            .for_each(|u| graph.disconnect_vertex(*u));
        let connected: HashSet<usize> = HashSet::from_iter(graph.dfs(vs[0]));
        println!("connected: {:?}", connected);
        set == connected
    }

    /// Checks that the set of vertices is a clique of the graph
    pub fn is_clique(&self, vs: Vec<usize>) -> bool {
        for i in 0..vs.len() - 1 {
            for j in i + 1..vs.len() {
                if !self.matrix[vs[i]][vs[j]] {
                    return false;
                }
            }
        }
        true
    }

    /// Check that the set of vertices is a separator of the graph
    pub fn is_separator(&self, vs: HashSet<usize>) -> bool {
        self.is_connected_component(
            self.vertices()
                .into_iter()
                .filter(|v| vs.contains(v))
                .collect(),
        )
    }

    /// Return the neighbourhood of the set of vertices
    pub fn neighbourhood(&self, vs: HashSet<usize>) -> HashSet<usize> {
        let mut res = vs.clone();
        vs.iter().for_each(|v| res.extend(self.outgoing(*v)));
        res
    }

    /// Return the set of all minimal separators of the graph of cardinality at
    /// most k
    ///
    /// Implements the nibble and conquer method, where rather than naively
    /// iterating all a-b minimal separators, use a recursive approach, where
    /// given a separator 'X', find all separators that "cross" 'X' and those
    /// that are "local to" to each component of 'G \ X'
    ///
    /// Given 'S' a minimal separator of 'G', we say 'S' "crosses" 'X' if 'S' is
    /// a minimal a-b separator for two distinct vertices 'a' and 'b' in 'X'.
    /// For a component 'C' of 'G \ X', we say that 'S' is local to 'C' with
    /// respect to 'X' if there is a full component 'D' associated with 'S' such
    /// that 'N[D]' is a subset of `X` union `C`
    pub fn minimal_separators(&self, k: usize) {
        todo!()
    }

    /// Return a tree decomposition of the graph
    pub fn optimal_tree_decomposition(&self) {
        // Select a random vertex
        let mut tree = Tree::new();
        tree.add_vertex(0);
    }
}

#[cfg(test)]
mod tests {

    use std::collections::HashSet;

    use super::Graph;

    #[test]
    fn empty_graph() {
        let graph = graph!();
        assert_eq!(vec![0; 0], graph.vertices());
        assert_eq!(vec![(0, 0); 0], graph.edges());
    }

    #[test]
    fn bfs() {
        let mut graph = graph!(5);
        graph.add_edges(vec![(0, 1), (0, 2), (1, 3), (2, 4)]);
        assert_eq!(vec![0, 1, 2, 3, 4], graph.bfs(0));
    }

    #[test]
    fn dfs() {
        let mut graph = graph!(5);
        graph.add_edges(vec![(0, 1), (0, 2), (1, 3), (2, 4)]);
        assert_eq!(vec![0, 1, 3, 2, 4], graph.dfs(0));
    }

    #[test]
    fn no_incoming_no_edges() {
        let mut graph = graph!(5);
        assert_eq!(vec![0, 1, 2, 3, 4], graph.no_incoming());
        graph.add_edge(1, 0);
        assert_eq!(vec![1, 2, 3, 4], graph.no_incoming());
    }

    #[test]
    fn topological_sort() {
        let mut graph = graph!(5);
        graph.add_edges(vec![(0, 1), (1, 2), (2, 3), (3, 4)]);
        assert_eq!(Some(vec![0, 1, 2, 3, 4]), graph.topological_sort());
    }

    #[test]
    fn is_connected_component() {
        let mut graph = graph!(3);
        graph.add_edges(vec![(0, 1), (1, 0)]);
        assert_eq!(true, graph.is_connected_component(vec![0, 1]));
        assert_eq!(false, graph.is_connected_component(vec![1, 2]));
        assert_eq!(false, graph.is_connected_component(vec![0, 1, 2]));
        graph.add_edges(vec![(2, 1), (1, 2)]);
        assert_eq!(true, graph.is_connected_component(vec![0, 1, 2]));
        assert_eq!(false, graph.is_connected_component(vec![0, 2]));
    }

    #[test]
    fn is_clique() {
        let mut graph = graph!(3);
        graph.add_bi_edge(0, 1);
        assert_eq!(true, graph.is_clique(vec![0, 1]));
        assert_eq!(false, graph.is_clique(vec![0, 1, 2]));
        graph.add_bi_edge(1, 2);
        assert_eq!(false, graph.is_clique(vec![0, 1, 2]));
        graph.add_bi_edge(0, 2);
        assert_eq!(true, graph.is_clique(vec![0, 1, 2]));
    }

    #[test]
    fn is_separator() {
        let mut graph = graph!(3);
        graph.add_edges(vec![(0, 1), (1, 0), (1, 2), (2, 1)]);
        assert_eq!(true, graph.is_separator(HashSet::from_iter(vec![1])));
    }

    #[test]
    fn neighbourhood() {
        let mut graph = graph!(3);
        assert_eq!(
            HashSet::from_iter(vec![0]),
            graph.neighbourhood(HashSet::from_iter(vec![0]))
        );
        graph.add_bi_edge(0, 1);
        graph.add_bi_edge(1, 2);
        assert_eq!(
            HashSet::from_iter(vec![0, 1]),
            graph.neighbourhood(HashSet::from_iter(vec![0]))
        );
    }
}
