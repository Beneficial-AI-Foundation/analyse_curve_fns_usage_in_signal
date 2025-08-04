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

## Remarks

The script `extract_grey_nodes.py` lists the unique grey nodes and confirms that any curve25519-dalek node in any graph appears in `curve25519_dalek_svg_files.md`, meaning, it should be the sink node of a graph. So the 119 functions should be all functions called in signal: say we have `f` appear in one of the graphs; if `f` calls `g`, then `g` is one of the 119 functions and appears in one of the graphs.

### Color code
 
 Blue nodes correspond to functions from `libisignal`. Grey nodes correspond to functions from `curve25119_dalek` and green denotes the function which is given as input.

### How the graphs are generated

For each public function `f` from this [json](https://github.com/Beneficial-AI-Foundation/analyse_curve_fns_usage_in_signal/blob/dbe6f44608895a22a908dfaa37bd955f17ff2890/curve25519-dalek-public-api.json) (with a more readable variant as an [md file](https://github.com/Beneficial-AI-Foundation/analyse_curve_fns_usage_in_signal/blob/dbe6f44608895a22a908dfaa37bd955f17ff2890/curve25519-dalek-public-api.md)), a 5 depth graph is generated like this: say `g1`, ..., `gk` call `f`; we add all `gi -> f` edges; we add `g1` ...`gk` to process and reiterate for 4 more iterations; then we filter the graph so we see only the paths starting from a function which is in libsignal. (the callers we get from a [big json](https://github.com/Beneficial-AI-Foundation/rust-analyzer-test/blob/master/index_scip_libsignal_deps.json) file which is generated with `rust-analyzer` and `scip`).

To take as example `pub fn add(a: &Scalar52, b: &Scalar52) -> (s: Scalar52)` from [this graph](https://github.com/Beneficial-AI-Foundation/analyse_curve_fns_usage_in_signal/blob/dbe6f44608895a22a908dfaa37bd955f17ff2890/curve25519-dalek_public_apis_graphs/backend_serial_u64_scalar_impl__Scalar52_add_5.svg): 
- `add` is called by `from_bytes_wide` in the [same file](https://github.com/Beneficial-AI-Foundation/curve25519-dalek/blob/c396de153573ee410853a3e6090b5952d476034c/curve25519-dalek/src/backend/serial/u64/scalar.rs#L139) - `from_bytes_wide` is called by `from_bytes_mod_order_wide` in [src/scalar.rs](https://github.com/Beneficial-AI-Foundation/curve25519-dalek/blob/c396de153573ee410853a3e6090b5952d476034c/curve25519-dalek/src/scalar.rs#L250);
- `from_bytes_mod_order_wide` is called by `from_hash` at [this line](https://github.com/Beneficial-AI-Foundation/curve25519-dalek/blob/c396de153573ee410853a3e6090b5952d476034c/curve25519-dalek/src/scalar.rs#L672);
- `from_hash` is called by `calculate_signature` in [libsignal](https://github.com/signalapp/libsignal/blob/be9e9a3ab6dee816fdf50ace6443b22a1ee00472/rust/core/src/curve/curve25519.rs#L89)

(The svgs can be downloaded and opened with firefox, for better navigation and to see the body of the functions by hovering over the nodes.) 
