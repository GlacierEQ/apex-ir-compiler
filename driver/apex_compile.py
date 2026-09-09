import argparse
import json
import subprocess
import sys
import os
from typing import List, Dict, Any

def parse_dsl(input_text: str) -> List[Dict[str, Any]]:
    tokens: List[Dict[str, Any]] = []
    for line in input_text.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if parts[0] == "CHANGESET":
            if len(parts) < 3:
                raise ValueError("CHANGESET needs op-id and target")
            target = parts[2].replace("target=", "")
            tokens.append({"type": "Changeset", "op_id": parts[1], "target": target})
        elif parts[0] == "ACTION":
            if len(parts) < 3:
                raise ValueError("ACTION needs action_type and params")
            idx = line.find("params=")
            if idx == -1:
                raise ValueError("ACTION missing params=")
            params = line[idx+7:]
            tokens.append({"type": "Action", "action_type": parts[1], "params": params})
        elif parts[0] == "COMMIT":
            tokens.append({"type": "Commit"})
        elif parts[0] == "ABORT":
            reason = " ".join(parts[1:]) if len(parts) > 1 else ""
            tokens.append({"type": "Abort", "reason": reason})
        else:
            raise ValueError(f"Invalid line format: {line}")
    return tokens

def verify_dsl(tokens: List[Dict[str, Any]]) -> None:
    if not tokens:
        raise ValueError("Empty DSL")
    has_changeset = False
    action_count = 0
    terminated = False
    for t in tokens:
        if terminated:
            if t["type"] in ("Commit", "Abort"):
                raise ValueError("Multiple COMMIT/ABORT")
            raise ValueError("Token after COMMIT/ABORT")
        if t["type"] == "Changeset":
            has_changeset = True
        elif t["type"] == "Action":
            if not has_changeset:
                raise ValueError("ACTION before CHANGESET")
            action_count += 1
        elif t["type"] in ("Commit", "Abort"):
            if not has_changeset:
                raise ValueError("Termination before CHANGESET")
            terminated = True
            if t["type"] == "Abort" and action_count == 0:
                raise ValueError("ABORT with no ACTION is a no-op changeset")
    if not terminated:
        raise ValueError("Missing COMMIT or ABORT")
    if action_count == 0:
        raise ValueError("CHANGESET without ACTIONs")

def main() -> None:
    parser = argparse.ArgumentParser(prog="apex_compile")
    parser.add_argument("command", choices=["parse", "emit-mlir", "verify"])
    parser.add_argument("--file", type=str, help="Input file")
    args = parser.parse_args()

    input_text = ""
    if args.file:
        with open(args.file, "r") as f:
            input_text = f.read()
    else:
        input_text = sys.stdin.read()

    if args.command == "parse":
        try:
            tokens = parse_dsl(input_text)
            print(json.dumps(tokens, indent=2))
        except ValueError as e:
            print(f"ParseError: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.command == "verify":
        try:
            tokens = parse_dsl(input_text)
            verify_dsl(tokens)
            print("\033[92mVerification passed.\033[0m")
        except ValueError as e:
            print(f"\033[91mVerifyError: {e}\033[0m", file=sys.stderr)
            sys.exit(1)
    elif args.command == "emit-mlir":
        rust_bin = os.path.join(os.path.dirname(__file__), "..", "frontend", "target", "release", "apex-frontend")
        if os.path.exists(rust_bin):
            result = subprocess.run([rust_bin], input=input_text, text=True, capture_output=True)
            if result.returncode != 0:
                print(result.stderr, file=sys.stderr)
                sys.exit(result.returncode)
            print(result.stdout)
        else:
            print(f"Rust binary not found at {rust_bin}. Please run 'cargo build --release' in frontend/", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
