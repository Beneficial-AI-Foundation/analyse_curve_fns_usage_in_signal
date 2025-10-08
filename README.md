# Curve25519-dalek Usage Analysis in libsignal

This repository contains an analysis of how curve25519-dalek v4.1.3 functions are used within the libsignal codebase.

## Summary

- **curve25519-dalek version**: 4.1.3
- **Total curve25519-dalek symbols analyzed**: 557
- **Functions with non-empty call graphs (called from libsignal)**: 119

## Overview

This analysis generated call graphs showing the relationships between curve25519-dalek v4.1.3 functions and their usage in libsignal. Out of 557 total symbols (including public API, internal functions, backend implementations, and trait implementations) in the curve25519-dalek v4.1.3 library, 119 functions have non-empty call graphs indicating they are called directly or transitively from libsignal code. 

The generated graphs are stored in the [outputs/curve25519-dalek_public_apis_graphs](outputs/curve25519-dalek_public_apis_graphs) directory, with each graph visualizing the call relationships for a specific function. The graphs are generated as `.dot` files and converted to `.svg` files for visualization. The names of the 119 sink nodes are enumerated [here](docs/curve25519_dalek_svg_files.md). 

## Installation

This project uses `uv` for fast, modern Python package management.

### Prerequisites

1. **Install uv** if you haven't already:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# or
pip install uv
```

2. **Set up rust-analyzer directory** (required for graph generation):
   - If the `rust-analyzer-test` directory is not in the parent directory, set the environment variable:
   ```bash
   export RUST_ANALYZER_DIR=/path/to/rust-analyzer-test
   ```
   - Or copy `.env.example` to `.env` and configure the path there

### Install the project:
```bash
# Sync dependencies and install the package
uv sync

# Or install manually
uv pip install -e .
```

### Quick start:
```bash
# Run commands directly with uv (no activation needed!)
uv run generate-curve25519-graphs-parallel
uv run extract-grey-nodes
uv run extract-functions-with-graphs
uv run extract-public-api-from-scip  # Extract public API from SCIP index
```

## Project Structure

```
.
├── src/curve25519_usage/     # Main package source code
│   ├── __init__.py
│   ├── generate_curve25519_graphs.py
│   ├── generate_curve25519_graphs_parallel.py
│   ├── extract_grey_nodes.py
│   ├── extract_functions_with_graphs.py
│   └── ...
├── data/                      # Input data files
│   ├── curve25519-dalek-public-api.json
│   └── index_scip_libsignal_deps.json
├── outputs/                   # Generated outputs (graphs, etc.)
│   └── curve25519-dalek_public_apis_graphs/
├── docs/                      # Documentation files
│   ├── curve25519_dalek_svg_files.md
│   ├── curve25519-dalek-public-api.md
│   └── curve25519-dalek-public-api-with-graphs.md
├── logs/                      # Log files from processing
├── tests/                     # Test files
├── pyproject.toml            # Project configuration and dependencies
└── README.md                 # This file
```

## Usage

After installation, you can use the command-line tools:

```bash
# With uv (recommended - no activation needed)
uv run generate-curve25519-graphs
uv run generate-curve25519-graphs-parallel
uv run extract-grey-nodes
uv run extract-functions-with-graphs
uv run extract-public-api-from-scip

# Or with activated virtual environment
generate-curve25519-graphs
generate-curve25519-graphs-parallel
extract-grey-nodes
extract-functions-with-graphs
extract-public-api-from-scip
```

## Development

Common development tasks with `uv`:

```bash
# Sync dependencies (install/update all dependencies)
uv sync

# Run tests
uv run pytest

# Format code
uv run black src/
uv run ruff check src/

# Run a script directly
uv run python src/curve25519_usage/generate_curve25519_graphs.py

# Add a new dependency
uv add <package-name>

