#!/usr/bin/env python3
"""
Pipeline router — reads routing.yaml and fires the right pipelines
based on which files changed in the last git commit.

Flow:
  1. Get changed files from git
  2. Load routing.yaml
  3. Match changed files against route watch patterns
  4. Execute matched pipelines (deduped, priority-ordered)
"""

import subprocess
import sys
import fnmatch
import yaml
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent


def get_changed_files() -> list[str]:
    """Get files changed in the last commit."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        # First commit — get all tracked files
        result = subprocess.run(
            ["git", "ls-files"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True
        )
    return [f.strip() for f in result.stdout.splitlines() if f.strip()]


def matches_pattern(filepath: str, pattern: str) -> bool:
    """Check if a filepath matches a glob pattern."""
    return fnmatch.fnmatch(filepath, pattern)


def load_routing_table() -> list[dict]:
    routing_file = REPO_ROOT / "routing.yaml"
    if not routing_file.exists():
        print("ERROR: routing.yaml not found", file=sys.stderr)
        sys.exit(1)

    with open(routing_file) as f:
        data = yaml.safe_load(f)

    return data.get("routes", [])


def route(changed_files: list[str], routes: list[dict]) -> list[str]:
    """Return ordered list of pipeline files to execute (deduped)."""
    matched = []
    seen = set()

    # Sort: high-priority routes first (no priority field = high)
    def priority_key(route):
        p = route.get("priority", "high")
        return {"high": 0, "normal": 1, "low": 2}.get(p, 1)

    sorted_routes = sorted(routes, key=priority_key)

    for route in sorted_routes:
        pattern = route["watch"]
        pipeline = route.get("pipeline")

        if not pipeline:
            continue

        for changed in changed_files:
            if matches_pattern(changed, pattern):
                if pipeline not in seen:
                    matched.append(pipeline)
                    seen.add(pipeline)
                    print(f"  Match: '{changed}' → {route['name']} → {pipeline}")
                break

    return matched


def main():
    print("\n=== Router ===")

    changed = get_changed_files()
    if not changed:
        print("No changed files detected. Nothing to route.")
        return 0

    print(f"Changed files: {changed}")

    routes = load_routing_table()
    pipelines = route(changed, routes)

    if not pipelines:
        print("No matching pipelines for changed files.")
        return 0

    print(f"\nPipelines to execute: {pipelines}\n")

    # Import and run each pipeline
    sys.path.insert(0, str(REPO_ROOT / "tools"))
    from execute_pipeline import execute_pipeline

    for pipeline_file in pipelines:
        print(f"\n--- Running: {pipeline_file} ---")
        exit_code = execute_pipeline(pipeline_file)
        if exit_code != 0:
            print(f"\nPipeline FAILED: {pipeline_file} (exit {exit_code})", file=sys.stderr)
            return exit_code

    return 0


if __name__ == "__main__":
    sys.exit(main())
