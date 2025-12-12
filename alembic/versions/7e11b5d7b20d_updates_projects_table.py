"""updates projects table

Revision ID: 7e11b5d7b20d
Revises: a14a1b3857ea
Create Date: 2025-12-12 04:50:49.390745

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '7e11b5d7b20d'
down_revision: Union[str, Sequence[str], None] = 'a14a1b3857ea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# define enum once (important!)
visibility_enum = sa.Enum(
    'PUBLIC',
    'UNLISTED',
    name='visibility_status'
)


def upgrade() -> None:
    """Upgrade schema."""
    # Create enum type FIRST
    visibility_enum.create(op.get_bind(), checkfirst=True)

    # Now add columns
    op.add_column(
        'projects',
        sa.Column('visibility', visibility_enum, nullable=True)
    )
    op.add_column(
        'projects',
        sa.Column('analytics', postgresql.JSONB(astext_type=sa.Text()), nullable=True)
    )
    op.add_column(
        'projects',
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True)
    )
    op.add_column(
        'projects',
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('projects', 'updated_at')
    op.drop_column('projects', 'created_at')
    op.drop_column('projects', 'analytics')
    op.drop_column('projects', 'visibility')

    # Drop enum type LAST
    visibility_enum.drop(op.get_bind(), checkfirst=True)
