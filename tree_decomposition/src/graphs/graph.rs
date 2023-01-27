use std::collections::HashSet;

#[derive(Debug, Clone)]
pub struct Graph {
    matrix: Vec<Vec<bool>>,
}

pub type Vertex = usize;
pub type Edge = (Vertex, Vertex);

/// Macro for generating a new directed graph
#[macro_export]
macro_rules! graph {
    () => {
        $crate::Graph::new()
    };
    ($n:expr) => {{
        let mut graph = $crate::Graph::new();
        for _ in 0..$n {
            graph.add_vertex();
        }
        graph
    }};
}

impl Graph {
    pub fn new() -> Self {
        Self { matrix: vec![] }
    }

    /// Return the vertices in a vector
    pub fn vs(&self) -> Vec<Vertex> {
        (0..self.n()).collect()
    }

    /// Return the vertices in a set
    pub fn vs_set(&self) -> HashSet<Vertex> {
        HashSet::from_iter(self.vs())
    }

    /// Return the number of vertices
    pub fn n(&self) -> usize {
        self.matrix.len()
    }

    /// Add a new vertex and return it's index
    pub fn add_vertex(&mut self) -> Vertex {
        // Add a new vertex
        self.matrix.push(vec![false; self.matrix.len() + 1]);
        // Add a new row to each of the other vertex
        for u in 0..self.n() - 1 {
            self.matrix[u].push(false);
        }
        self.n() - 1
    }

    /// Return a vec of the edges represented as tuples
    pub fn edges(&self) -> Vec<Edge> {
        let mut res = vec![];
        for v in self.vs() {
            for u in self.vs() {
                if u != v && self.matrix[u][v] {
                    res.push((u, v));
                }
            }
        }
        res
    }

    /// Return if there is an edge between the two vertices
    pub fn has_edge(&self, u: Vertex, v: Vertex) -> bool {
        let vs = self.vs_set();
        if !vs.contains(&u) || !vs.contains(&v) {
            return false;
        }
        self.matrix[u][v]
    }

    /// Add a new directed edge between the two vertices
    pub fn add_edge(&mut self, u: Vertex, v: Vertex) {
        self.matrix[u][v] = true;
    }

    /// Add a new bidirectional edge between the two vertices
    pub fn add_bi_edge(&mut self, u: Vertex, v: Vertex) {
        self.add_edge(u, v);
        self.add_edge(v, u);
    }

    /// Given a list of edges add all of them to the graph
    pub fn add_edges(&mut self, edges: Vec<Edge>) {
        edges.iter().for_each(|(u, v)| self.add_edge(*u, *v));
    }

    /// Remove the edge between the two vertices if it exists
    pub fn del_edge(&mut self, u: Vertex, v: Vertex) {
        self.matrix[u][v] = false;
    }

    /// Remove all incoming or outgoing edges from a vertex
    pub fn disconnect_vertex(&mut self, u: Vertex) {
        for v in self.vs() {
            self.del_edge(u, v);
            self.del_edge(v, u);
        }
    }
    /// Return a list of the vertices that the given vertex has edges to
    pub fn outgoing(&self, u: Vertex) -> Vec<Vertex> {
        self.matrix[u]
            .iter()
            .enumerate()
            .filter(|(_, v)| **v)
            .map(|(i, _)| i)
            .collect()
    }

    /// Return a list of vertices that have outgoing edges to the given vertex
    pub fn incoming(&self, u: Vertex) -> Vec<Vertex> {
        self.matrix
            .iter()
            .enumerate()
            .filter(|(_, row)| row[u])
            .map(|(i, _)| i)
            .collect()
    }
}

impl From<String> for Graph {
    fn from(string: String) -> Self {
        let lines: Vec<&str> = string.split('\n').filter(|s| !s.starts_with('c')).collect();
        let num_vertices = lines[0]
            .split(' ')
            .nth(2)
            .expect("Missing number of vertices");
        let n: u32 = num_vertices
            .parse()
            .expect("Number of vertices be a valid number");
        let mut graph = graph!(n);
        for s in lines.iter().skip(1) {
            // Get src and des vertex
            let nums: Vec<usize> = s
                .split(' ')
                .map(|n| n.parse::<usize>().expect("Vertex be a number"))
                .collect();
            graph.add_bi_edge(nums[0], nums[1]);
        }
        graph
    }
}

#[cfg(test)]
mod tests {

    #[test]
    fn empty_graph() {
        let graph = graph!();
        assert_eq!(vec![0; 0], graph.vs());
        assert_eq!(vec![(0, 0); 0], graph.edges());
    }
}
