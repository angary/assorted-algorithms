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

    /// Return treewidth (one less than the size of the largest clique)
    pub fn treewidth(&self) -> usize {
        self.nodes
            .values()
            .map(|set| set.len())
            .max()
            .unwrap_or(0)
            - 1
    }

    /// Add a new vertex to a new bag
    pub fn add_vertex(&mut self, vertex: usize) {
        let bag = self.get_new_node();
        self.nodes.insert(bag, HashSet::from([vertex]));
    }

    /// Add a new vertex to a bag and create the bag if it doesn't exist
    pub fn add_vertex_to_bag(&mut self, node: usize, vertex: usize) {
        self.nodes.entry(node).or_insert_with(HashSet::new);
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
