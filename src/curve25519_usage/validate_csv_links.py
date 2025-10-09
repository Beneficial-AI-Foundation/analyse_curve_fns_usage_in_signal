#!/usr/bin/env python3
"""
Validate GitHub links in the curve25519_functions.csv file.

This script checks each GitHub link in the CSV to ensure it doesn't return a 404 error.
It reports any broken links and provides a summary of the validation results.

Uses parallel processing to speed up validation.
"""

import csv
from pathlib import Path
from typing import Tuple
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading


def check_url(url: str, timeout: int = 10) -> Tuple[bool, int, str]:
    """
    Check if a URL is accessible.

    Args:
        url: The URL to check
        timeout: Request timeout in seconds

    Returns:
        Tuple of (success, status_code, error_message)
    """
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            status_code = response.getcode()
            return (status_code == 200, status_code, "")
    except urllib.error.HTTPError as e:
        return (False, e.code, str(e))
    except urllib.error.URLError as e:
        return (False, 0, f"URL Error: {e.reason}")
    except Exception as e:
        return (False, 0, f"Error: {str(e)}")


def check_link_with_metadata(
    function_name: str, link: str, index: int, total: int
) -> Tuple[str, str, bool, int, str]:
    """
    Check a single link and return results with metadata.

    Args:
        function_name: Name of the function
        link: URL to check
        index: Index of this link (1-based)
        total: Total number of links

    Returns:
        Tuple of (function_name, link, success, status_code, error_msg)
    """
    success, status_code, error_msg = check_url(link)
    return (function_name, link, success, status_code, error_msg)


def validate_csv_links(csv_file: Path, max_workers: int = 10) -> None:
    """
    Validate all GitHub links in the CSV file using parallel processing.

    Args:
        csv_file: Path to the CSV file
        max_workers: Maximum number of parallel workers
    """
    print(f"Reading CSV file: {csv_file}")

    # Read all links from the CSV
    links_to_check = []
    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            link = row.get("link", "").strip()
            function_name = row.get("function_name", "")
            if link:  # Only check non-empty links
                links_to_check.append((function_name, link))

    total_links = len(links_to_check)
    print(f"Found {total_links} links to validate")
    print(f"Using {max_workers} parallel workers\n")

    # Validate links in parallel
    valid_links = []
    broken_links = []
    completed = 0
    lock = threading.Lock()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_link = {
            executor.submit(check_link_with_metadata, func_name, link, i, total_links): (
                func_name,
                link,
            )
            for i, (func_name, link) in enumerate(links_to_check, 1)
        }

        # Process results as they complete
        for future in as_completed(future_to_link):
            func_name, link = future_to_link[future]
            try:
                function_name, url, success, status_code, error_msg = future.result()

                with lock:
                    completed += 1
                    print(f"[{completed}/{total_links}] Checking: {function_name}")
                    print(f"  URL: {url}")

                    if success:
                        print(f"  ✓ OK (Status: {status_code})")
                        valid_links.append((function_name, url))
                    else:
                        print(f"  ✗ FAILED (Status: {status_code})")
                        if error_msg:
                            print(f"  Error: {error_msg}")
                        broken_links.append((function_name, url, status_code, error_msg))
            except Exception as e:
                with lock:
                    completed += 1
                    print(f"[{completed}/{total_links}] Exception checking: {func_name}")
                    print(f"  Error: {e}")
                    broken_links.append((func_name, link, 0, str(e)))

    # Print summary
    print("\n" + "=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)
    print(f"Total links checked: {total_links}")
    print(
        f"Valid links: {len(valid_links)} ({len(valid_links) * 100 // total_links if total_links else 0}%)"
    )
    print(
        f"Broken links: {len(broken_links)} ({len(broken_links) * 100 // total_links if total_links else 0}%)"
    )

    if broken_links:
        print("\n" + "=" * 80)
        print("BROKEN LINKS DETAILS")
        print("=" * 80)
        for function_name, link, status_code, error_msg in broken_links:
            print(f"\nFunction: {function_name}")
            print(f"  URL: {link}")
            print(f"  Status: {status_code}")
            if error_msg:
                print(f"  Error: {error_msg}")
    else:
        print("\n✓ All links are valid!")


def main():
    """Main function."""
    base_dir = Path(__file__).parent.parent.parent
    csv_file = base_dir / "outputs" / "curve25519_functions.csv"

    if not csv_file.exists():
        print(f"Error: CSV file not found: {csv_file}")
        return 1

    try:
        # Use 10 parallel workers for faster validation
        validate_csv_links(csv_file, max_workers=10)
        return 0
    except KeyboardInterrupt:
        print("\n\nValidation interrupted by user")
        return 1
    except Exception as e:
        print(f"\nError during validation: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
