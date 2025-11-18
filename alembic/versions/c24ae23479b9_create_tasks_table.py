"""create tasks table

Revision ID: c24ae23479b9
Revises: 204ad66180ec
Create Date: 2025-11-12 10:42:36.475213
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY


# revision identifiers, used by Alembic.
revision: str = 'c24ae23479b9'
down_revision: Union[str, Sequence[str], None] = '204ad66180ec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('Task_ID', sa.String(), unique=True, nullable=False),
        sa.Column('Task_Name', sa.String(), nullable=True),
        sa.Column('Project_ID', ARRAY(sa.String()), server_default='{}', nullable=True),
        sa.Column('Type', sa.String(), nullable=True),
        sa.Column('Assigned_To', ARRAY(sa.String()), server_default='{}', nullable=True),
        sa.Column('Priority', sa.String(), nullable=True),
        sa.Column('Deadline', sa.DateTime(timezone=True), nullable=True),
        sa.Column('Status', sa.String(), nullable=True),
        sa.Column('Dependencies', ARRAY(sa.String()), server_default='{}', nullable=True),
        sa.Column('Description', sa.Text(), nullable=True),
        sa.Column('Skills_Required', ARRAY(sa.String()), server_default='{}', nullable=True),

        # ⏱️ Timestamp fields
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )


def downgrade():
    op.drop_table('tasks')
