use std::collections::{HashSet, VecDeque};

use super::graph::{Graph, Vertex};

/// Implementation of graph algorithms by interfacing with the graph methods

impl Graph {
    /// Perform a breath first search from the given vertex and return a list of
    /// the visited vertices
    pub fn bfs(&self, u: Vertex) -> Vec<Vertex> {
        let mut res = vec![u];
        let mut queue = VecDeque::from([u]);
        // Loop through the queue
        while !queue.is_empty() {
            let v = queue.pop_front().expect("Queue should not be empty");
            for w in self.outgoing(v) {
                if !res.contains(&w) {
                    queue.push_back(w);
                    res.push(w);
                }
            }
        }
        res
    }

    /// Perform a depth first search from the given vertex and return a list of
    /// the visited vertices
    pub fn dfs(&self, u: Vertex) -> Vec<Vertex> {
        let mut res = vec![];
        let mut stack = VecDeque::from([u]);
        // Loop through the stack
        while !stack.is_empty() {
            let v = stack.pop_back().expect("Stack should not be empty");
            res.push(v);
            for w in self.outgoing(v).iter().rev() {
                if !res.contains(w) {
                    stack.push_back(*w);
                }
            }
        }
        res
    }

    /// Returns if the graph is connected or not
    pub fn is_connected(&self) -> bool {
        self.dfs(0).len() == self.n()
    }

    /// Return a list of all the vertices with no incoming edges
    pub fn no_incoming(&self) -> Vec<Vertex> {
        self.vs()
            .into_iter()
            .filter(|u| self.incoming(*u).is_empty())
            .collect()
    }

    /// Checks that the set of vertices is a connected component of the graph
    pub fn is_connected_component(&self, vs: Vec<Vertex>) -> bool {
        let set: HashSet<usize> = HashSet::from_iter(vs.iter().cloned());
        let mut g = self.clone();
        g.vs()
            .iter()
            .filter(|u| !set.contains(u))
            .for_each(|u| g.disconnect_vertex(*u));
        set == HashSet::from_iter(g.dfs(vs[0]))
    }

    /// Checks that the set of vertices is a clique of the graph
    pub fn is_clique(&self, vs: Vec<Vertex>) -> bool {
        for i in 0..vs.len() - 1 {
            for j in i + 1..vs.len() {
                if !self.has_edge(vs[i], vs[j]) {
                    return false;
                }
            }
        }
        true
    }

    /// Check that the set of vertices is a separator of the graph
    pub fn is_separator(&self, vs: HashSet<Vertex>) -> bool {
        self.is_connected_component(self.vs().into_iter().filter(|v| vs.contains(v)).collect())
    }

    /// Return the union of the neighbourhood of the set of vertices and the set
    /// itself
    pub fn neighbours(&self, vs: &HashSet<Vertex>) -> HashSet<Vertex> {
        let mut res = vs.clone();
        vs.iter().for_each(|v| res.extend(self.outgoing(*v)));
        res
    }

    /// Returning the smallest degree of any vertex of this graph
    pub fn min_degree(&self) -> usize {
        self.vs()
            .iter()
            .map(|v| self.outgoing(*v).len())
            .min()
            .unwrap_or(0)
    }

    /// Perform a topological sort of the vertices if possible, else return None
    pub fn topological_sort(&self) -> Option<Vec<Vertex>> {
        // Find all vertices with no incoming edge
        let mut g = self.clone();
        for u in g.no_incoming() {
            g.outgoing(u).iter().for_each(|v| g.del_edge(u, *v));
        }
        let mut res = vec![];
        let mut no_incoming = VecDeque::from(g.no_incoming());
        while !no_incoming.is_empty() {
            // Remove first vertex of the queue and add it to
            let u = no_incoming.pop_front().unwrap();
            res.push(u);
            g.outgoing(u).iter().for_each(|v| g.del_edge(u, *v));
            no_incoming = g
                .no_incoming()
                .into_iter()
                .filter(|v| !res.contains(v))
                .collect();
        }
        if res.len() == g.n() {
            return Some(res);
        }
        None
    }

