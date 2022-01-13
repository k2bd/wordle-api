# Wordle API
[![CI](https://github.com/k2bd/wordle-api/actions/workflows/ci.yml/badge.svg)](https://github.com/k2bd/wordle-api/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/k2bd/wordle-api/branch/main/graph/badge.svg?token=4LB5LSD1AT)](https://codecov.io/gh/k2bd/wordle-api)

A simple stateless API for daily or on-demand random wordle puzzles of variable size, for example for bot competitions.

You can hit the `/daily` and `/random` endpoints to get the results of single guesses. Set a seed for the `/random` endpoint to be able to solve a puzzle in steps.

## Developing

Install [Poetry](https://python-poetry.org/) and `poetry install` the project

### Useful Commands

Note: if Poetry is managing a virtual environment for you, you may need to use `poetry run poe` instead of `poe`

- `poe autoformat` - Autoformat code
- `poe lint` - Linting
- `poe test` - Run Tests
- `poe local-server` - Run your API locally

While the local server is running, you can see API docs at `http://localhost:8011/docs` or `http://localhost:8011/redoc`, and can get the OpenAPI spec at `http://localhost:8011/openapi.json`.

### Deployment

Release a new version by manually running the release action on GitHub with a 'major', 'minor', or 'patch' version bump selected.
This will create an push a new semver tag of the format `v1.2.3`, and also update the appropriate major version tag (`v1`, `v2`, ...).

Updating the major version tags will cause Cloud Build to create or update that version's deployment automatically and host it at e.g. `v1.(your configured domain)`. You may need to configure your domain's DNS if you're creating an endpoint for a new major version and you use an external provider. See the domain mappings page linked [here](https://cloud.google.com/run/docs/mapping-custom-domains#map) for instructions.
