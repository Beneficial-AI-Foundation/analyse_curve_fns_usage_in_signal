#!/usr/bin/env python3
"""
Generate a CSV file with curve25519-dalek function information.

This script extracts function symbols from processing_results.json,
finds their definitions in the SCIP index, and generates a CSV with
GitHub links to the source code.

Note: This script only includes functions with successfully generated graphs.
Functions that failed for any reason (empty graph, error, timeout, etc.) are excluded.
This ensures the CSV contains only functions actually used in libsignal.
"""

import json
import csv
import re
from pathlib import Path
from typing import Dict, List, Tuple


def extract_symbols_from_processing_results(json_file: Path) -> List[str]:
    """Extract symbols from processing_results.json that have successfully generated graphs."""
    with open(json_file, "r") as f:
        data = json.load(f)

    # Get all symbols and failed symbols
    all_symbols = data.get("all_symbols", [])
    failed_symbols_list = data.get("failed_symbols", [])

    # Build set of ALL failed symbols (any failure reason)
    # Note: failed_symbols have shortened names without the prefix
    failed_symbols = set()
    for item in failed_symbols_list:
        if isinstance(item, list) and len(item) >= 1:
            symbol_id = item[0]
            failed_symbols.add(symbol_id)

    # Helper function to get short name (without prefix)
    def get_short_name(symbol):
        if "curve25519-dalek 4.1.3 " in symbol:
            return symbol.split("curve25519-dalek 4.1.3 ")[1]
        return symbol

    # Filter to only curve25519-dalek 4.1.3 symbols with successfully generated graphs
    # Also exclude benchmarks/tests
    curve_symbols = []
    for symbol in all_symbols:
        if "curve25519-dalek 4.1.3" in symbol:
            # Skip if it failed for ANY reason (compare using short name)
            short_name = get_short_name(symbol)
            if short_name in failed_symbols:
                continue

            # Exclude benchmarks and test files (these start with specific paths)
            if not any(x in symbol for x in ["_benches/", "/tests/", "/test/", "test_"]):
                # Also exclude if it's clearly in a test or bench module
                if (
                    "backend/" in symbol
                    or "edwards/" in symbol
                    or "ristretto/" in symbol
                    or "montgomery/" in symbol
                    or "scalar/" in symbol
                    or "field/" in symbol
                    or "traits/" in symbol
                    or "window/" in symbol
                    or "lizard/" in symbol
                    or "constants/" in symbol
                ):
                    curve_symbols.append(symbol)

    return curve_symbols


def parse_symbol_path(symbol: str) -> Dict[str, str]:
    """
    Parse a symbol ID to extract useful information.

    Example: 'rust-analyzer cargo curve25519-dalek 4.1.3 backend/serial/u64/field/impl#[FieldElement51]as_bytes().'
    """
    # Remove the prefix
    if "curve25519-dalek 4.1.3 " in symbol:
        path_part = symbol.split("curve25519-dalek 4.1.3 ")[1]
    else:
        path_part = symbol

    # Extract the display name (function name)
    # Pattern: ends with something like "function()." or "#[Type]method()."
    if "()." in path_part:
        # Get everything after the last / or #
        parts = re.split(r"[/#]", path_part)
        last_part = parts[-1]
        # Remove the ().
        func_name = last_part.replace("().", "")
    else:
        func_name = path_part

    return {"symbol_id": symbol, "path": path_part, "display_name": func_name}


