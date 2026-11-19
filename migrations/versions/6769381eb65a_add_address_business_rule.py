"""add address business rule

Revision ID: 6769381eb65a
Revises: 2e09989f61c4
Create Date: 2026-11-19 10:20:30.975259

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6769381eb65a'
down_revision = '2e09989f61c4'
branch_labels = None
depends_on = None

def upgrade():
    op.create_check_constraint(
        "ck_orders_address_by_order_type",
        "orders",
        """
        (
            (order_type = 'WALK_IN' AND address IS NULL)
            OR
            (
                order_type = 'DELIVERY'
                AND address IS NOT NULL
                AND length(trim(address)) > 0
            )
        )
        """,
    )


def downgrade():
    op.drop_constraint(
        "ck_orders_address_by_order_type",
        "orders",
        type_="check",
    )
