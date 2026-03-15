from sqlalchemy import inspect, text
from sqlmodel import SQLModel
from app.database.session import engine
from app.database import models  # noqa: F401


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    _apply_runtime_migrations()


def _apply_runtime_migrations():
    inspector = inspect(engine)

    _ensure_columns(
        table_name="city",
        expected_columns={
            "source": "VARCHAR NOT NULL DEFAULT 'seed'",
            "verified": "BOOLEAN NOT NULL DEFAULT 1",
            "image_url": "VARCHAR",
        },
        inspector=inspector,
    )
    _ensure_columns(
        table_name="place",
        expected_columns={
            "source": "VARCHAR NOT NULL DEFAULT 'seed'",
            "verified": "BOOLEAN NOT NULL DEFAULT 1",
        },
        inspector=inspector,
    )
    _ensure_columns(
        table_name="hotel",
        expected_columns={
            "source": "VARCHAR NOT NULL DEFAULT 'seed'",
            "verified": "BOOLEAN NOT NULL DEFAULT 1",
        },
        inspector=inspector,
    )
    _ensure_columns(
        table_name="activity",
        expected_columns={
            "source": "VARCHAR NOT NULL DEFAULT 'seed'",
            "verified": "BOOLEAN NOT NULL DEFAULT 1",
        },
        inspector=inspector,
    )
    _ensure_columns(
        table_name="trip",
        expected_columns={
            "version": "INTEGER NOT NULL DEFAULT 1",
            "locked_by": "VARCHAR",
            "locked_day_number": "INTEGER",
            "locked_at": "TIMESTAMP",
            "organization_id": "INTEGER",
            "created_by": "INTEGER",
        },
        inspector=inspector,
    )
    _ensure_columns(
        table_name="collaborationevent",
        expected_columns={
            "operation_id": "VARCHAR",
            "base_version": "INTEGER",
            "status": "VARCHAR NOT NULL DEFAULT 'applied'",
            "created_at": "TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP",
        },
        inspector=inspector,
    )
    _ensure_default_organization(inspector)


def _ensure_columns(table_name: str, expected_columns: dict[str, str], inspector):
    if not inspector.has_table(table_name):
        return

    existing_columns = {column["name"] for column in inspector.get_columns(table_name)}
    with engine.begin() as connection:
        for column_name, column_type in expected_columns.items():
            if column_name in existing_columns:
                continue
            connection.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"))


def _ensure_default_organization(inspector):
    if not inspector.has_table("organization") or not inspector.has_table("trip"):
        return

    with engine.begin() as connection:
        org_row = connection.execute(text("SELECT id FROM organization ORDER BY id LIMIT 1")).first()
        if org_row:
            org_id = org_row[0]
        else:
            connection.execute(
                text(
                    "INSERT INTO organization (name, slug, created_at) VALUES ('Default Agency', 'default-agency', CURRENT_TIMESTAMP)"
                )
            )
            org_id = connection.execute(text("SELECT id FROM organization WHERE slug = 'default-agency'")).first()[0]

        connection.execute(text("UPDATE trip SET organization_id = :org_id WHERE organization_id IS NULL"), {"org_id": org_id})
