import argparse
import sys
from typing import Dict, Any, List

from pygments.lexers import diff

# Exit Codes
EXIT_NO_DRIFT = 0
EXIT_DRIFT_FOUND = 2
EXIT_FILE_ERROR = 10
EXIT_SCHEMA_ERROR = 11
EXIT_INTERNAL_ERROR = 99


# ---------- CLI ----------

def parse_args():
    parser = argparse.ArgumentParser(
        description="Compare two configuration files and report differences."
    )

    parser.add_argument(
        "--baseline",
        required=True,
        help="Path to baseline JSON config"
    )

    parser.add_argument(
        "--target",
        required=True,
        help="Path to target JSON config"
    )

    parser.add_argument(
        "--output-csv",
        help="Write drift report to CSV file"
    )

    parser.add_argument(
        "--output-json",
        help="Write drift report to JSON file"
    )

    parser.add_argument(
        "--fail-on-drift",
        action="store_true",
        help="Exit with code 1 if drift is detected"
    )

    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress console output"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Verbose output"
    )

    return parser.parse_args()


# ---------- Load & Normalize ----------

def load_config(path: str) -> Dict[str, Any]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: File not found: {path}", file=sys.stderr)
        sys.exit(2)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {path}: {e}", file=sys.stderr)
        sys.exit(2)

    if not isinstance(data, dict):
        print(f"ERROR: Root JSON must be an object in {path}", file=sys.stderr)
        sys.exit(2)

    return data


def flatten_config(
        data: Dict[str, Any],
        parent_key: str = "",
        sep: str = "."
) -> Dict[str, Any]:
    items = {}

    for key, value in data.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key

        if isinstance(value, dict):
            items.update(flatten_config(value, new_key, sep))
        else:
            items[new_key] = value

    return items

# ---------- Comparison ----------

def compare_configs(flat_a: dict, flat_b: dict) -> dict:
    """
    Compare two flattened configs.
    Returns differences grouped by type.
    """
    result = {
        "only_in_a": [],
        "only_in_b": [],
        "different_values": []
    }

    keys_a = set(flat_a.keys())
    keys_b = set(flat_b.keys())

    # Keys only in A
    for key in keys_a - keys_b:
        result["only_in_a"].append(key)

    # Keys only in B
    for key in keys_b - keys_a:
        result["only_in_b"].append(key)

    # Keys in both but with different values
    for key in keys_a & keys_b:
        if flat_a[key] != flat_b[key]:
            result["different_values"].append({
                "key": key,
                "value_a": flat_a[key],
                "value_b": flat_b[key],
            })

    return result

def diff_has_changes(diff: Dict) -> bool:
    return(
        bool(diff.get("only_in_a")) or
        bool(diff.get("only_in_b")) or
        bool(diff.get("different_values"))
    )

# ---------- Output ----------

def export_results(
    records: List[Dict[str, Any]],
    args
):
    pass


def print_summary(
    records: List[Dict[str, Any]],
    args
):
    pass

def print_report(diff: dict) -> None:
    """
    Print a human-readable comparison report.
    """
    if not any(diff.values()):
        print("No differences found.")
        return

    if diff["only_in_a"]:
        print("\nKeys only in A:")
        for key in sorted(diff["only_in_a"]):
            print(f"  - {key}")

    if diff["only_in_b"]:
        print("\nKeys only in B:")
        for key in sorted(diff["only_in_b"]):
            print(f"  - {key}")

    if diff["different_values"]:
        print("\nKeys with different values:")
        for item in diff["different_values"]:
            print(f"  - {item['key']}")
            print(f"      A: {item['value_a']}")
            print(f"      B: {item['value_b']}")

import csv
import json

def export_csv(diff, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["section", "key", "baseline", "target"])

        # Keys only in A
        for key in diff.get("only_in_a", []):
            writer.writerow(["only_in_a", key, "", ""])

        # Keys only in B
        for key in diff.get("only_in_b", []):
            writer.writerow(["only_in_b", key, "", ""])

        # Keys with different values
        for change in diff.get("different_values", []):
            writer.writerow([
                "different_values",
                change["key"],
                json.dumps(change["value_a"]),
                json.dumps(change["value_b"]),
            ])

def export_json(diff, path):
    """
    Write drift report to JSON.
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(diff, f, indent=2)

# ---------- Exit ----------

def exit_with_code(
    records: List[Dict[str, Any]],
    args
):
    sys.exit(0)

def diff_has_changes(diff) ->bool:
    """
    Return True if configuration drift exists
    """
    return bool(
        diff.get("only_in_a")
        or diff.get("only_in_b")
        or diff.get("different_values")
    )

def handle_output(diff, args):
    """
    Handle all user-facing output and exports
    """
    if not args.quiet:
        print_report(diff)

    if args.output_csv:
        export_csv(diff, args.output_csv)

    if args.output_json:
        export_json(diff, args.output_json)

def evaluate_exit_code(diff):
    """
    Determine exit code based on drift detection.
    """
    if diff_has_changes(diff):
        return 1
    return 0

# ---------- Main ----------

def main():
    try:
        args = parse_args()
        baseline = load_config(args.baseline)
        target = load_config(args.target)

        diff = compare_configs(baseline, target)

        handle_output(diff, args)

        exit_code = evaluate_exit_code(diff)
        sys.exit(exit_code)

    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        sys.exit(EXIT_FILE_ERROR)

    except ValueError as e:
        print(f"ERROR: {e}")
        sys.exit(EXIT_SCHEMA_ERROR)

    except Exception as e:
        print(f"ERROR: Unexpected failure: {e}")
        sys.exit(EXIT_INTERNAL_ERROR)


if __name__ == "__main__":
    main()