# Add a dev dependency
uv add --dev <package-name>
```

## Data Files

- `data/index_scip_libsignal_deps.json` - SCIP index containing all symbols and call relationships for curve25519-dalek v4.1.3 and libsignal (generated with rust-analyzer and scip)
- `data/index_scip_curve25519-4.1.3.json` - SCIP index for curve25519-dalek v4.1.3 only
- `data/curve25519-dalek-public-api.json` - Reference documentation of public APIs in curve25519-dalek v4.1.3 (can be regenerated with `extract-public-api-from-scip`)
- `docs/curve25519_dalek_svg_files.md` - Index of all 119 generated SVG graph files
- `outputs/curve25519-dalek_public_apis_graphs/processing_results.json` - Processing statistics and metadata

### Regenerating the Public API JSON

The `curve25519-dalek-public-api.json` file can be regenerated from the SCIP index:

```bash
uv run extract-public-api-from-scip
```

This script extracts all public API functions, methods, and constants from the SCIP index and organizes them by module and type. Note that the extracted API depends on the compilation configuration used when generating the SCIP index (e.g., 64-bit vs 32-bit backends).

## Remarks

The 119 functions with non-empty graphs represent **all curve25519-dalek v4.1.3 functions that are reachable from libsignal code**. This includes:
- **58** typed implementations (methods on public types like `EdwardsPoint::double()`)
- **45** backend implementations (internal u64/field operations)
- **9** standalone public API functions
- **7** trait implementations (Identity, MultiscalarMul, etc.)

The script `extract_grey_nodes.py` confirms that any curve25519-dalek node in any graph appears in `curve25519_dalek_svg_files.md`, meaning it is a sink node in a graph. In other words: if function `f` appears in any graph and `f` calls `g` (where both are in curve25519-dalek), then `g` is one of the 119 functions and has its own graph.

### Color code
 
 Blue nodes correspond to functions from `libisignal`. Grey nodes correspond to functions from `curve25119_dalek` and green denotes the function which is given as input.

### How the graphs are generated

The analysis extracts **all** curve25519-dalek v4.1.3 symbols from the [SCIP index](https://github.com/Beneficial-AI-Foundation/rust-analyzer-test/blob/master/index_scip_libsignal_deps.json) (generated with `rust-analyzer` and `scip`). This includes public API functions, internal backend implementations, trait implementations, and helper functions.

For each curve25519-dalek v4.1.3 function `f`, a 5-depth call graph is generated: if functions `g1`, ..., `gk` call `f`, we add all `gi -> f` edges, then recursively process `g1`, ..., `gk` for 4 more iterations. The graph is then filtered to show only paths starting from a libsignal function. This ensures we capture all curve25519-dalek code that is **actually reachable** from libsignal, whether it's public API or internal implementation details.

**Example:** Consider the internal backend function `pub fn add(a: &Scalar52, b: &Scalar52) -> (s: Scalar52)` from [this graph](https://github.com/Beneficial-AI-Foundation/analyse_curve_fns_usage_in_signal/blob/dbe6f44608895a22a908dfaa37bd955f17ff2890/curve25519-dalek_public_apis_graphs/backend_serial_u64_scalar_impl__Scalar52_add_5.svg). Even though `add` is an internal backend implementation (not public API), it appears as a sink node because it's reachable from libsignal:
- `add` is called by `from_bytes_wide` (internal) in the [same file](https://github.com/Beneficial-AI-Foundation/curve25519-dalek/blob/c396de153573ee410853a3e6090b5952d476034c/curve25519-dalek/src/backend/serial/u64/scalar.rs#L139)
- `from_bytes_wide` is called by `from_bytes_mod_order_wide` (public API) in [src/scalar.rs](https://github.com/Beneficial-AI-Foundation/curve25519-dalek/blob/c396de153573ee410853a3e6090b5952d476034c/curve25519-dalek/src/scalar.rs#L250)
- `from_bytes_mod_order_wide` is called by `from_hash` (public API) at [this line](https://github.com/Beneficial-AI-Foundation/curve25519-dalek/blob/c396de153573ee410853a3e6090b5952d476034c/curve25519-dalek/src/scalar.rs#L672)
- `from_hash` is called by `calculate_signature` in [libsignal](https://github.com/signalapp/libsignal/blob/be9e9a3ab6dee816fdf50ace6443b22a1ee00472/rust/core/src/curve/curve25519.rs#L89)

This demonstrates why we analyze all symbols, not just public API: internal functions like `add` are part of the actual code execution path.

(The svgs can be downloaded and opened with firefox, for better navigation and to see the body of the functions by hovering over the nodes.) 