def parse_scip_index(scip_file: Path) -> Dict[str, Tuple[str, int]]:
    """
    Parse the SCIP index and create a mapping from symbol IDs to their file locations.

    Returns a dictionary mapping symbol IDs to (file_path, line_number) tuples.
    """
    with open(scip_file, "r") as f:
        data = json.load(f)

    symbol_locations = {}

    for doc in data.get("documents", []):
        relative_path = doc.get("relative_path", "")

        # Only process curve25519-dalek files (not x25519-dalek or ed25519-dalek)
        if not relative_path.startswith("curve25519-dalek/"):
            continue

        # Build a symbol to occurrence mapping for definitions
        for occ in doc.get("occurrences", []):
            symbol = occ.get("symbol", "")
            symbol_roles = occ.get("symbol_roles", 0)

            # symbol_roles & 1 means it's a definition
            if symbol_roles & 1:
                range_info = occ.get("range", [])
                line_num = range_info[0] if range_info else 0

                # Only store if we haven't seen this symbol before
                # (prefer the first definition)
                if symbol not in symbol_locations:
                    symbol_locations[symbol] = (relative_path, line_num)

    return symbol_locations


def generate_github_link(file_path: str, line_num: int, version: str = "4.1.3") -> str:
    """Generate a GitHub link to the curve25519-dalek repository."""
    # Keep the full path including "curve25519-dalek/" prefix
    # The repository structure has the code in the curve25519-dalek/ subdirectory
    base_url = "https://github.com/dalek-cryptography/curve25519-dalek"
    return f"{base_url}/tree/curve25519-{version}/{file_path}#L{line_num}"


def main():
    """Main function to generate the CSV file."""
    # Paths
    base_dir = Path(__file__).parent.parent.parent
    processing_results_file = (
        base_dir / "outputs" / "curve25519-dalek_public_apis_graphs" / "processing_results.json"
    )
    scip_file = base_dir / "data" / "index_scip_curve25519-4.1.3.json"
    output_file = base_dir / "outputs" / "curve25519_functions.csv"

    print(f"Reading symbols from {processing_results_file}...")
    symbols = extract_symbols_from_processing_results(processing_results_file)
    print(f"Found {len(symbols)} curve25519-dalek symbols")

    print(f"\nParsing SCIP index from {scip_file}...")
    symbol_locations = parse_scip_index(scip_file)
    print(f"Found {len(symbol_locations)} symbol definitions in SCIP index")

    print("\nMatching symbols and generating CSV...")

    # Prepare CSV data with uniqueness enforcement
    rows = []
    matched = 0
    unmatched = []
    seen_functions = set()  # Track unique function names
    duplicates_skipped = 0

    for symbol in symbols:
        parsed = parse_symbol_path(symbol)
        function_name = parsed["path"]

        # Skip if we've already seen this function name (enforce uniqueness)
        if function_name in seen_functions:
            duplicates_skipped += 1
            continue
        seen_functions.add(function_name)

        # Try to find the location in SCIP index
        if symbol in symbol_locations:
            file_path, line_num = symbol_locations[symbol]
            github_link = generate_github_link(file_path, line_num)
            rows.append(
                {
                    "function_name": function_name,
                    "link": github_link,
                    "has_spec_verus": "",
                    "has_proof_verus": "",
                    "has_spec_hax": "",
                    "has_proof_hax": "",
                }
            )
            matched += 1
        else:
            # Still add to CSV but with empty link
            rows.append(
                {
                    "function_name": function_name,
                    "link": "",
                    "has_spec_verus": "",
                    "has_proof_verus": "",
                    "has_spec_hax": "",
                    "has_proof_hax": "",
                }
            )
            unmatched.append(function_name)

    # Write CSV
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", newline="") as f:
        fieldnames = [
            "function_name",
            "link",
            "has_spec_verus",
            "has_proof_verus",
            "has_spec_hax",
            "has_proof_hax",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nCSV file generated: {output_file}")
    print(f"Total unique entries: {len(rows)}")
    print(f"Matched: {matched}/{len(rows)} entries ({matched * 100 // len(rows) if rows else 0}%)")

    if duplicates_skipped > 0:
        print(f"Duplicates skipped: {duplicates_skipped}")

    if unmatched:
        print(f"\nUnmatched symbols ({len(unmatched)}):")
        for name in unmatched[:10]:  # Show first 10
            print(f"  - {name}")
        if len(unmatched) > 10:
            print(f"  ... and {len(unmatched) - 10} more")


if __name__ == "__main__":
    main()
