#!/usr/bin/env python3
"""
Extract functions that have non-empty graphs and create a markdown file
"""

import json
import os
from pathlib import Path

def main():
    # Read the original API JSON
    api_json_path = Path('/home/lacra/git_repos/baif/curve25519-dalek-public-api.json')
    with open(api_json_path, 'r') as f:
        api_data = json.load(f)
    
    # Get list of DOT files (which represent non-empty graphs)
    graphs_dir = Path('/home/lacra/git_repos/baif/curve25519-dalek_public_apis_graphs')
    dot_files = list(graphs_dir.glob('*.dot'))
    
    # Extract function names from DOT filenames
    functions_with_graphs = set()
    for dot_file in dot_files:
        # Remove _5.dot suffix and convert underscores back to original format
        name = dot_file.stem[:-2]  # Remove _5
        functions_with_graphs.add(name)
    
    print(f"Found {len(functions_with_graphs)} functions with graphs")
    
    # Build markdown content
    md_content = ["# curve25519-dalek Public API Functions with libsignal Call Graphs\n"]
    md_content.append("This file lists only the curve25519-dalek public functions that have non-empty call graphs ")
    md_content.append("showing relationships with libsignal code.\n\n")
    md_content.append(f"Total functions with graphs: {len(functions_with_graphs)}\n")
    
    # Process each module from the original API
    for module_name, module_data in api_data['modules'].items():
        module_functions = []
        
        # Check types in module
        if 'types' in module_data:
            for type_name, type_data in module_data['types'].items():
                if 'constants' in type_data:
                    for const in type_data['constants']:
                        # Check if this constant has a graph
                        safe_name = f"{module_name.replace('/', '_')}_{type_name}__{const['name']}"
                        if any(safe_name in str(f) for f in functions_with_graphs):
                            module_functions.append(f"- `{const['signature']}`")
                
                if 'methods' in type_data:
                    for method in type_data['methods']:
                        # Check if this method has a graph
                        safe_name = f"{module_name.replace('/', '_')}_{type_name}_{method['name']}"
                        if any(safe_name in str(f) for f in functions_with_graphs):
                            module_functions.append(f"- `{method['signature']}`")
        
        # Check standalone functions
        if 'functions' in module_data:
            for function in module_data['functions']:
                safe_name = f"{module_name.replace('/', '_')}_{function['name']}"
                if any(safe_name in str(f) for f in functions_with_graphs):
                    module_functions.append(f"- `{function['signature']}`")
        
        # Check constants
        if 'constants' in module_data:
            for const in module_data['constants']:
                safe_name = f"{module_name.replace('/', '_')}_{const['name']}"
                if any(safe_name in str(f) for f in functions_with_graphs):
                    module_functions.append(f"- `{const['signature']}`")
        
        # Add to markdown if there are functions
        if module_functions:
            md_content.append(f"\n## Module: `{module_name}`\n")
            md_content.extend(module_functions)
    
    # Write the markdown file
    output_path = Path('/home/lacra/git_repos/baif/curve25519-dalek-public-api-with-graphs.md')
    with open(output_path, 'w') as f:
        f.write('\n'.join(md_content))
    
    print(f"Created {output_path}")

if __name__ == "__main__":
    main()