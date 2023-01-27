use std::collections::HashSet;

use crate::graphs::graph::{Graph, Vertex};

pub struct MinimalSeparatorGenerator {
    g: Graph,
    k: usize,
    a_excluded: HashSet<Vertex>,
    minimal_separators: Vec<HashSet<Vertex>>,
}

impl MinimalSeparatorGenerator {
    pub fn new(graph: &Graph, k: usize) -> Self {
        MinimalSeparatorGenerator {
            g: graph.clone(),
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
        let mut vertices = self.g.vs();
        vertices.sort_by_key(|v| self.g.outgoing(*v).len());

        // Generate all separators for each vertex 'a'
        self.a_excluded = HashSet::new();
        for a in vertices {
            let (a_set, b_set) = self.generate_sides(a);
            let s_fixed = self.get_separator(&a_set);
            if s_fixed.len() > self.k {
                continue;
            }
            let separator: HashSet<Vertex> = self.g.neighbours(&a_set);
            self.generate_minimal_separator(a, a_set, b_set, separator, s_fixed);
            self.a_excluded.insert(a);
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
        let (fulls, non_fulls) = self.g.list_components(&rest, &separator);

        // List components
        for full in fulls {
            self.branch(a, &a_set, &full, &separator, &s_fixed);
        }

        for non_full in non_fulls {
            let sep = self.g.neighbours(&non_full);
            if !s_fixed.is_subset(&sep) {
                continue;
            }
            let rest1 = &(&self.g.vs_set() - &non_full) - &separator;
            for c in self.g.components_of(&rest1) {
                if c.contains(&a) {
                    if c.is_disjoint(&self.a_excluded) {
                        self.branch(a, &c, &non_full, &sep, &s_fixed);
                    }
                    break;
                }
            }
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
        let n_v = self.g.n();
        let n_a = a_set.len();
        let n_s = separator.len();
        if n_s <= self.k && n_a > (n_v - n_s) / 2
            || n_s > self.k && n_a + (n_s - self.k) > (n_v - self.k) / 2
        {
            return;
        }

        if separator.len() > self.k {
            return;
        }
        assert!(s_fixed.is_subset(separator));
        assert!(s_fixed.len() <= self.k);
        assert!(&self.g.neighbours(a_set) == separator);
        assert!(&self.g.neighbours(b_set) == separator);

        self.minimal_separators.push(separator.clone());
        if separator.len() == self.k {
            return;
        }
        let to_decide = separator - s_fixed;
        assert!(to_decide.is_disjoint(&self.a_excluded));
        if to_decide.is_empty() {
            return;
        }
        let v = HashSet::from([self.largest_neighbourhood_vertex(&to_decide, b_set)]);
        let v_neighbours = self.g.neighbours(&v);
        let rest = b_set - &v_neighbours;
        let n_b = &(&v_neighbours - separator) - a_set;
        let separator_1 = &(separator - &v) | &n_b;
        let s_fixed_1 = s_fixed | &(&n_b & &self.a_excluded);
        if s_fixed_1.len() <= self.k {
            self.generate_minimal_separator(a, a_set | &v, rest, separator_1, s_fixed_1);
        }
        if s_fixed.len() < self.k {
            self.branch(a, a_set, b_set, separator, &(s_fixed & &v));
        }
    }

    /// Return the vertex that has the largest neighbourhood which intersects
    /// with a set
    fn largest_neighbourhood_vertex(
        &self,
        to_decide: &HashSet<Vertex>,
        set: &HashSet<Vertex>,
    ) -> Vertex {
        to_decide
            .iter()
            .map(|v| (*v, (&self.g.neighbours(&HashSet::from([*v])) & set).len()))
            .max_by_key(|(_, degree)| *degree)
            .unwrap()
            .0
    }

    /// Given a vertex 'a' return the set of just that vertex and a set of all
    /// vertices but the neighbourhood of the vertex
    fn generate_sides(&self, a: Vertex) -> (HashSet<Vertex>, HashSet<Vertex>) {
        let a_set: HashSet<Vertex> = HashSet::from([a]);
        let b_set: HashSet<Vertex> = &HashSet::from_iter(self.g.vs()) - &self.g.neighbours(&a_set);
        (a_set, b_set)
    }

    /// Given a set of vertices find the separator of that set of vertices
    fn get_separator(&self, a_set: &HashSet<Vertex>) -> HashSet<Vertex> {
        &self.g.neighbours(a_set) & &self.a_excluded
    }
}
