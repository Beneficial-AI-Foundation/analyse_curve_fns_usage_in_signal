#!/usr/bin/env python3
"""
Generate call graphs for curve25519-dalek functions - parallel version
"""

import json
import subprocess
import os
import sys
from pathlib import Path
from multiprocessing import Pool, cpu_count
import time

def search_all_curve25519_symbols(scip_json_path):
    """Get all unique curve25519-dalek symbols"""
    cmd = ['grep', '-o', '"symbol":"[^"]*curve25519-dalek[^"]*"', scip_json_path]
    print("Searching for all curve25519-dalek symbols...")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            symbols = set()
            for line in result.stdout.strip().split('\n'):
                if '"symbol":"' in line:
                    symbol = line.split('"symbol":"')[1].rstrip('"')
                    # Filter for function symbols (those with () at the end)
                    if symbol.endswith('().'):
                        symbols.add(symbol)
            return sorted(list(symbols))
        return []
    except Exception as e:
        print(f"Error searching: {e}")
        return []

def generate_single_graph(args):
    """Generate graph for a single function symbol (for use with multiprocessing)"""
    scip_json_path, output_path, symbol, depth = args
    
    # Create a safe filename
    safe_name = symbol.replace('rust-analyzer cargo curve25519-dalek 4.1.3 ', '')
    safe_name = safe_name.replace('::', '_').replace('#', '_').replace('[', '_').replace(']', '_')
    safe_name = safe_name.replace('()', '').replace('.', '').replace(' ', '_').replace('/', '_')
    output_file = output_path / f"{safe_name}_5.dot"
    
    cmd = [
        'cargo', 'run', '--release', '--bin', 'generate_function_subgraph_dot',
        scip_json_path,
        str(output_file),
        symbol,
        '--filter-non-libsignal-sources',
        '--include-callers',
        '--depth', str(depth)
    ]
    
    try:
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            cwd='/home/lacra/git_repos/baif/rust-analyzer-test',
            timeout=30  # 30 second timeout per graph
        )
        
        if result.returncode == 0:
            # Check if the generated file is non-empty
            if output_file.exists() and output_file.stat().st_size > 0:
                # Check if the dot file has actual content (not just empty graph)
                with open(output_file, 'r') as f:
                    content = f.read()
                    if 'digraph' in content and '->' in content:
                        return (symbol, True, str(output_file))
                    else:
                        # Remove empty graph
                        output_file.unlink()
                        return (symbol, False, "empty graph")
            else:
                if output_file.exists():
                    output_file.unlink()
                return (symbol, False, "no file generated")
        else:
            return (symbol, False, f"error: {result.returncode}")
    except subprocess.TimeoutExpired:
        return (symbol, False, "timeout")
    except Exception as e:
        return (symbol, False, f"exception: {str(e)}")

def main():
    # Paths
    scip_json_path = '/home/lacra/git_repos/baif/rust-analyzer-test/index_scip_libsignal_deps.json'
    output_dir = Path('/home/lacra/git_repos/baif/curve25519-dalek_public_apis_graphs')
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    # Get all function symbols
    all_symbols = search_all_curve25519_symbols(scip_json_path)
    print(f"Found {len(all_symbols)} function symbols")
    
    # Prepare arguments for parallel processing
    args_list = [(scip_json_path, output_dir, symbol, 5) for symbol in all_symbols]
    
    # Use number of CPUs for parallel processing
    num_workers = min(cpu_count(), 8)  # Cap at 8 workers to avoid overwhelming the system
    print(f"Using {num_workers} parallel workers")
    
    # Process in parallel
    generated_graphs = 0
    failed_symbols = []
    start_time = time.time()
    
    with Pool(num_workers) as pool:
        # Process with progress updates
        for i, result in enumerate(pool.imap_unordered(generate_single_graph, args_list)):
            symbol, success, info = result
            short_name = symbol.replace('rust-analyzer cargo curve25519-dalek 4.1.3 ', '')
            
            if success:
                generated_graphs += 1
                print(f"[{i+1}/{len(all_symbols)}] ✓ {short_name}")
            else:
                failed_symbols.append((short_name, info))
                print(f"[{i+1}/{len(all_symbols)}] × {short_name} ({info})")
            
            # Show progress every 10 items
            if (i + 1) % 10 == 0:
                elapsed = time.time() - start_time
                rate = (i + 1) / elapsed
                remaining = (len(all_symbols) - (i + 1)) / rate
                print(f"  Progress: {i+1}/{len(all_symbols)} - Rate: {rate:.1f}/s - ETA: {remaining:.0f}s")
    
    # Print summary
    elapsed_total = time.time() - start_time
    print(f"\n{'='*50}")
    print(f"Summary:")
    print(f"  Total function symbols: {len(all_symbols)}")
    print(f"  Non-empty graphs generated: {generated_graphs}")
    print(f"  Failed/empty: {len(failed_symbols)}")
    print(f"  Time elapsed: {elapsed_total:.1f}s")
    print(f"  Average time per symbol: {elapsed_total/len(all_symbols):.2f}s")
    print(f"  Output directory: {output_dir}")
    
    # Save detailed results
    results = {
        'total_symbols': len(all_symbols),
        'generated_graphs': generated_graphs,
        'failed_symbols': failed_symbols,
        'elapsed_seconds': elapsed_total,
        'all_symbols': all_symbols
    }
    
    with open(output_dir / 'processing_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # List generated files
    dot_files = list(output_dir.glob('*.dot'))
    print(f"\nGenerated {len(dot_files)} .dot files")

if __name__ == "__main__":
    main()