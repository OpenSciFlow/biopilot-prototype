from __future__ import annotations

import importlib.metadata
import importlib.util
import json
import platform
import sys
from datetime import datetime, timezone


PACKAGES = ["MDAnalysis", "MDAnalysisData", "numpy", "pandas", "matplotlib"]


def package_status(name: str) -> dict[str, object]:
    installed = importlib.util.find_spec(name) is not None
    version: str | None = None
    if installed:
        try:
            version = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            version = None
    return {"name": name, "installed": installed, "version": version}


def main() -> None:
    report = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "python": {
            "version": platform.python_version(),
            "executable": sys.executable,
        },
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
        },
        "packages": [package_status(name) for name in PACKAGES],
    }

    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
