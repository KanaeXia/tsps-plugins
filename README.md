# TSPS plugins

This repository publishes plugins for the [RSPS.app Plugin Hub](https://rsps.app/plugins/). Download a release ZIP and upload it from your server's **Plugins** panel. The server loads the plugin on its next start.

## Package layout

Each plugin lives in `plugins/<id>/`. Its format-1 ZIP contains `plugin.json` and one CommonJS entry named `<name>.plugin.js` at the ZIP root. The manifest includes the package ID, TSPS plugin name, version and description. The entry exports the same plugin name and a `register(api)` function. ZIPs and their individual files are limited to 1 MiB.

## Publish a release

1. Set the version in the plugin manifest and build the ZIP with `python3 scripts/package-plugin.py <id>`.
2. Publish the ZIP as a GitHub Release asset. Use the tag `<id>-v<version>` and attach `dist/<id>-<version>.zip`. GitHub's automatic source archive contains the whole repository.
3. Update `catalogue.json` with the published version. The Hub reads this index from `main` and builds the release download URL from the ID and version.
