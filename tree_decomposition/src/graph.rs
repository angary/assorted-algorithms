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

    /// Remove a vertex
    pub fn del_vertex(&mut self, u: usize) {
        // Remove the column
        self.matrix.remove(u);
        self.matrix.iter_mut().for_each(|row| {
            row.remove(u);
        });
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

    /// Remove the edge between the two vertices if it exists
    pub fn del_edge(&mut self, u: usize, v: usize) {
        if self.matrix[u][v] {
            self.matrix[u][v] = false;
            self.num_edges -= 1;
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

    /// Perform a topological sort
    pub fn topological(&self) -> Option<Vec<usize>> {
        // Find all vertices with no incoming edge
        let mut graph = self.clone();
        let mut res = vec![];
        graph.no_incoming().iter().for_each(|u| {
            res.push(*u);
            graph.del_vertex(*u);
        });

        let mut no_incoming = VecDeque::from(graph.no_incoming());
        while !no_incoming.is_empty() {
            // Remove first vertex of the queue and add it to
            let u = no_incoming.pop_front().unwrap();
            res.push(u);
            graph.del_vertex(u);
            let mut also_no_incoming = graph.no_incoming();
            also_no_incoming.retain(|u| !&no_incoming.contains(u));
            also_no_incoming
                .iter()
                .for_each(|u| no_incoming.push_back(*u));
        }
        if graph.vertices().is_empty() {
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

    /// Return a tree decomposition of the graph
    pub fn greedy_tree_decomposition(&self, w: u32) {
        // Select a random vertex
        let mut tree = Tree::new();
        tree.add_vertex(0);
    }
}

#[cfg(test)]
mod tests {
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
        graph.add_edge(0, 1);
        graph.add_edge(0, 2);
        graph.add_edge(1, 3);
        graph.add_edge(2, 4);
        assert_eq!(vec![0, 1, 2, 3, 4], graph.bfs(0));
    }

    #[test]
    fn dfs() {
        let mut graph = graph!(5);
        graph.add_edge(0, 1);
        graph.add_edge(0, 2);
        graph.add_edge(1, 3);
        graph.add_edge(2, 4);
        assert_eq!(vec![0, 1, 3, 2, 4], graph.dfs(0));
    }

    #[test]
    fn no_incoming_no_edges() {
        let graph = graph!(5);
        assert_eq!(vec![0, 1, 2, 3, 4], graph.no_incoming());
    }

    #[test]
    fn no_incoming_one_edge() {
        let mut graph = graph!(5);
        graph.add_edge(1, 0);
        assert_eq!(vec![1, 2, 3, 4], graph.no_incoming());
    }

    #[test]
    fn topological() {
        let mut graph = graph!(5);
        graph.add_edge(0, 1);
        graph.add_edge(1, 2);
        graph.add_edge(2, 3);
        graph.add_edge(3, 4);
        assert_eq!(Some(vec![0, 1, 2, 3, 4]), graph.topological());
    }
}
