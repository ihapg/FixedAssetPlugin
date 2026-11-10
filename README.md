# FixedAssetPlugin

An [InvenTree](https://inventree.org) plugin that adds a **Fixed Asset** parameter to every new Part.

Whenever a Part is created, the plugin attaches the `Fixed Asset` parameter with the value `False`. Users only need to switch it to `True` for parts that are fixed assets, so every part carries the field and none are missed.

## Compatibility

| Plugin version | InvenTree version |
|----------------|-------------------|
| 0.2.x          | 1.2.0 or newer    |
| 0.1.0          | older than 1.2.0  |

InvenTree 1.2.0 replaced the `PartParameter` / `PartParameterTemplate` models with the generic `Parameter` / `ParameterTemplate` models. Version 0.2.0 of this plugin uses the new models and does not work on older InvenTree versions.

## Requirements

- Plugins enabled on the server (`INVENTREE_PLUGINS_ENABLED=True`, or `plugins_enabled: True` in `config.yaml`).
- A parameter template named exactly **`Fixed Asset`**. A checkbox template is recommended.
- **Enable event integration** turned on in the plugin settings. Without it, the plugin is never notified when parts are created.

## Installation

### InvenTree Plugin Manager

1. As a superuser, go to **Admin Center → Plugins → Install Plugin**.
2. Enter `fixed-asset-plugin` as the package name. Optionally, enter a version such as `0.2.0`.
3. Confirm and install.
4. Restart the InvenTree server **and** the background worker.

### plugins.txt

Add this line to your `plugins.txt` file:

```text
fixed-asset-plugin
```

Then run `invoke plugins` and restart the server and the background worker. On Docker:

```bash
docker compose run --rm inventree-server invoke plugins
docker compose restart inventree-server inventree-worker
```

### Command Line

Install the package into the Python environment that runs InvenTree:

```bash
pip install fixed-asset-plugin
```

Then restart the server and the background worker.

## Configuration

1. **Create the parameter template**, if it does not exist yet. Name it `Fixed Asset` and enable the *checkbox* option.
2. **Activate the plugin** in **Admin Center → Plugins**.
3. **Enable event integration** in the plugin settings in the Admin Center.

The plugin has no settings of its own. It looks up the template by name each time a part is created, so you can create or fix the template later without restarting InvenTree.

## Usage

1. Create a new Part, by any method: the web interface, the API, or an import.
2. The `Fixed Asset` parameter is added to the part with the value `False`.
3. Change it to `True` on the parts that are fixed assets.

Notes:

- Parts that already have the parameter are left unchanged, for example when the category copies it.
- Parts that existed before the plugin was installed are not modified.
- Events are processed by the background worker, so the parameter may appear a few seconds after the part is created.
- If the template is missing, the plugin logs `Template 'Fixed Asset' not found` and does nothing.

## Changelog

### 0.2.0

- Support for InvenTree 1.2.0 and newer, which use the generic `Parameter` / `ParameterTemplate` models.
- The template is looked up when each part is created instead of once at startup.
- Removed the unneeded dependency on the `inventree` Python API client.

### 0.1.0

- First release.

## License

MIT. See [LICENSE](LICENSE).
