"""
Smart Test Selector

Maps changed source files to the relevant test files.
Defaults to running all tests if no mapping is found or if an error occurs.
"""

import argparse
import json
import logging
import os
import sys
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("test_selector")

# ---------------------------------------------------------------------------
# Mapping rules: source file pattern -> list of test files
# ---------------------------------------------------------------------------
FILE_TO_TEST_MAP: dict[str, list[str]] = {
    "app/user.py": ["tests/test_user.py"],
    "app/payment.py": ["tests/test_payment.py"],
    "app/order.py": ["tests/test_order.py"],
    "app/inventory.py": ["tests/test_inventory.py"],
    "app/__init__.py": ["tests/test_user.py", "tests/test_payment.py", "tests/test_order.py", "tests/test_inventory.py"],
}

# Default fallback when no specific mapping matches
DEFAULT_TEST_PATHS: list[str] = ["tests/"]


def get_test_paths_for_file(changed_file: str) -> list[str]:
    """
    Return the list of test paths associated with a changed source file.
    Falls back to an empty list if the file is not in the mapping.
    """
    normalized = changed_file.replace("\\", "/").strip()
    logger.info("Looking up tests for: %s", normalized)

    # Direct match
    if normalized in FILE_TO_TEST_MAP:
        return FILE_TO_TEST_MAP[normalized]

    # Automatic inference: app/foo.py -> tests/test_foo.py
    if normalized.startswith("app/") and normalized.endswith(".py"):
        basename = os.path.basename(normalized)
        if basename != "__init__.py":
            inferred_test_file = f"tests/test_{basename}"
            if os.path.exists(inferred_test_file):
                logger.info("Auto-inferred test file: %s", inferred_test_file)
                return [inferred_test_file]

    # Fallback: partial match on basename (e.g., user.py -> test_user.py)
    basename = os.path.basename(normalized)
    for source_pattern, test_paths in FILE_TO_TEST_MAP.items():
        if basename in source_pattern:
            return test_paths

    return []


def select_tests(changed_files: list[str]) -> list[str]:
    """
    Given a list of changed file paths, return deduplicated test paths.
    """
    selected: set[str] = set()
    for f in changed_files:
        tests = get_test_paths_for_file(f)
        if tests:
            selected.update(tests)
            logger.info("Mapped '%s' -> %s", f, tests)
        else:
            logger.info("No direct mapping for '%s'", f)

    if not selected:
        logger.warning("No specific mapping found; defaulting to all tests.")
        return DEFAULT_TEST_PATHS

    return sorted(selected)


def main(argv: Optional[list[str]] = None) -> int:
    """
    CLI entry point.
    Accepts a JSON list of changed files via --files or reads from stdin.
    Prints the selected test paths as a JSON list to stdout.
    """
    parser = argparse.ArgumentParser(
        description="Select relevant test files based on changed source files."
    )
    parser.add_argument(
        "--files",
        type=str,
        help='JSON-encoded list of changed file paths, e.g., ["app/user.py"]',
    )
    args = parser.parse_args(argv)

    try:
        if args.files:
            changed_files = json.loads(args.files)
        else:
            # Read from stdin as fallback
            raw = sys.stdin.read().strip()
            changed_files = json.loads(raw) if raw else []

        if not isinstance(changed_files, list):
            raise ValueError("Input must be a JSON list of strings.")

        selected_tests = select_tests(changed_files)

        # Output as JSON list for easy consumption by CI pipeline
        print(json.dumps(selected_tests))
        return 0

    except Exception as exc:
        logger.error("Error during test selection: %s", exc)
        # On any error, default to running all tests so CI does not silently skip testing
        print(json.dumps(DEFAULT_TEST_PATHS))
        return 0  # return 0 so CI still proceeds to run tests


if __name__ == "__main__":
    sys.exit(main())
