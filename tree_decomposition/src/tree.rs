use std::collections::{HashMap, HashSet};

pub struct Tree {
    nodes: HashMap<usize, HashSet<usize>>,
    edges: Vec<(usize, usize)>,
}

impl Tree {
    pub fn new() -> Self {
        Self {
            nodes: HashMap::new(),
            edges: vec![],
        }
    }

    /// Add a new vertex to a new bag
    pub fn add_vertex(&mut self, vertex: usize) {
        let bag = self.get_new_node();
        self.nodes.insert(bag, HashSet::from([vertex]));
    }

    /// Add a new vertex to a bag and create the bag if it doesn't exist
    pub fn add_vertex_to_bag(&mut self, node: usize, vertex: usize) {
        if !self.nodes.contains_key(&node) {
            self.nodes.insert(node, HashSet::new());
        }
        self.nodes
            .get_mut(&node)
            .expect("key should be valid")
            .insert(vertex);
    }

    /// Add edge between two bags in the tree
    pub fn add_edge(&mut self, u: usize, v: usize) {
        self.edges.push((u, v));
    }

    /// Find the smallest positive value that does not exist as a bag id
    fn get_new_node(&self) -> usize {
        let mut i = 0;
        while self.nodes.contains_key(&i) {
            i += 1;
        }
        i
    }
}
