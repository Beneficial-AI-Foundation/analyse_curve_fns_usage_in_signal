"""
Test suite for curve25519_usage package.

Tests core functionality including:
- Node ID parsing from SCIP symbols
- DOT file parsing and node extraction
- Filename sanitization
- Path resolution
"""

import pytest
from pathlib import Path
from curve25519_usage import __version__
from curve25519_usage.extract_grey_nodes import parse_node_id, extract_nodes_from_dot
from curve25519_usage.generate_curve25519_graphs_parallel import (
    get_project_root,
    search_all_curve25519_symbols,
)


def test_version():
    """Test that version is defined."""
    assert __version__ == "0.1.0"


class TestParseNodeId:
    """Tests for parse_node_id function from extract_grey_nodes.py"""

    def test_parse_standard_function(self):
        """Test parsing of standard function node."""
        node_id = "rust-analyzer cargo curve25519-dalek 4.1.3 src/scalar.rs/from_hash()."
        result = parse_node_id(node_id)
        assert result == ("src/scalar.rs", "from_hash")

    def test_parse_method_with_impl(self):
        """Test parsing of method with impl block."""
        node_id = (
            "rust-analyzer cargo curve25519-dalek 4.1.3 src/edwards.rs/impl#[EdwardsPoint]double()."
        )
        result = parse_node_id(node_id)
        assert result == ("src/edwards.rs", "double")

    def test_parse_trait_implementation(self):
        """Test parsing of trait implementation method."""
        node_id = "rust-analyzer cargo curve25519-dalek 4.1.3 src/edwards.rs/impl#[EdwardsPoint][MultiscalarMul]multiscalar_mul()."
        result = parse_node_id(node_id)
        assert result == ("src/edwards.rs", "multiscalar_mul")

    def test_parse_backend_function(self):
        """Test parsing of backend function with nested path."""
        node_id = "rust-analyzer cargo curve25519-dalek 4.1.3 backend/serial/u64/scalar.rs/add()."
        result = parse_node_id(node_id)
        assert result == ("backend/serial/u64/scalar.rs", "add")

    def test_parse_nested_module(self):
        """Test parsing of function in nested module."""
        node_id = "rust-analyzer cargo curve25519-dalek 4.1.3 src/backend/serial/curve_models/montgomery.rs/differential_add_and_double()."
        result = parse_node_id(node_id)
        assert result == (
            "src/backend/serial/curve_models/montgomery.rs",
            "differential_add_and_double",
        )

    def test_parse_identity_trait(self):
        """Test parsing of Identity trait implementation."""
        node_id = "rust-analyzer cargo curve25519-dalek 4.1.3 src/edwards.rs/impl#[EdwardsPoint][Identity]identity()."
        result = parse_node_id(node_id)
        assert result == ("src/edwards.rs", "identity")

    def test_parse_invalid_node_id(self):
        """Test that invalid node ID returns None."""
        node_id = "invalid node id without proper structure"
        result = parse_node_id(node_id)
        assert result is None

    def test_parse_node_without_parentheses(self):
        """Test parsing node without trailing parentheses."""
        node_id = (
            "rust-analyzer cargo curve25519-dalek 4.1.3 src/constants.rs/ED25519_BASEPOINT_TABLE"
        )
        result = parse_node_id(node_id)
        # Should still parse the constant/value
        assert result is not None