    /// Return a list of all the full components after the vertices of the
    /// separator are removed
    ///
    /// A component 'C' is a full component of 'G \ S' if 'N(C) = S'
    pub fn full_components(&self, separator: HashSet<Vertex>) -> Vec<HashSet<Vertex>> {
        let mut g = self.clone();
        separator.iter().for_each(|v| g.disconnect_vertex(*v));
        let res = vec![];
        let remaining = &HashSet::from_iter(self.vs()) - &separator;

        for v in remaining.iter() {
            let mut c = g.outgoing(*v);
            c.push(*v);
            // TODO: Implement method of finding the component a vertex is in
            todo!()
        }
        res
    }

    /// Returns two lists of components in a given vertex set
    /// the first list contains full components
    /// the second contains non full components
    pub fn list_components(
        &self,
        vs: &HashSet<Vertex>,
        separator: &HashSet<Vertex>,
    ) -> (Vec<HashSet<Vertex>>, Vec<HashSet<Vertex>>) {
        let mut fulls = vec![];
        let mut non_fulls = vec![];
        for v in vs.iter() {
            // Grow component around current vertex
            let mut component = self.neighbours(&HashSet::from([*v]));
            let mut remaining = &component - separator;
            while !remaining.is_empty() {
                let save = component.clone();
                for w in remaining.iter() {
                    component = &component | &self.neighbours(&HashSet::from([*w]));
                }
                remaining = &(&component - &save) - separator;
            }
            if separator.is_subset(&component) {
                fulls.push(&component - separator);
            } else {
                non_fulls.push(&component - separator);
            }
        }
        (fulls, non_fulls)
    }

    /// Return connected components of the subgraph induced by the given
    /// vertices
    pub fn components_of(&self, vs: &HashSet<Vertex>) -> Vec<HashSet<Vertex>> {
        // Clone vertices
        let mut vs = vs.clone();
        let mut vs_vec = VecDeque::from_iter(vs.iter().cloned());
        let mut res = vec![];

        // Loop through vertices
        while !&vs_vec.is_empty() {
            let v = vs_vec.pop_front().unwrap();
            let mut c = self.neighbours(&HashSet::from([v]));
            let mut remaining = &c & &vs;
            while !remaining.is_empty() {
                let save = c.clone();
                for w in remaining {
                    c = &c | &self.neighbours(&HashSet::from([w]));
                }
                remaining = &c - &save;
                remaining = &remaining & &vs;
            }
            vs.retain(|v| !c.contains(v));
            vs_vec.retain(|v| !c.contains(v));
            res.push(c);
        }
        res
    }
}

#[cfg(test)]
mod tests {
    use std::collections::HashSet;

    use crate::graph;

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
    fn topological_sort() {
        let mut graph = graph!(5);
        graph.add_edges(vec![(0, 1), (1, 2), (2, 3), (3, 4)]);
        assert_eq!(Some(vec![0, 1, 2, 3, 4]), graph.topological_sort());
    }
    #[test]
    fn no_incoming_no_edges() {
        let mut graph = graph!(5);
        assert_eq!(vec![0, 1, 2, 3, 4], graph.no_incoming());
        graph.add_edge(1, 0);
        assert_eq!(vec![1, 2, 3, 4], graph.no_incoming());
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
        assert_eq!(true, graph.is_separator(HashSet::from([1])));
    }

    #[test]
    fn neighbourhood() {
        let mut graph = graph!(3);
        assert_eq!(HashSet::from([0]), graph.neighbours(&HashSet::from([0])));
        graph.add_bi_edge(0, 1);
        graph.add_bi_edge(1, 2);
        assert_eq!(HashSet::from([0, 1]), graph.neighbours(&HashSet::from([0])));
    }
}
