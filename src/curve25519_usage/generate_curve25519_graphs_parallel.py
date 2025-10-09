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


def get_project_root():
    """Get the project root directory."""
    current = Path(__file__).resolve().parent
    return current.parent.parent


def get_default_paths():
    """Get default paths relative to project root."""
    project_root = get_project_root()
    return {
        "scip_json": project_root / "data" / "index_scip_libsignal_deps.json",
        "output_dir": project_root / "outputs" / "curve25519-dalek_public_apis_graphs_20",
        "rust_analyzer_dir": os.getenv("RUST_ANALYZER_DIR", project_root.parent / "scip-callgraph"),
    }


def search_all_curve25519_symbols(scip_json_path):
    """Get all unique curve25519-dalek symbols"""
    cmd = ["grep", "-o", '"symbol":"[^"]*curve25519-dalek[^"]*"', scip_json_path]
    print("Searching for all curve25519-dalek symbols...")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            symbols = set()
            for line in result.stdout.strip().split("\n"):
                if '"symbol":"' in line:
                    symbol = line.split('"symbol":"')[1].rstrip('"')
                    # Filter for function symbols (those with () at the end)
                    if symbol.endswith("()."):
                        symbols.add(symbol)
            return sorted(list(symbols))
        return []
    except Exception as e:
        print(f"Error searching: {e}")
        return []


def generate_single_graph(args):
    """Generate graph for a single function symbol (for use with multiprocessing)"""
    scip_json_path, output_path, symbol, rust_analyzer_dir, depth = args

    # Create a safe filename
    safe_name = symbol.replace("rust-analyzer cargo curve25519-dalek 4.1.3 ", "")
    safe_name = safe_name.replace("::", "_").replace("#", "_").replace("[", "_").replace("]", "_")
    safe_name = safe_name.replace("()", "").replace(".", "").replace(" ", "_").replace("/", "_")
    output_file = output_path / f"{safe_name}_depth{depth}.dot"

    cmd = [
        "cargo",
        "run",
        "--release",
        "--bin",
        "generate_function_subgraph_dot",
        str(scip_json_path),
        str(output_file),
        symbol,
        "--filter-non-libsignal-sources",
        "--include-callers",
        "--depth",
        str(depth),
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(rust_analyzer_dir),
            timeout=120,  # 120 second timeout per graph (increased for depth 20)
        )

        if result.returncode == 0:
            # Check if the generated file is non-empty
            if output_file.exists() and output_file.stat().st_size > 0:
                # Check if the dot file has actual content (not just empty graph)
                with open(output_file, "r") as f:
                    content = f.read()
                    if "digraph" in content and "->" in content:
                        return (symbol, True, str(output_file), None)
                    else:
                        # Remove empty graph
                        output_file.unlink()
                        return (symbol, False, "empty graph", None)
            else:
                if output_file.exists():
                    output_file.unlink()
                return (symbol, False, "no file generated", None)
        else:
            # Capture stderr for error diagnosis
            error_msg = result.stderr.strip() if result.stderr else "no error message"
            # Truncate to last 200 chars to keep it manageable
            if len(error_msg) > 200:
                error_msg = "..." + error_msg[-200:]
            return (symbol, False, f"error: {result.returncode}", error_msg)
    except subprocess.TimeoutExpired:
        return (symbol, False, "timeout", "Process exceeded 120 second timeout")
    except Exception as e:
        return (symbol, False, f"exception: {str(e)}", str(e))


def main():
    # Get paths
    paths = get_default_paths()
    scip_json_path = paths["scip_json"]
    output_dir = paths["output_dir"]
    rust_analyzer_dir = paths["rust_analyzer_dir"]

    # Validate paths
    if not scip_json_path.exists():
        print(f"Error: SCIP JSON not found at {scip_json_path}")
        sys.exit(1)
    if not Path(rust_analyzer_dir).exists():
        print(f"Error: Rust analyzer directory not found at {rust_analyzer_dir}")
        print("Tip: Set RUST_ANALYZER_DIR environment variable to the correct path")
        sys.exit(1)

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Get all function symbols
    all_symbols = search_all_curve25519_symbols(scip_json_path)
    print(f"Found {len(all_symbols)} function symbols")

    # Prepare arguments for parallel processing
    # Using depth 20 for comprehensive call chains (increased from 15 to capture all dependencies)
    args_list = [
        (scip_json_path, output_dir, symbol, rust_analyzer_dir, 20) for symbol in all_symbols
    ]

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
            # Result can be (symbol, success, info) or (symbol, success, info, error_msg)
            symbol = result[0]
            success = result[1]
            info = result[2]
            error_msg = result[3] if len(result) > 3 else None

            short_name = symbol.replace("rust-analyzer cargo curve25519-dalek 4.1.3 ", "")

            if success:
                generated_graphs += 1
                print(f"[{i + 1}/{len(all_symbols)}] ✓ {short_name}")
            else:
                # Store with error message if available
                if error_msg and error_msg is not None:
                    failed_symbols.append((short_name, info, error_msg))
                else:
                    failed_symbols.append((short_name, info))
                print(f"[{i + 1}/{len(all_symbols)}] × {short_name} ({info})")

            # Show progress every 10 items
            if (i + 1) % 10 == 0:
                elapsed = time.time() - start_time
                rate = (i + 1) / elapsed
                remaining = (len(all_symbols) - (i + 1)) / rate
                print(
                    f"  Progress: {i + 1}/{len(all_symbols)} - Rate: {rate:.1f}/s - ETA: {remaining:.0f}s"
                )

    # Print summary with detailed failure breakdown
    elapsed_total = time.time() - start_time

    # Categorize failures by type
    from collections import Counter

    failure_reasons = Counter([item[1] for item in failed_symbols])

    print(f"\n{'=' * 50}")
    print("Summary:")
    print(f"  Total function symbols: {len(all_symbols)}")
    print(f"  Non-empty graphs generated: {generated_graphs}")
    print(f"  Failed/empty: {len(failed_symbols)}")
    print("\nFailure breakdown:")
    for reason, count in failure_reasons.most_common():
        print(f"  - {reason}: {count}")
    print("\nTiming:")
    print(f"  Time elapsed: {elapsed_total:.1f}s")
    print(f"  Average time per symbol: {elapsed_total / len(all_symbols):.2f}s")
    print("\nOutput:")
    print(f"  Directory: {output_dir}")

    # Save detailed error messages to a separate file
    error_details = []
    for item in failed_symbols:
        if len(item) >= 3 and item[1].startswith("error:"):
            symbol, reason, error_msg = item[0], item[1], item[2] if len(item) > 2 else "no details"
            error_details.append({"symbol": symbol, "reason": reason, "error_message": error_msg})

    if error_details:
        error_log_path = output_dir / "cargo_errors.json"
        with open(error_log_path, "w") as f:
            json.dump(error_details, f, indent=2)
        print(f"\nCargo errors saved to: {error_log_path}")
        print(f"  Total cargo errors: {len(error_details)}")

    # Save detailed results with failure breakdown
    results = {
        "total_symbols": len(all_symbols),
        "generated_graphs": generated_graphs,
        "failed_symbols": failed_symbols,
        "failure_breakdown": dict(failure_reasons),
        "elapsed_seconds": elapsed_total,
        "all_symbols": all_symbols,
    }

    with open(output_dir / "processing_results.json", "w") as f:
        json.dump(results, f, indent=2)

    # List generated files
    dot_files = list(output_dir.glob("*.dot"))
    print(f"\nGenerated {len(dot_files)} .dot files")


if __name__ == "__main__":
    main()
