"""Create estimates table.

Revision ID: 001
Create Date: 2026-03-01
"""

from alembic import op
import sqlalchemy as sa

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "estimates",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("square_footage", sa.Float(), nullable=False),
        sa.Column("bedrooms", sa.Integer(), nullable=False),
        sa.Column("bathrooms", sa.Float(), nullable=False),
        sa.Column("year_built", sa.Integer(), nullable=False),
        sa.Column("lot_size", sa.Float(), nullable=False),
        sa.Column("distance_to_city_center", sa.Float(), nullable=False),
        sa.Column("school_rating", sa.Float(), nullable=False),
        sa.Column("predicted_price", sa.Float(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_estimates_created_at", "estimates", ["created_at"])


def downgrade() -> None:
    op.drop_index("ix_estimates_created_at", table_name="estimates")
    op.drop_table("estimates")
