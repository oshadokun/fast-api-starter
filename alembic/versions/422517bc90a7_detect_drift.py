"""detect drift

Revision ID: 422517bc90a7
Revises: 3b9b3c47dbb6
Create Date: 2026-02-27 12:41:57.148078

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '422517bc90a7'
down_revision: Union[str, Sequence[str], None] = '3b9b3c47dbb6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Remove rogue_col introduced outside migration history."""
    with op.batch_alter_table("people") as batch_op:
        batch_op.drop_column("rogue_col")


def downgrade() -> None:
    """Re-add rogue_col for downgrade compatibility."""
    with op.batch_alter_table("people") as batch_op:
        batch_op.add_column(
            sa.Column("rogue_col", sa.TEXT(), nullable=True)
        )