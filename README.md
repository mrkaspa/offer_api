# Installation

## Setup

Setup the project using Poetry for the dependencies management, install the dependencies like this:

```
poetry install
```

## Migrations

Run all the migraitons with alembic

```
poetry run alembic upgrade head
```

## Testing

To ensure everything is ok run:

```
pytest
```
