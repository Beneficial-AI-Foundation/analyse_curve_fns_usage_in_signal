# Curve25519-dalek Usage Analysis in libsignal

This repository contains an analysis of how the curve25519-dalek public API functions are used within the libsignal codebase.

## Summary

- **Total public functions in curve25519-dalek**: 557
- **Functions with non-empty call graphs**: 119

## Overview

This analysis generated call graphs showing the relationships between curve25519-dalek public API functions and their usage in libsignal. Out of 557 total public functions, methods, and constants in the curve25519-dalek library, 119 functions have non-empty call graphs indicating they are referenced in libsignal code. 

The generated graphs are stored as SVG files in the [curve25519-dalek_public_apis_graphs](https://github.com/Beneficial-AI-Foundation/analyse_curve_fns_usage_in_signal/tree/master/curve25519-dalek_public_apis_graphs) directory, with each graph visualizing the call relationships for a specific function. The names of the 119 sink nodes are enumerated [here](https://github.com/Beneficial-AI-Foundation/analyse_curve_fns_usage_in_signal/blob/master/curve25519_dalek_svg_files.md). 

## Files

- `curve25519-dalek-public-api.json` - Complete listing of all public APIs in curve25519-dalek v4.1.3
- `curve25519_dalek_svg_files.md` - Index of all 119 generated SVG graph files
- `curve25519-dalek_public_apis_graphs/processing_results.json` - Processing statistics and metadata

### Remark

The script `extract_grey_nodes.py` lists the unique grey nodes and confirms that any curve25519-dalek node in any graph appears in `curve25519_dalek_svg_files.md`, meaning, it should be the sink node of a graph. So the 119 functions should be all functions called in signal: say we have `f` appear in one of the graphs; if `f` calls `g`, then `g` is one of the 119 functions and appears in one of the graphs.
