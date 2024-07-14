# CHANGELOG

## v0.5.3 (2024-07-14)

### Fix

* fix: body overview_type requires daily mean ([`f5cc434`](https://github.com/alxdrcirilo/apple-health-parser/commit/f5cc434199b04dee8021158c1b92d0c4f51be1e8))

## v0.5.2 (2024-07-13)

### Build

* build(deps-dev): bump certifi from 2024.6.2 to 2024.7.4

Bumps [certifi](https://github.com/certifi/python-certifi) from 2024.6.2 to 2024.7.4.
- [Commits](https://github.com/certifi/python-certifi/compare/2024.06.02...2024.07.04)

---
updated-dependencies:
- dependency-name: certifi
  dependency-type: indirect
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`d6efbd9`](https://github.com/alxdrcirilo/apple-health-parser/commit/d6efbd91a704a3d9bee0e7d90b945e57cba971d7))

### Documentation

* docs: mention available flags listing ([`15c89ca`](https://github.com/alxdrcirilo/apple-health-parser/commit/15c89ca814f23ada4674bef575d957707a6c8fc4))

### Fix

* fix(plot): replace append_trace with add_trace ([`672ef4e`](https://github.com/alxdrcirilo/apple-health-parser/commit/672ef4ec85acaf866006f65b7328e63ace45934c))

### Test

* test: improve coverage ([`0ccdb83`](https://github.com/alxdrcirilo/apple-health-parser/commit/0ccdb83ec7a0a149e5d776e3d7dc6aaa9572e8a2))

### Unknown

* Merge pull request #1 from alxdrcirilo/dependabot/pip/certifi-2024.7.4

build(deps-dev): bump certifi from 2024.6.2 to 2024.7.4 ([`66b54ce`](https://github.com/alxdrcirilo/apple-health-parser/commit/66b54cea1d7bf294a54ae5cd62e31e54b9026ead))

## v0.5.1 (2024-07-08)

### Fix

* fix: source_version optional

Some older data does not include the `sourceVersion` attribute. ([`64413f5`](https://github.com/alxdrcirilo/apple-health-parser/commit/64413f591067ae45632a28e2c8c5e689737c3d0a))

## v0.5.0 (2024-07-05)

### Breaking

* docs(todo): mention CHANGELOG.md and LICENSE.md

BREAKING CHANGE: Manually trigger major bump on version zero. ([`6a596db`](https://github.com/alxdrcirilo/apple-health-parser/commit/6a596db4c5078547dd8cf434a0d5648476f3b797))

## v0.4.0 (2024-07-05)

### Breaking

* feat: add initial features

BREAKING CHANGE: The first few features include a loader, parser, and plotting capabilities. ([`9526224`](https://github.com/alxdrcirilo/apple-health-parser/commit/9526224ce279a790f02c5af1e6690facd8093106))

### Unknown

* Initial commit ([`a82d438`](https://github.com/alxdrcirilo/apple-health-parser/commit/a82d4384e5cc5a5a1c864d42cf3a1a751a9f6bb9))
