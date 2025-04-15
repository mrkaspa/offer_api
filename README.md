# Installation

## Setup

Setup the project using Poetry for the dependencies management, install the dependencies like this:

```
poetry install
```

Start the shell with the environment

```
poetry shell
```

## Migrations

Run all the migraitons with alembic

```
poetry run alembic upgrade head
```

## Testing

To ensure everything is ok run:

```
poetry run pytest tests
```

# Other

## Common Alembic commands

```
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply all pending migrations
alembic upgrade head

# Roll back one migration
alembic downgrade -1

# Roll back to a specific migration
alembic downgrade <revision>

# Show current migration
alembic current

# Show migration history
alembic history

# Show pending migrations
alembic history --indicate-current
```
