use std::{env, error::Error, fs};

use graph::Graph;

mod graph;
mod tree;

/// Convert the read contents of the input file into a graph struct
fn input_to_graph(string: String) -> Graph {
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

fn main() -> Result<(), Box<dyn Error>> {
    let args: Vec<String> = env::args().collect();
    let input = fs::read_to_string(&args[1])?;
    let graph = input_to_graph(input);
    graph.optimal_tree_decomposition();
    Ok(())
}
