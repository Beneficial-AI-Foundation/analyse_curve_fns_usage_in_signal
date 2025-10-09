#!/usr/bin/env python3
"""
Extract grey-colored nodes and sink nodes from DOT files in curve25519-dalek_public_apis_graphs directory.
Grey nodes represent curve25519-dalek functions and are marked with fillcolor=lightgray.
Sink nodes are curve25519-dalek nodes that have incoming edges but no outgoing edges.
"""

import json
import re
from pathlib import Path


def get_project_root():
    """Get the project root directory."""
    current = Path(__file__).resolve().parent
    return current.parent.parent


def parse_node_id(node_id, preserve_type_info=True):
    """
    Parse a node ID to extract file and function information.
    Returns (file, function) tuple or None if parsing fails.

    Args:
        node_id: The full node ID string
        preserve_type_info: If True, preserve type information from impl#[Type] patterns
    """
    # Split by spaces and find the part with the file path
    parts = node_id.split()

    # Find the part that contains the path (usually after version number)
    path_part = None
    for i, part in enumerate(parts):
        if "/" in part or part.endswith("()."):
            path_part = part
            break

    if path_part:
        # Remove trailing "()" and "."
        path_part = path_part.rstrip("().")

        # Split by '/' to get file and function
        if "/" in path_part:
            path_components = path_part.split("/")
            # The file is everything except the last component
            file_path = "/".join(path_components[:-1])
            # The function is the last component
            function_name = path_components[-1]

            # Handle special cases like impl#[Type]method
            if "impl#" in function_name:
                if preserve_type_info:
                    # Keep the full signature including type information
                    # e.g., "impl#[EdwardsPoint][MultiscalarMul]multiscalar_mul"
                    # becomes "impl#[EdwardsPoint][MultiscalarMul]multiscalar_mul"
                    pass  # Keep function_name as is
                else:
                    # Extract just the method name
                    # e.g., "impl#[EdwardsPoint][MultiscalarMul]multiscalar_mul" -> "multiscalar_mul"
                    match = re.search(r"impl#.*\]([^]]+)$", function_name)
                    if match:
                        function_name = match.group(1)

            # Add .rs extension if not present
            if not file_path.endswith(".rs"):
                file_path += ".rs"

            return (file_path, function_name)
        else:
            # If no '/' in path, it might be a top-level function
            return ("unknown.rs", path_part)

    return None


def extract_nodes_from_dot(dot_file_path, preserve_type_info=True):
    """
    Extract information about grey nodes and sink nodes from a DOT file.
    Returns a tuple of (grey_nodes_set, sink_node).

    Args:
        dot_file_path: Path to the DOT file
        preserve_type_info: Whether to preserve type information in function names
    """
    grey_nodes = set()
    all_nodes = {}  # node_id -> node_info
    outgoing_edges = set()  # nodes that have outgoing edges
    incoming_edges = set()  # nodes that have incoming edges

    with open(dot_file_path, "r") as f:
        content = f.read()

    # First, extract all nodes and identify grey nodes
    node_pattern = r'"([^"]+)"\s*\[([^\]]+)\]'
    matches = re.findall(node_pattern, content, re.DOTALL)

    for node_id, attributes in matches:
        # Check if it's a curve25519-dalek node
        if "curve25519-dalek" in node_id:
            all_nodes[node_id] = attributes

            # Check if it's grey
            if "fillcolor=lightgray" in attributes:
                parsed = parse_node_id(node_id, preserve_type_info=preserve_type_info)
                if parsed:
                    grey_nodes.add(parsed)

    # Now find all edges
    edge_pattern = r'"([^"]+)"\s*->\s*"([^"]+)"'
    edge_matches = re.findall(edge_pattern, content)

    for source, target in edge_matches:
        if "curve25519-dalek" in source:
            outgoing_edges.add(source)
        if "curve25519-dalek" in target:
            incoming_edges.add(target)

    # Find sink nodes (curve25519-dalek nodes with incoming edges but no outgoing edges)
    # Also consider isolated nodes (no edges at all) as potential sink nodes
    sink_node = None
    sink_nodes = []

    # Debug: check for green nodes
    green_count = 0
    for node_id in all_nodes:
        # Check if it's a green node (sink nodes are marked with fillcolor=green)
        if "fillcolor=green" in all_nodes[node_id]:
            green_count += 1
            parsed = parse_node_id(node_id, preserve_type_info=preserve_type_info)
            if parsed:
                sink_nodes.append(parsed)

    # If no green nodes found but we have curve25519 nodes, take the one with no outgoing edges
    if green_count == 0 and len(all_nodes) > 0:
        for node_id in all_nodes:
            if node_id in incoming_edges and node_id not in outgoing_edges:
                parsed = parse_node_id(node_id, preserve_type_info=preserve_type_info)
                if parsed:
                    sink_nodes.append(parsed)
                    break

    # There should be exactly one sink node per graph
    if len(sink_nodes) == 1:
        sink_node = sink_nodes[0]
    elif len(sink_nodes) > 1:
        print(f"  Warning: Multiple sink nodes found in {dot_file_path.name}: {sink_nodes}")
        sink_node = sink_nodes[0]  # Take the first one

    return grey_nodes, sink_node


