use std::collections::{HashMap, HashSet};

use crate::{
    graph::{Graph, Vertex},
    msg::MinimalSeparatorGenerator,
};

type Node = usize;

pub struct Tree {
    nodes: HashMap<Node, HashSet<Vertex>>,
    edges: HashMap<Node, HashSet<Node>>,
    graph: Graph,
    treewidth: usize,
}

impl Tree {
    pub fn new(graph: &Graph, treewidth: usize) -> Self {
        Self {
            nodes: HashMap::new(),
            edges: HashMap::new(),
            graph: graph.clone(),
            treewidth,
        }
    }

    /// Return treewidth (one less than the size of the largest clique)
    pub fn treewidth(&self) -> usize {
        self.nodes.values().map(|set| set.len()).max().unwrap_or(0) - 1
    }

    /// Add a new vertex to a new bag
    pub fn add_vertex(&mut self, vertex: Vertex) {
        let bag = self.get_new_node();
        self.nodes.insert(bag, HashSet::from([vertex]));
    }

    /// Add a new vertex to a bag and create the bag if it doesn't exist
    pub fn add_vertex_to_bag(&mut self, node: usize, vertex: Vertex) {
        self.nodes.entry(node).or_insert_with(HashSet::new);
        self.nodes
            .get_mut(&node)
            .expect("key should be valid")
            .insert(vertex);
    }

    /// Add edge between two bags in the tree
    pub fn add_edge(&mut self, u: usize, v: usize) {
        self.edges.entry(u).or_insert_with(HashSet::new).insert(v);
    }

    /// Find the smallest positive value that does not exist as a bag id
    fn get_new_node(&self) -> usize {
        let mut i = 0;
        while self.nodes.contains_key(&i) {
            i += 1;
        }
        i
    }

    pub fn neighbour(&self, node: &Node) -> Vec<Node> {
        Vec::from_iter(self.edges.get(node).unwrap().iter().cloned())
    }

    /// Check if this structure satisfies the properties of a tree decomposition
    pub fn is_valid_tree(&self) -> bool {
        self.is_connected()
            && self.no_cycles()
            && self.valid_bag_sizes()
            && self.no_missing_vertex()
            && self.no_missing_edge()
            && self.satisfies_connectivity()
    }

    /// Check if from 1 vertex we can reach all other vertices
    fn is_connected(&self) -> bool {
        let mut visited = vec![false; self.nodes.len()];
        self.dfs(0, &mut visited);
        visited.iter().all(|n| *n)
    }

    /// Perform a dfs on the tree, marking the visited nodes
    fn dfs(&self, node: Node, visited: &mut Vec<bool>) {
        visited[node] = true;
        for next in self.neighbour(&node) {
            if !visited[next] {
                self.dfs(next, visited);
            }
        }
    }

    /// Check that there is no cycle of edges in the tree
    fn no_cycles(&self) -> bool {
        let mut visited = vec![false; self.nodes.len()];
        self.is_cyclic(1, &mut visited, 0)
    }

    fn is_cyclic(&self, node: Node, visited: &mut Vec<bool>, parent: Node) -> bool {
        visited[node] = true;
        for next in self.neighbour(&node) {
            if next == parent {
                continue;
            }
            if visited[next] {
                return true;
            } else {
                let is_cyclic = self.is_cyclic(next, visited, node);
                if is_cyclic {
                    return true;
                }
            }
        }
        false
    }

    /// Return if all the bags are smaller than the required size
    fn valid_bag_sizes(&self) -> bool {
        self.nodes
            .values()
            .all(|vertices| vertices.len() <= self.treewidth + 1)
    }

    /// Check that all vertices appear in some node
    fn no_missing_vertex(&self) -> bool {
        self.graph
            .vertices()
            .iter()
            .all(|vertex| self.nodes.values().any(|node| node.contains(&vertex)))
    }

    /// Check that all edges appear in some node
    fn no_missing_edge(&self) -> bool {
        self.graph.edges().iter().all(|(u, v)| {
            self.nodes
                .values()
                .any(|node| node.contains(u) && node.contains(v))
        })
    }

    /// Check that all nodes that contain a vertex is connected
    fn satisfies_connectivity(&self) -> bool {
        self.graph.vertices().iter().all(|vertex| {
            let mut visited = vec![false; self.graph.num_vertices()];
            for (node, vertices) in self.nodes.iter() {
                if vertices.contains(vertex) {
                    self.visit_bags(vertex, node, &mut visited);
                    break;
                }
            }
            self.nodes
                .iter()
                .all(|(node, vertices)| visited[*node] == vertices.contains(vertex))
        })
    }

    /// Given a vertex and a node, reach all available nodes
    fn visit_bags(&self, vertex: &Vertex, node: &Node, visited: &mut Vec<bool>) {
        if visited[*node] {
            return;
        }
        visited[*node] = true;
        for next in self.neighbour(&node) {
            if self.nodes.get(&next).unwrap().contains(&vertex) {
                self.visit_bags(vertex, &next, visited);
            }
        }
    }
}

/// Return a tree decomposition of the graph
pub fn optimal_tree_decomposition(graph: &Graph) -> Option<Tree> {
    // Loop from smallest to largest tree width
    for k in graph.min_degree()..graph.num_vertices() {
        // Generate tree decomposition and if it is valid return it
        let minimal_separators = MinimalSeparatorGenerator::new(graph, k).generate();
        println!("minimal separators: {:?}", minimal_separators);
        let tree = Tree::new(graph, k);
        let valid = tree.is_valid_tree();
        todo!();
    }
    None
}