class TestExtractNodesFromDot:
    """Tests for extract_nodes_from_dot function"""

    def test_extract_simple_graph(self, tmp_path):
        """Test extracting nodes from a simple DOT graph."""
        dot_content = """digraph {
    "libsignal func" [fillcolor=lightblue]
    "rust-analyzer cargo curve25519-dalek 4.1.3 src/scalar.rs/from_hash()." [fillcolor=green]
    "rust-analyzer cargo curve25519-dalek 4.1.3 src/scalar.rs/from_bytes_wide()." [fillcolor=lightgray]
    
    "libsignal func" -> "rust-analyzer cargo curve25519-dalek 4.1.3 src/scalar.rs/from_hash()."
    "rust-analyzer cargo curve25519-dalek 4.1.3 src/scalar.rs/from_hash()." -> "rust-analyzer cargo curve25519-dalek 4.1.3 src/scalar.rs/from_bytes_wide()."
}"""

        dot_file = tmp_path / "test.dot"
        dot_file.write_text(dot_content)

        grey_nodes, sink_node = extract_nodes_from_dot(dot_file)

        # Should have one grey node
        assert len(grey_nodes) == 1
        assert ("src/scalar.rs", "from_bytes_wide") in grey_nodes

        # Should identify the sink node (green)
        assert sink_node == ("src/scalar.rs", "from_hash")

    def test_extract_multiple_grey_nodes(self, tmp_path):
        """Test extracting multiple grey nodes from DOT file."""
        dot_content = """digraph {
    "rust-analyzer cargo curve25519-dalek 4.1.3 src/scalar.rs/func1()." [fillcolor=green]
    "rust-analyzer cargo curve25519-dalek 4.1.3 src/scalar.rs/func2()." [fillcolor=lightgray]
    "rust-analyzer cargo curve25519-dalek 4.1.3 src/edwards.rs/func3()." [fillcolor=lightgray]
    "rust-analyzer cargo curve25519-dalek 4.1.3 backend/serial/u64/scalar.rs/add()." [fillcolor=lightgray]
    
    "rust-analyzer cargo curve25519-dalek 4.1.3 src/scalar.rs/func1()." -> "rust-analyzer cargo curve25519-dalek 4.1.3 src/scalar.rs/func2()."
    "rust-analyzer cargo curve25519-dalek 4.1.3 src/scalar.rs/func2()." -> "rust-analyzer cargo curve25519-dalek 4.1.3 src/edwards.rs/func3()."
    "rust-analyzer cargo curve25519-dalek 4.1.3 src/edwards.rs/func3()." -> "rust-analyzer cargo curve25519-dalek 4.1.3 backend/serial/u64/scalar.rs/add()."
}"""

        dot_file = tmp_path / "test_multiple.dot"
        dot_file.write_text(dot_content)

        grey_nodes, sink_node = extract_nodes_from_dot(dot_file)

        # Should have three grey nodes
        assert len(grey_nodes) == 3
        assert ("src/scalar.rs", "func2") in grey_nodes
        assert ("src/edwards.rs", "func3") in grey_nodes
        assert ("backend/serial/u64/scalar.rs", "add") in grey_nodes

    def test_extract_empty_graph(self, tmp_path):
        """Test extracting from an empty DOT graph."""
        dot_content = """digraph {
}"""

        dot_file = tmp_path / "empty.dot"
        dot_file.write_text(dot_content)

        grey_nodes, sink_node = extract_nodes_from_dot(dot_file)

        assert len(grey_nodes) == 0
        assert sink_node is None

    def test_extract_graph_without_green_node(self, tmp_path):
        """Test extracting from graph without explicit green sink node."""
        dot_content = """digraph {
    "libsignal func" [fillcolor=lightblue]
    "rust-analyzer cargo curve25519-dalek 4.1.3 src/scalar.rs/terminal()." [fillcolor=lightgray]
    
    "libsignal func" -> "rust-analyzer cargo curve25519-dalek 4.1.3 src/scalar.rs/terminal()."
}"""

        dot_file = tmp_path / "no_green.dot"
        dot_file.write_text(dot_content)

        grey_nodes, sink_node = extract_nodes_from_dot(dot_file)

        # Should still identify sink node (node with incoming but no outgoing edges)
        assert len(grey_nodes) == 1
        assert sink_node == ("src/scalar.rs", "terminal")


class TestFilenameSanitization:
    """Tests for filename sanitization logic"""

    def test_sanitize_simple_symbol(self):
        """Test sanitization of simple symbol to filename."""
        symbol = "rust-analyzer cargo curve25519-dalek 4.1.3 src/scalar.rs/from_hash()."

        safe_name = symbol.replace("rust-analyzer cargo curve25519-dalek 4.1.3 ", "")
        safe_name = (
            safe_name.replace("::", "_").replace("#", "_").replace("[", "_").replace("]", "_")
        )
        safe_name = safe_name.replace("()", "").replace(".", "").replace(" ", "_").replace("/", "_")

        assert safe_name == "src_scalarrs_from_hash"
        assert "#" not in safe_name
        assert "[" not in safe_name
        assert "/" not in safe_name

    def test_sanitize_impl_symbol(self):
        """Test sanitization of impl block symbol."""
        symbol = (
            "rust-analyzer cargo curve25519-dalek 4.1.3 src/edwards.rs/impl#[EdwardsPoint]double()."
        )

        safe_name = symbol.replace("rust-analyzer cargo curve25519-dalek 4.1.3 ", "")
        safe_name = (
            safe_name.replace("::", "_").replace("#", "_").replace("[", "_").replace("]", "_")
        )
        safe_name = safe_name.replace("()", "").replace(".", "").replace(" ", "_").replace("/", "_")

        assert "#" not in safe_name
        assert "[" not in safe_name
        assert "]" not in safe_name
        assert "::" not in safe_name

    def test_sanitize_trait_impl_symbol(self):
        """Test sanitization of trait implementation symbol."""
        symbol = "rust-analyzer cargo curve25519-dalek 4.1.3 src/edwards.rs/impl#[EdwardsPoint][MultiscalarMul]multiscalar_mul()."

        safe_name = symbol.replace("rust-analyzer cargo curve25519-dalek 4.1.3 ", "")
        safe_name = (
            safe_name.replace("::", "_").replace("#", "_").replace("[", "_").replace("]", "_")
        )
        safe_name = safe_name.replace("()", "").replace(".", "").replace(" ", "_").replace("/", "_")

        # Should not contain any special characters
        assert all(c.isalnum() or c == "_" for c in safe_name)


