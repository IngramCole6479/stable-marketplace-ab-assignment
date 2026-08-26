"""Assign marketplace users to a stable control or treatment experience."""

import hashlib
import json
import sys

from infrai_flags import infrai


def bucket_for(user_id: str, experiment: str) -> int:
    """Return a deterministic bucket from 0 through 99."""
    digest = hashlib.sha256(f"{experiment}:{user_id}".encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") % 100


def assign(user_id: str, experiment: str = "marketplace-checkout") -> dict:
    """Read the treatment percentage and assign one user without storing state."""
    flag = infrai.flags.get_value(experiment)
    treatment_percent = int(flag.get("default_value", 50))
    bucket = bucket_for(user_id, experiment)
    variant = "treatment" if bucket < treatment_percent else "control"
    return {"user_id": user_id, "experiment": experiment, "variant": variant, "bucket": bucket}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python marketplace_assignment.py USER_ID")
    print(json.dumps(assign(sys.argv[1]), sort_keys=True))
