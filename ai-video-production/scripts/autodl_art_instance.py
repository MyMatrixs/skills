#!/usr/bin/env python3
"""Safely inspect and power-cycle the configured AutoDL.Art Pro instance.

Credentials are loaded only from the sibling .env file and are never emitted.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ENV_PATH = SKILL_ROOT / ".env"
API_PREFIX = "/api/v1/adl_dev/dev/instance/pro"


class LifecycleError(RuntimeError):
    """An error safe to display without credentials."""


def load_env(path: Path) -> dict[str, str]:
    if not path.is_file():
        raise LifecycleError(f"Configuration file not found: {path}")

    values: dict[str, str] = {}
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise LifecycleError(f"Invalid configuration line {line_number} in {path.name}")
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")

    required = ("AUTODL_ART_BASE_URL", "AUTODL_ART_TOKEN", "AUTODL_ART_INSTANCE_UUID")
    missing = [key for key in required if not values.get(key)]
    if missing:
        raise LifecycleError(f"Missing required configuration: {', '.join(missing)}")
    return values


def api_request(
    config: dict[str, str], method: str, path: str, payload: dict[str, Any] | None = None
) -> dict[str, Any]:
    base_url = config["AUTODL_ART_BASE_URL"].rstrip("/")
    url = f"{base_url}{path}"
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    request = Request(
        url,
        data=body,
        method=method,
        headers={
            "Authorization": config["AUTODL_ART_TOKEN"],
            "Accept": "application/json",
            **({"Content-Type": "application/json"} if body is not None else {}),
        },
    )
    try:
        with urlopen(request, timeout=30) as response:
            raw_bytes = response.read()
    except HTTPError as exc:
        raise LifecycleError(f"AutoDL.Art API returned HTTP {exc.code}.") from exc
    except URLError as exc:
        raise LifecycleError(f"Could not reach AutoDL.Art API: {exc.reason}") from exc

    result: dict[str, Any] | None = None
    for encoding in ("utf-8", "gb18030"):
        try:
            candidate = json.loads(raw_bytes.decode(encoding))
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
        if isinstance(candidate, dict):
            result = candidate
            break
    if result is None:
        raise LifecycleError("AutoDL.Art API returned an invalid response.")
    if result.get("code") != "Success":
        message = str(result.get("msg") or result.get("message") or "unspecified API error")
        raise LifecycleError(f"AutoDL.Art API rejected the request: {message}")
    return result


def instance_status(config: dict[str, str]) -> str:
    query = urlencode({"instance_uuid": config["AUTODL_ART_INSTANCE_UUID"]})
    result = api_request(config, "GET", f"{API_PREFIX}/status?{query}")
    status = result.get("data")
    if not isinstance(status, str):
        raise LifecycleError("AutoDL.Art API returned an unexpected instance status.")
    return status


def safe_snapshot(config: dict[str, str]) -> dict[str, Any]:
    query = urlencode({"instance_uuid": config["AUTODL_ART_INSTANCE_UUID"]})
    data = api_request(config, "GET", f"{API_PREFIX}/snapshot?{query}").get("data")
    if not isinstance(data, dict):
        raise LifecycleError("AutoDL.Art API returned an unexpected instance snapshot.")
    return {
        "instance_uuid": config["AUTODL_ART_INSTANCE_UUID"],
        "gpu": data.get("snapshot_gpu_alias_name"),
        "region": data.get("region_sign"),
        "ssh_host": data.get("proxy_host"),
        "ssh_port": data.get("ssh_port"),
        "system_disk_gb": round(float(data.get("expand_system_disk_size", 0)) / 1024**3, 1),
    }


def print_json(value: dict[str, Any]) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))


def wait_for_running(config: dict[str, str], timeout_seconds: int, interval_seconds: int) -> None:
    deadline = time.monotonic() + timeout_seconds
    while True:
        status = instance_status(config)
        print_json({"instance_uuid": config["AUTODL_ART_INSTANCE_UUID"], "status": status})
        if status == "running":
            return
        if time.monotonic() >= deadline:
            raise LifecycleError(f"Timed out after {timeout_seconds}s waiting for status 'running'.")
        time.sleep(interval_seconds)


def parser() -> argparse.ArgumentParser:
    command_parser = argparse.ArgumentParser(description=__doc__)
    command_parser.add_argument("--env", type=Path, default=DEFAULT_ENV_PATH, help="local .env path")
    subparsers = command_parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("status", help="show the current platform state")
    subparsers.add_parser("snapshot", help="show a credential-safe instance summary")

    start = subparsers.add_parser("power-on", help="request GPU-mode boot")
    start.add_argument("--wait", action="store_true", help="wait until platform state is running")
    start.add_argument("--timeout", type=int, default=600, help="maximum wait time in seconds")
    start.add_argument("--interval", type=int, default=10, help="status poll interval in seconds")
    start.add_argument("--dry-run", action="store_true", help="show request intent without changing state")

    stop = subparsers.add_parser("power-off", help="request shutdown after all work is safe locally")
    stop.add_argument("--dry-run", action="store_true", help="show request intent without changing state")
    return command_parser


def main() -> int:
    args = parser().parse_args()
    config = load_env(args.env)
    instance_uuid = config["AUTODL_ART_INSTANCE_UUID"]

    if args.command == "status":
        print_json({"instance_uuid": instance_uuid, "status": instance_status(config)})
        return 0
    if args.command == "snapshot":
        print_json(safe_snapshot(config))
        return 0

    if args.command == "power-on":
        payload = {"instance_uuid": instance_uuid, "payload": "gpu"}
        if args.dry_run:
            print_json({"dry_run": True, "method": "POST", "path": f"{API_PREFIX}/power_on", "payload": payload})
            return 0
        api_request(config, "POST", f"{API_PREFIX}/power_on", payload)
        print_json({"instance_uuid": instance_uuid, "requested": "power_on"})
        if args.wait:
            wait_for_running(config, args.timeout, args.interval)
        return 0

    if args.command == "power-off":
        payload = {"instance_uuid": instance_uuid}
        if args.dry_run:
            print_json({"dry_run": True, "method": "POST", "path": f"{API_PREFIX}/power_off", "payload": payload})
            return 0
        api_request(config, "POST", f"{API_PREFIX}/power_off", payload)
        print_json({"instance_uuid": instance_uuid, "requested": "power_off"})
        return 0

    raise AssertionError(f"Unhandled command: {args.command}")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except LifecycleError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(2)
