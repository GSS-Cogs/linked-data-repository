# linked-data-repository
A repository to hold and store CSV-Ws, Turtle and other Linked data


### Running the server locally

* clone this repo
* `poetry install`
* `poetry run ./app/server.py`


### Upgrading or adding python packages

* Add required python library to `pyproject.toml` in the `tool.poetry.dependencies`.
* If it's a development only library (e.g `pytest`, `behave` etc) then add it to the `tool.poetry.dev-dependencies` section.
* Run `make` (this will update the lockfile without dragging in any macos only assumptions) then commit your changes.


### Tests

Will run on PR's into develop or master, merges with test fails will not be permitted.

To run tests locally use `poetry run pytest ./tests/* -v` (v is for verbose, you'll want that).

### Releasing Process / Images

A new `gsscogs/linked-data-repository:develop` image will be pushed to dockerhub on commits to the `develop` branch.

A new `gsscogs/linked-data-repository:master` image will **only** be build on **release** of the master branch code.

The convention is to only merge `develop` -> `master` as the immediate precurrsor of an official release of `master` (so both `develop` and `master` remain representative of what's contained in the public dockerhub images).

