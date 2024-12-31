# CHANGELOG


## v0.6.0 (2024-12-31)

### Features

- Add get_device method ([#4](https://github.com/alxdrcirilo/apple-health-parser/pull/4),
  [`e19ee06`](https://github.com/alxdrcirilo/apple-health-parser/commit/e19ee06f6fd82b8d44187800fa39699ef1b96202))

* feat: add get_device method

* chore: remove ignore-init-module-imports from ruff section in pyproject.toml


## v0.5.4 (2024-08-17)

### Bug Fixes

- Circular imports in plot subpackage
  ([#3](https://github.com/alxdrcirilo/apple-health-parser/pull/3),
  [`498d384`](https://github.com/alxdrcirilo/apple-health-parser/commit/498d38453055a7eb4ed3de58e800cb9e03f028a7))

### Documentation

- **README**: Fix warning markdown alert
  ([`d2bc78c`](https://github.com/alxdrcirilo/apple-health-parser/commit/d2bc78c672453df63232d8fe220a0d0f4924ce3f))


## v0.5.3 (2024-07-14)

### Bug Fixes

- Body overview_type requires daily mean
  ([`f5cc434`](https://github.com/alxdrcirilo/apple-health-parser/commit/f5cc434199b04dee8021158c1b92d0c4f51be1e8))


## v0.5.2 (2024-07-13)

### Bug Fixes

- **plot**: Replace append_trace with add_trace
  ([`672ef4e`](https://github.com/alxdrcirilo/apple-health-parser/commit/672ef4ec85acaf866006f65b7328e63ace45934c))

### Build System

- **deps-dev**: Bump certifi from 2024.6.2 to 2024.7.4
  ([`d6efbd9`](https://github.com/alxdrcirilo/apple-health-parser/commit/d6efbd91a704a3d9bee0e7d90b945e57cba971d7))

Bumps [certifi](https://github.com/certifi/python-certifi) from 2024.6.2 to 2024.7.4. -
  [Commits](https://github.com/certifi/python-certifi/compare/2024.06.02...2024.07.04)

--- updated-dependencies: - dependency-name: certifi dependency-type: indirect

...

Signed-off-by: dependabot[bot] <support@github.com>

### Documentation

- Mention available flags listing
  ([`15c89ca`](https://github.com/alxdrcirilo/apple-health-parser/commit/15c89ca814f23ada4674bef575d957707a6c8fc4))

### Testing

- Improve coverage
  ([`0ccdb83`](https://github.com/alxdrcirilo/apple-health-parser/commit/0ccdb83ec7a0a149e5d776e3d7dc6aaa9572e8a2))


## v0.5.1 (2024-07-08)

### Bug Fixes

- Source_version optional
  ([`64413f5`](https://github.com/alxdrcirilo/apple-health-parser/commit/64413f591067ae45632a28e2c8c5e689737c3d0a))

Some older data does not include the `sourceVersion` attribute.


## v0.5.0 (2024-07-05)

### Documentation

- **todo**: Mention CHANGELOG.md and LICENSE.md
  ([`6a596db`](https://github.com/alxdrcirilo/apple-health-parser/commit/6a596db4c5078547dd8cf434a0d5648476f3b797))

BREAKING CHANGE: Manually trigger major bump on version zero.

### BREAKING CHANGES

- **todo**: Manually trigger major bump on version zero.


## v0.4.0 (2024-07-05)

### Features

- Add initial features
  ([`9526224`](https://github.com/alxdrcirilo/apple-health-parser/commit/9526224ce279a790f02c5af1e6690facd8093106))

BREAKING CHANGE: The first few features include a loader, parser, and plotting capabilities.

### BREAKING CHANGES

- The first few features include a loader, parser, and plotting capabilities.
