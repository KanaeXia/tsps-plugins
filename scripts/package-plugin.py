import argparse
import json
import re
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]


def package_plugin(plugin_id):
    if not re.fullmatch(r"[a-z][a-z0-9-]{0,63}", plugin_id):
        raise ValueError("Invalid plugin ID")
    directory = ROOT / "plugins" / plugin_id
    manifest_path = directory / "plugin.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if (
        manifest["format"] != 1
        or manifest["id"] != plugin_id
        or not re.fullmatch(r"[A-Za-z][A-Za-z0-9]{0,63}", manifest["name"])
        or not re.fullmatch(r"[0-9]{1,6}\.[0-9]{1,6}\.[0-9]{1,6}", manifest["version"])
        or not isinstance(manifest["description"], str)
        or len(manifest["description"]) > 500
    ):
        raise ValueError("Invalid plugin manifest")

    output = ROOT / "dist" / f'{plugin_id}-{manifest["version"]}.zip'
    source_path = directory / f'{manifest["name"]}.plugin.js'
    files = {file.name: file.read_bytes() for file in (manifest_path, source_path)}
    if any(not data or len(data) > 1024 * 1024 for data in files.values()):
        raise ValueError("Each plugin file must be between 1 byte and 1 MiB")
    output.parent.mkdir(exist_ok=True)
    with ZipFile(output, "w") as archive:
        for name, data in files.items():
            archive.writestr(ZipInfo(name), data, ZIP_DEFLATED)
    if output.stat().st_size > 1024 * 1024:
        output.unlink()
        raise ValueError("Plugin ZIP must be at most 1 MiB")
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build an importable TSPS plugin ZIP.")
    parser.add_argument("plugin_id")
    print(package_plugin(parser.parse_args().plugin_id).relative_to(ROOT))
