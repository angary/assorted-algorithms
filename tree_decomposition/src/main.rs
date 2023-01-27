use std::{error::Error, fs};

mod graphs;
mod msg;
mod tree_decomposition;

use clap::Parser;
use graphs::graph::Graph;
use tree_decomposition::optimal_decomposition;

#[derive(Parser, Debug)]
struct Args {
    // Input file containing the graph in DIMACs representation
    input: String,

    // File to output the tree decomposition in DIMACs representation
    output: String,
}

fn main() -> Result<(), Box<dyn Error>> {
    let args = Args::parse();
    let input = fs::read_to_string(&args.input)?;
    let graph = Graph::from(input);
    match optimal_decomposition(&graph) {
        Some(tree) => {
            println!("Valid tree decomposition found");
            let string = String::from(tree);
            fs::write(args.output, string).expect("Unable to write to file");
        }
        None => {
            println!("No valid tree decomposition found");
        }
    };
    Ok(())
}
