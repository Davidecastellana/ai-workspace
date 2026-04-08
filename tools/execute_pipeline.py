#!/usr/bin/env python3
"""
Pipeline executor: reads a YAML pipeline definition and executes each step strictly.
Claude Code CLI steps are called via `claude -p "prompt"`.
Exit code != 0 on any step halts the entire pipeline.
"""

import sys
import subprocess
import yaml
from pathlib import Path


def execute_pipeline(pipeline_file: str) -> int:
    path = Path(pipeline_file)
    if not path.exists():
        print(f"ERROR: Pipeline file not found: {pipeline_file}", file=sys.stderr)
        return 1

    with open(path) as f:
        pipeline = yaml.safe_load(f)

    name = pipeline.get("name", path.stem)
    steps = pipeline.get("steps", [])

    print(f"\n{'='*60}")
    print(f"Pipeline: {name}")
    print(f"Steps: {len(steps)}")
    print(f"{'='*60}\n")

    for i, step in enumerate(steps, 1):
        step_name = step.get("name", f"step-{i}")
        step_type = step.get("type", "")

        print(f"[{i}/{len(steps)}] {step_name} ({step_type})")

        if step_type == "claude-code":
            prompt = step.get("prompt", "")
            if not prompt:
                print(f"  ERROR: No prompt defined for claude-code step '{step_name}'", file=sys.stderr)
                return 1

            result = subprocess.run(
                ["claude", "-p", prompt, "--allowedTools", "Read,Write,Edit,Bash"],
                capture_output=False,  # let output stream to terminal
            )

            if result.returncode != 0:
                print(f"\n  FAILED (exit {result.returncode}): {step_name}", file=sys.stderr)
                return result.returncode

        elif step_type == "shell":
            command = step.get("command", "")
            if not command:
                print(f"  ERROR: No command defined for shell step '{step_name}'", file=sys.stderr)
                return 1

            result = subprocess.run(command, shell=True)

            if result.returncode != 0:
                print(f"\n  FAILED (exit {result.returncode}): {step_name}", file=sys.stderr)
                return result.returncode

        else:
            print(f"  ERROR: Unknown step type '{step_type}' in step '{step_name}'", file=sys.stderr)
            return 1

        print(f"  OK\n")

    print(f"{'='*60}")
    print(f"Pipeline '{name}' completed successfully.")
    print(f"{'='*60}\n")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 tools/execute_pipeline.py <pipeline.yaml>", file=sys.stderr)
        sys.exit(1)

    sys.exit(execute_pipeline(sys.argv[1]))
