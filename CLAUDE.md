# CLAUDE.md

## Default

Refer `./README.md` for the project overview.

## Everytime after finishing code change

### 1. **Run tests**

- Always run the full test suite before considering a task done:
- All tests must pass. Fix any failures before proceeding.

### 2. **Check the current version**

- If the current version in `./setup.py` is not a development version, bump it to the next development version.
  - Versioning convention for development version: `X.Y.Z.dev0`

### 3. **Update `CHANGELOG.md`**

- Add or update the latest version section at the top with what changed under the appropriate heading (`Added`, `Changed`, `Fixed`, `Removed`, etc.).
  - When adding a new version section, add in this format: `[{Current version}] - Unreleased`

### 4. **Update `README.md` if needed**

- Check whether any of the following sections need updating:
  - File/directory structure (if files were added, removed, or renamed)
  - Configuration reference (if `config.yaml` keys changed)
  - Input/output format (if parsing or output behaviour changed)
  - Usage instructions (if CLI interface changed)

## When release version

- Update current development version to the release version in `./setup.py` and `CHANGELOG.md` files.
- Update `Unreleased` to the current date in `YYYY-MM-DD` format in `CHANGELOG.md`.