def main():
    """
    Main function to process all DOT files and extract grey nodes and sink nodes.
    """
    # Directory containing the DOT files
    project_root = get_project_root()
    graphs_dir = project_root / "outputs" / "curve25519-dalek_public_apis_graphs_20"
    output_file = project_root / "data" / "grey_nodes_extracted_depth20.json"

    if not graphs_dir.exists():
        print(f"Error: Directory {graphs_dir} does not exist")
        return

    # Sets to store all unique (file, function) pairs
    # With type information preserved
    all_grey_nodes = set()
    all_sink_nodes = set()
    sink_node_to_files = {}  # Track which files have which sink nodes

    # Without type information (for comparison)
    all_grey_nodes_no_type = set()
    all_sink_nodes_no_type = set()

    # Process all DOT files
    dot_files = list(graphs_dir.glob("*.dot"))
    print(f"Found {len(dot_files)} DOT files to process")

    missing_sink_files = []

    for dot_file in dot_files:
        # Extract with type info preserved
        grey_nodes, sink_node = extract_nodes_from_dot(dot_file, preserve_type_info=True)
        all_grey_nodes.update(grey_nodes)

        # Extract without type info for comparison
        grey_nodes_no_type, sink_node_no_type = extract_nodes_from_dot(
            dot_file, preserve_type_info=False
        )
        all_grey_nodes_no_type.update(grey_nodes_no_type)

        if sink_node:
            all_sink_nodes.add(sink_node)
            # Track which files have this sink node
            if sink_node not in sink_node_to_files:
                sink_node_to_files[sink_node] = []
            sink_node_to_files[sink_node].append(dot_file.name)
        else:
            missing_sink_files.append(dot_file.name)

        if sink_node_no_type:
            all_sink_nodes_no_type.add(sink_node_no_type)

        if grey_nodes or sink_node:
            print(
                f"  {dot_file.name}: found {len(grey_nodes)} grey nodes, sink: {sink_node[1] if sink_node else 'None'}"
            )

    # Convert sets to sorted lists for JSON serialization
    # WITH type information
    grey_nodes_list = sorted(list(all_grey_nodes))
    sink_nodes_list = sorted(list(all_sink_nodes))
    all_curve25519_functions = sorted(list(all_grey_nodes | all_sink_nodes))

    # WITHOUT type information (for comparison)
    grey_nodes_list_no_type = sorted(list(all_grey_nodes_no_type))
    sink_nodes_list_no_type = sorted(list(all_sink_nodes_no_type))
    all_curve25519_functions_no_type = sorted(list(all_grey_nodes_no_type | all_sink_nodes_no_type))

    # Create a list of all sink nodes (one per DOT file)
    all_sink_nodes_per_file = []
    for dot_file in sorted(dot_files):
        grey_nodes, sink_node = extract_nodes_from_dot(dot_file, preserve_type_info=True)
        if sink_node:
            all_sink_nodes_per_file.append(
                {"dot_file": dot_file.name, "file": sink_node[0], "function": sink_node[1]}
            )

    # Calculate overlap (with type info)
    overlap = all_grey_nodes & all_sink_nodes
    grey_only = all_grey_nodes - all_sink_nodes
    sink_only = all_sink_nodes - all_grey_nodes

    # Calculate overlap (without type info)
    overlap_no_type = all_grey_nodes_no_type & all_sink_nodes_no_type
    grey_only_no_type = all_grey_nodes_no_type - all_sink_nodes_no_type
    sink_only_no_type = all_sink_nodes_no_type - all_grey_nodes_no_type

    # Create output dictionary
    output = {
        # PRIMARY COUNTS (with full type information preserved)
        "total_curve25519_functions_with_types": len(all_curve25519_functions),
        "total_grey_nodes_with_types": len(grey_nodes_list),
        "total_unique_sink_nodes_with_types": len(sink_nodes_list),
        "total_sink_nodes_per_file": len(all_sink_nodes_per_file),
        "overlap_grey_and_sink_with_types": len(overlap),
        "grey_only_with_types": len(grey_only),
        "sink_only_with_types": len(sink_only),
        # COMPARISON COUNTS (without type information, collapsed)
        "total_curve25519_functions_no_types": len(all_curve25519_functions_no_type),
        "total_grey_nodes_no_types": len(grey_nodes_list_no_type),
        "total_unique_sink_nodes_no_types": len(sink_nodes_list_no_type),
        "overlap_grey_and_sink_no_types": len(overlap_no_type),
        "grey_only_no_types": len(grey_only_no_type),
        "sink_only_no_types": len(sink_only_no_type),
        # DETAILED LISTS (with type information)
        "all_curve25519_functions": [
            {"file": file, "function": function} for file, function in all_curve25519_functions
        ],
        "grey_nodes": [{"file": file, "function": function} for file, function in grey_nodes_list],
        "unique_sink_nodes": [
            {"file": file, "function": function} for file, function in sink_nodes_list
        ],
        "all_sink_nodes": all_sink_nodes_per_file,
        # DETAILED LISTS (without type information)
        "all_curve25519_functions_no_types": [
            {"file": file, "function": function}
            for file, function in all_curve25519_functions_no_type
        ],
    }

    # Write to JSON file
    with open(output_file, "w") as f:
        json.dump(output, f, indent=2)

    print("\nExtraction complete!")
    print(f"\n{'=' * 80}")
    print("WITH TYPE INFORMATION (full function signatures including type parameters):")
    print(f"{'=' * 80}")
    print(f"Total curve25519-dalek functions: {len(all_curve25519_functions)}")
    print(f"  - Grey nodes (transitive dependencies): {len(grey_nodes_list)}")
    print(f"  - Unique sink nodes (entry points): {len(sink_nodes_list)}")
    print(f"  - Overlap (appear as both): {len(overlap)}")
    print(f"  - Grey only: {len(grey_only)}")
    print(f"  - Sink only: {len(sink_only)}")

    print(f"\n{'=' * 80}")
    print("WITHOUT TYPE INFORMATION (collapsed by function name only):")
    print(f"{'=' * 80}")
    print(f"Total curve25519-dalek functions: {len(all_curve25519_functions_no_type)}")
    print(f"  - Grey nodes (transitive dependencies): {len(grey_nodes_list_no_type)}")
    print(f"  - Unique sink nodes (entry points): {len(sink_nodes_list_no_type)}")
    print(f"  - Overlap (appear as both): {len(overlap_no_type)}")
    print(f"  - Grey only: {len(grey_only_no_type)}")
    print(f"  - Sink only: {len(sink_only_no_type)}")

    print(f"\n{'=' * 80}")
    print(f"Total DOT files processed: {len(dot_files)}")
    print(f"Total sink nodes (one per DOT file): {len(all_sink_nodes_per_file)}")
    print(f"Results saved to: {output_file}")
    print(f"{'=' * 80}")

    # Print first few examples (with type information)
    print("\nFirst 10 sink nodes (WITH type information):")
    for i, (file, function) in enumerate(sink_nodes_list[:10]):
        print(f"  {i + 1}. {file} :: {function}")

    print("\nFirst 10 grey nodes (WITH type information):")
    for i, (file, function) in enumerate(grey_nodes_list[:10]):
        print(f"  {i + 1}. {file} :: {function}")

    if missing_sink_files:
        print(f"\nWarning: {len(missing_sink_files)} DOT files have no sink nodes identified:")
        for f in missing_sink_files:
            print(f"  - {f}")

    # Check for duplicate sink nodes
    duplicate_sinks = [
        (sink, files) for sink, files in sink_node_to_files.items() if len(files) > 1
    ]
    if duplicate_sinks:
        print(f"\nNote: {len(duplicate_sinks)} sink nodes appear in multiple DOT files:")
        for sink, files in sorted(duplicate_sinks):  # Show all duplicates
            print(f"  {sink[0]} :: {sink[1]} appears in {len(files)} files:")
            for f in sorted(files):
                print(f"    - {f}")

    print("\nSummary:")
    print(f"  Total DOT files: {len(dot_files)}")
    print(f"  Unique sink nodes: {len(all_sink_nodes)}")
    print(f"  DOT files with identified sink nodes: {len(dot_files) - len(missing_sink_files)}")


if __name__ == "__main__":
    main()
