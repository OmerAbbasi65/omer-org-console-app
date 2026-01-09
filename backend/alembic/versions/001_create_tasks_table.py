"""create tasks table

Revision ID: 001
Revises:
Create Date: 2026-01-09

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects.postgresql import UUID, ARRAY

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'task',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('priority', sa.String(10), nullable=False, server_default='medium'),
        sa.Column('tags', ARRAY(sa.String(50)), nullable=False, server_default='{}'),
        sa.Column('due_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('recurrence', sa.String(20), nullable=False, server_default='none'),
        sa.Column('parent_id', UUID(as_uuid=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
    )

    # Create indexes
    op.create_index('ix_task_completed', 'task', ['completed'])
    op.create_index('ix_task_due_date', 'task', ['due_date'])
    op.create_index('ix_task_priority', 'task', ['priority'])
    op.create_index('ix_task_created_at', 'task', ['created_at'])
    op.create_index('ix_task_parent_id', 'task', ['parent_id'])


def downgrade() -> None:
    op.drop_index('ix_task_parent_id')
    op.drop_index('ix_task_created_at')
    op.drop_index('ix_task_priority')
    op.drop_index('ix_task_due_date')
    op.drop_index('ix_task_completed')
    op.drop_table('task')
