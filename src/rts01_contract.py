"""Run the public RTS-01 synthetic queue-to-readback contract.

The runner is deliberately local and deterministic. It does not invoke a
shell, contact a network service, or read credentials.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any


STAGES = [
    "queue",
    "claim",
    "bounded_execution",
    "cas_writeback",
    "remote_readback",
]
TASK_ID = "synthetic-rts01-task-001"
CORRELATION_ID = "synthetic-rts01-trace-001"
EXECUTOR_ID = "synthetic-runner"
OPERATION = "fixture.transform"


def _canonical(value: dict[str, Any]) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _atomic_write(path: Path, payload: bytes) -> None:
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_bytes(payload)
    os.replace(temporary, path)


def _cas_write(path: Path, payload: bytes) -> str:
    digest = hashlib.sha256(payload).hexdigest()
    destination = path / f"{digest}.json"
    if destination.exists():
        if destination.read_bytes() != payload:
            raise ValueError("CAS collision with different content")
    else:
        _atomic_write(destination, payload)
    return digest


def run_contract(root: Path) -> dict[str, Any]:
    """Execute the five public synthetic stages under *root*.

    Only fixture data is used. The returned evidence is safe to print and
    contains no absolute paths or secret material.
    """

    root.mkdir(parents=True, exist_ok=True)
    queue = root / "queue"
    results = root / "results"
    remote = root / "remote-mirror" / "results"
    for directory in (queue, results, remote):
        directory.mkdir(parents=True, exist_ok=True)

    task = {
        "task_id": TASK_ID,
        "correlation_id": CORRELATION_ID,
        "status": "queued",
        "route": "synthetic",
        "operation": OPERATION,
    }
    task_file = queue / f"{TASK_ID}.json"
    _atomic_write(task_file, _canonical(task))
    queued = json.loads(task_file.read_text(encoding="utf-8"))
    queue_ok = queued["status"] == "queued" and queued["task_id"] == TASK_ID

    claimed = {**queued, "status": "claimed", "executor_id": EXECUTOR_ID}
    _atomic_write(task_file, _canonical(claimed))
    claim_ok = (
        json.loads(task_file.read_text(encoding="utf-8"))["status"] == "claimed"
        and claimed["executor_id"] == EXECUTOR_ID
    )

    if OPERATION != "fixture.transform":
        raise ValueError("unsupported operation")
    bounded_result = {"value": "RTS-01", "transformed": True}
    bounded_ok = bounded_result["transformed"] is True

    result = {
        "schema": "rts01.synthetic.result.v1",
        "task_id": TASK_ID,
        "correlation_id": CORRELATION_ID,
        "executor_id": EXECUTOR_ID,
        "operation": OPERATION,
        "output": bounded_result,
        "status": "verified",
    }
    payload = _canonical(result)
    digest = _cas_write(results, payload)
    second_digest = _cas_write(results, payload)
    cas_ok = digest == second_digest and (results / f"{digest}.json").read_bytes() == payload

    remote_file = remote / f"{digest}.json"
    _atomic_write(remote_file, payload)
    remote_result = json.loads(remote_file.read_text(encoding="utf-8"))
    remote_ok = remote_result["correlation_id"] == CORRELATION_ID and _canonical(remote_result) == payload

    status = {
        "queue": queue_ok,
        "claim": claim_ok,
        "bounded_execution": bounded_ok,
        "cas_writeback": cas_ok,
        "remote_readback": remote_ok,
    }
    if not all(status.values()):
        raise AssertionError(f"synthetic contract failed: {status}")

    return {
        "contract": "RTS-01 synthetic queue-to-readback",
        "stages": STAGES,
        "status": status,
        "task_id": TASK_ID,
        "correlation_id": CORRELATION_ID,
        "claim": {"executor_id": EXECUTOR_ID},
        "bounded_execution": {"bounded": bounded_ok, "operation": OPERATION},
        "cas_writeback": {"result_sha256": digest, "idempotent": cas_ok},
        "remote_readback": {"matches_correlation": remote_ok},
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workdir", type=Path, default=Path(".rts01-synthetic-run"))
    args = parser.parse_args()
    print(json.dumps(run_contract(args.workdir), indent=2, sort_keys=True))