class TestProjectPaths:
    """Tests for project path resolution"""

    def test_get_project_root(self):
        """Test that project root is correctly identified."""
        root = get_project_root()

        # Should be a Path object
        assert isinstance(root, Path)

        # Should contain expected project structure
        assert (root / "src").exists()
        assert (root / "data").exists()
        assert (root / "pyproject.toml").exists()
        assert (root / "tests").exists()

    def test_project_root_has_expected_files(self):
        """Test that project root contains key data files."""
        root = get_project_root()

        # Check for important data files
        assert (root / "data" / "curve25519-dalek-public-api.json").exists()
        assert (root / "data" / "index_scip_libsignal_deps.json").exists()


class TestSymbolExtraction:
    """Tests for symbol extraction from SCIP JSON"""

    def test_search_curve25519_symbols_from_json(self, tmp_path):
        """Test extracting curve25519-dalek symbols from SCIP JSON."""
        # Create a minimal SCIP JSON file
        scip_json = tmp_path / "test_scip.json"
        scip_content = """{"symbol":"rust-analyzer cargo curve25519-dalek 4.1.3 src/scalar.rs/from_hash()."}
{"symbol":"rust-analyzer cargo curve25519-dalek 4.1.3 src/edwards.rs/double()."}
{"symbol":"rust-analyzer cargo libsignal 0.1.0 src/lib.rs/func()."}
{"symbol":"rust-analyzer cargo curve25519-dalek 4.1.3 src/constants.rs/BASEPOINT_TABLE"}
"""
        scip_json.write_text(scip_content)

        symbols = search_all_curve25519_symbols(scip_json)

        # Should only include curve25519-dalek symbols ending with ().
        assert len(symbols) == 2
        assert all("curve25519-dalek" in s for s in symbols)
        assert all(s.endswith("().") for s in symbols)

    def test_search_handles_empty_file(self, tmp_path):
        """Test that search handles empty SCIP JSON file."""
        scip_json = tmp_path / "empty_scip.json"
        scip_json.write_text("")

        symbols = search_all_curve25519_symbols(scip_json)

        assert len(symbols) == 0
        assert isinstance(symbols, list)

    def test_search_filters_non_function_symbols(self, tmp_path):
        """Test that search filters out non-function symbols."""
        scip_json = tmp_path / "mixed_scip.json"
        scip_content = """{"symbol":"rust-analyzer cargo curve25519-dalek 4.1.3 src/scalar.rs/Scalar#"}
{"symbol":"rust-analyzer cargo curve25519-dalek 4.1.3 src/scalar.rs/from_hash()."}
{"symbol":"rust-analyzer cargo curve25519-dalek 4.1.3 src/constants.rs/BASEPOINT"}
{"symbol":"rust-analyzer cargo curve25519-dalek 4.1.3 src/edwards.rs/double()."}
"""
        scip_json.write_text(scip_content)

        symbols = search_all_curve25519_symbols(scip_json)

        # Should only get function symbols (ending with ().)
        assert len(symbols) == 2
        assert all(s.endswith("().") for s in symbols)


class TestEdgeCases:
    """Tests for edge cases and error conditions"""

    def test_parse_node_with_special_characters(self):
        """Test parsing node IDs with various special characters."""
        # Node with generic type parameters (if they appear)
        node_id = "rust-analyzer cargo curve25519-dalek 4.1.3 src/traits.rs/impl#[CompressedRistretto][Identity]identity()."
        result = parse_node_id(node_id)
        assert result is not None
        assert result[1] == "identity"

    def test_extract_from_malformed_dot(self, tmp_path):
        """Test that malformed DOT file doesn't crash."""
        dot_content = """digraph {
    "incomplete node [fillcolor=green
    "rust-analyzer cargo curve25519-dalek 4.1.3 src/test.rs/func()." [fillcolor=lightgray]
"""

        dot_file = tmp_path / "malformed.dot"
        dot_file.write_text(dot_content)

        # Should not crash, even if results are incomplete
        try:
            grey_nodes, sink_node = extract_nodes_from_dot(dot_file)
            # If it doesn't crash, test passes
            assert isinstance(grey_nodes, set)
        except Exception as e:
            pytest.fail(f"Should handle malformed DOT gracefully, but raised: {e}")
