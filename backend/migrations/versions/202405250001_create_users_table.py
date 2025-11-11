"""Create users table placeholder."""

def upgrade() -> None:  # pragma: no cover - placeholder migration
    """Document expected SQLAlchemy migration."""
    # In Phase 2 Build we rely on in-memory stores. The final implementation
    # will define SQLModel metadata and actual Alembic operations.
    pass


def downgrade() -> None:  # pragma: no cover - placeholder migration
    pass
