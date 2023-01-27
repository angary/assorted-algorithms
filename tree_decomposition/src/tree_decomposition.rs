use std::collections::{HashMap, HashSet};

use crate::{
    graphs::graph::{Graph, Vertex},
    msg::MinimalSeparatorGenerator,
};

type Bag = usize;

pub struct TreeDecomposition {
    graph: Graph,
    treewidth: usize,
    bags: HashMap<Bag, HashSet<Vertex>>,
    edges: HashMap<Bag, HashSet<Bag>>,
}

impl TreeDecomposition {
    pub fn new(graph: &Graph, treewidth: usize) -> Self {
        Self {
            bags: HashMap::new(),
            edges: HashMap::new(),
            graph: graph.clone(),
            treewidth,
        }
    }

    /// Implementation of the decomposition algorithm
    pub fn decompose(&mut self, k: usize) -> Self {
        if self.treewidth >= self.graph.n() - 1 {
            let mut tree = Self::new(&self.graph, self.treewidth);
            tree.add_bag(self.graph.vs_set());
            return tree;
        }
        if !self.graph.is_connected() {
            let components = self.graph.components_of(&self.graph.vs_set());
            let mut decomposition = TreeDecomposition::new(&self.graph, 0);
            for component in components {
                // Create a new subgraph
            }
        }
        todo!();
    }
    /// Return treewidth (one less than the size of the largest clique)
    pub fn treewidth(&self) -> usize {
        self.bags.values().map(|set| set.len()).max().unwrap_or(0) - 1
    }

    /// Add a new vertex to a new bag
    pub fn add_vertex(&mut self, vertex: Vertex) {
        let bag = self.next_bag_id();
        self.bags.insert(bag, HashSet::from([vertex]));
    }

    /// Add a new vertex to a bag and create the bag if it doesn't exist
    pub fn add_vertex_to_bag(&mut self, bag_id: usize, vertex: Vertex) {
        self.bags.entry(bag_id).or_insert_with(HashSet::new);
        self.bags
            .get_mut(&bag_id)
            .expect("key should be valid")
            .insert(vertex);
    }

    /// Add a new bag to the graph with given values
    pub fn add_bag(&mut self, bag: HashSet<Vertex>) {
        let id = self.bags.len();
        todo!();
    }

    /// Add edge between two bags in the tree
    pub fn add_edge(&mut self, u: usize, v: usize) {
        self.edges.entry(u).or_insert_with(HashSet::new).insert(v);
    }

    /// Find the smallest positive value that does not exist as a bag id
    fn next_bag_id(&self) -> usize {
        let mut i = 0;
        while self.bags.contains_key(&i) {
            i += 1;
        }
        i
    }

    pub fn neighbour(&self, bag: &Bag) -> Vec<Bag> {
        Vec::from_iter(self.edges.get(bag).unwrap().iter().cloned())
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
        let mut visited = vec![false; self.bags.len()];
        self.dfs(0, &mut visited);
        visited.iter().all(|n| *n)
    }

    /// Perform a dfs on the tree, marking the visited bags
    fn dfs(&self, bag: Bag, visited: &mut Vec<bool>) {
        visited[bag] = true;
        for next in self.neighbour(&bag) {
            if !visited[next] {
                self.dfs(next, visited);
            }
        }
    }

    /// Check that there is no cycle of edges in the tree
    fn no_cycles(&self) -> bool {
        let mut visited = vec![false; self.bags.len()];
        self.is_cyclic(1, &mut visited, 0)
    }

    fn is_cyclic(&self, bag: Bag, visited: &mut Vec<bool>, parent: Bag) -> bool {
        visited[bag] = true;
        for next in self.neighbour(&bag) {
            if next == parent {
                continue;
            }
            if visited[next] {
                return true;
            } else {
                let is_cyclic = self.is_cyclic(next, visited, bag);
                if is_cyclic {
                    return true;
                }
            }
        }
        false
    }

    /// Return if all the bags are smaller than the required size
    fn valid_bag_sizes(&self) -> bool {
        self.bags
            .values()
            .all(|vertices| vertices.len() <= self.treewidth + 1)
    }

    /// Check that all vertices appear in some bag
    fn no_missing_vertex(&self) -> bool {
        self.graph
            .vs()
            .iter()
            .all(|vertex| self.bags.values().any(|bag| bag.contains(vertex)))
    }

    /// Check that all edges appear in some bag
    fn no_missing_edge(&self) -> bool {
        self.graph.edges().iter().all(|(u, v)| {
            self.bags
                .values()
                .any(|bag| bag.contains(u) && bag.contains(v))
        })
    }

    /// Check that all bags that contain a vertex is connected
    fn satisfies_connectivity(&self) -> bool {
        self.graph.vs().iter().all(|vertex| {
            let mut visited = vec![false; self.graph.n()];
            for (bag, vertices) in self.bags.iter() {
                if vertices.contains(vertex) {
                    self.visit_bags(vertex, bag, &mut visited);
                    break;
                }
            }
            self.bags
                .iter()
                .all(|(bag, vertices)| visited[*bag] == vertices.contains(vertex))
        })
    }

    /// Given a vertex and a bag, reach all available bags
    fn visit_bags(&self, vertex: &Vertex, bag: &Bag, visited: &mut Vec<bool>) {
        if visited[*bag] {
            return;
        }
        visited[*bag] = true;
        for next in self.neighbour(bag) {
            if self.bags.get(&next).unwrap().contains(vertex) {
                self.visit_bags(vertex, &next, visited);
            }
        }
    }
}

impl From<TreeDecomposition> for String {
    fn from(_: TreeDecomposition) -> Self {
        todo!()
    }
}
/// Return a tree decomposition of the graph
pub fn optimal_decomposition(graph: &Graph) -> Option<TreeDecomposition> {
    // Loop from smallest to largest tree width
    for k in graph.min_degree()..graph.n() {
        // Generate tree decomposition and if it is valid return it
        let minimal_separators = MinimalSeparatorGenerator::new(graph, k).generate();
        println!("minimal separators: {:?}", minimal_separators);
        let tree = TreeDecomposition::new(graph, k);
        let valid = tree.is_valid_tree();
        todo!();
    }
    None
}
