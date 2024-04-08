# Changelog

## [Unreleased]

### Added

- ...

### Fixed

- ...

### Changed

- ...

## [0.2.0] - 2024-04-08

### Added

- Provided [Readme](README.md)
- Added new endpoints as well as their unit testing.
  - `/v1/disk`
  - `/v1/net`
- Provided GitHub `bug report` and `feature request` templates for workflow.

### Changed

- Fixed version `0.1.0` Changelog release date
- Updated endpoints:
  - `/v1/cpuavg` to `/v1/cpu`
  - `/v1/raminfo` to `/v1/mem`
    - Now memory unit can be specified instead of fixed to `kB`
- Updated default logging level from `DEBUG` to `INFO`

## [0.1.0] - 2024-03-30

### Added

- `CPU Avg Load` endpoint at `/v1/cpuavg`
- `Memory` status endpoint at `/v1/raminfo`
- Unit tests for all the above endpoints
- `amd64` and `linux/arm64` builds (docker buildx) provided in dockerfile
