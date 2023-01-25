use std::collections::HashSet;

use crate::graph::{Graph, Vertex};

pub struct MinimalSeparatorGenerator {
    graph: Graph,
    k: usize,
    a_excluded: HashSet<Vertex>,
    minimal_separators: Vec<HashSet<Vertex>>,
}

impl MinimalSeparatorGenerator {
    pub fn new(graph: &Graph, k: usize) -> Self {
        MinimalSeparatorGenerator {
            graph: graph.clone(),
            k,
            a_excluded: HashSet::new(),
            minimal_separators: vec![],
        }
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
    pub fn generate(&mut self) -> Vec<HashSet<Vertex>> {
        // Get all vertices and sort by their neighbourhood size
        let mut vertices = self.graph.vertices();
        vertices.sort_by(|a, b| {
            self.graph
                .outgoing(*a)
                .len()
                .cmp(&self.graph.outgoing(*b).len())
        });

        // Generate all separators for each vertex 'a'
        for a in vertices {
            let (a_set, b_set) = self.generate_sides(a);
            let s_fixed = self.get_separator(&a_set);
            if s_fixed.len() > self.k {
                continue;
            }
            let separator: HashSet<Vertex> = self.graph.neighbourhood(&a_set);
            self.generate_minimal_separator(a, a_set, b_set, separator, s_fixed);
        }
        self.minimal_separators.clone()
    }

    /// Recursively generate a minimal separator
    fn generate_minimal_separator(
        &mut self,
        a: Vertex,
        a_set: HashSet<Vertex>,
        rest: HashSet<Vertex>,
        separator: HashSet<Vertex>,
        s_fixed: HashSet<Vertex>,
    ) {
        // Check that a_set neighbour and separator is the same
        let (fulls, non_fulls) = self.graph.list_components(&rest, &separator);

        // List components
        for full in fulls {
            self.branch(a, &a_set, &full, &separator, &s_fixed);
        }

        for non_full in non_fulls {
            let sep = self.graph.neighbourhood(&non_full);
            if !s_fixed.is_subset(&sep) {
                continue;
            }
            // TODO: continue usage
            let rest1 = &(&self.graph.vertex_set() - &non_full) - &separator;
        }
    }

    /// Recursively branch using nibble and conquer method
    fn branch(
        &mut self,
        a: Vertex,
        a_set: &HashSet<Vertex>,
        b_set: &HashSet<Vertex>,
        separator: &HashSet<Vertex>,
        s_fixed: &HashSet<Vertex>,
    ) {
        // TODO: validation
        if separator.len() > self.k {
            return;
        }
        self.minimal_separators.push(separator.clone());
        if separator.len() < self.k {
            // TODO: Implement recursion
            todo!();
        }
    }
    /// Given a vertex 'a' return the set of just that vertex and a set of all
    /// vertices but the neighbourhood of the vertex
    fn generate_sides(&self, a: Vertex) -> (HashSet<Vertex>, HashSet<Vertex>) {
        let a_set: HashSet<Vertex> = HashSet::from([a]);
        let b_set: HashSet<Vertex> =
            &HashSet::from_iter(self.graph.vertices()) - &self.graph.neighbourhood(&a_set);
        (a_set, b_set)
    }

    /// Given a set of vertices find the separator of that set of vertices
    fn get_separator(&self, a_set: &HashSet<Vertex>) -> HashSet<Vertex> {
        self.graph
            .neighbourhood(a_set)
            .intersection(&self.a_excluded)
            .cloned()
            .collect()
    }
}
