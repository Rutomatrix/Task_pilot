"""create clients, projects, tasks, users, and teams (no relations)"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision: str = "b39125fe71e9"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema without foreign keys or join tables"""

    # --- Clients ---
    op.create_table(
        "clients",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("Client_ID", sa.String(), unique=True, nullable=False),
        sa.Column("Client_Name", sa.String(), nullable=False),
        sa.Column("Description", sa.Text(), nullable=True),
        sa.Column("Type", sa.String(), nullable=True),
        sa.Column("Status", sa.String(), nullable=True),
        sa.Column("Active_Projects", sa.Integer(), nullable=True),
    )

    # --- Teams ---
    op.create_table(
        "teams",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("Team_ID", sa.String(), unique=True, nullable=False),
        sa.Column("Category", sa.String(), nullable=True),
    )

    # --- Users ---
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("Emp_ID", sa.String(), unique=True, nullable=False),
        sa.Column("Team_ID", sa.String(), nullable=True),
        sa.Column("Name", sa.String(), nullable=True),
        sa.Column("Role", sa.String(), nullable=True),
        sa.Column("Skillset", sa.String(), nullable=True),
        sa.Column("Current_Tasks", sa.Integer(), nullable=True),
        sa.Column("Status", sa.String(), nullable=True),
        sa.Column("Comments", sa.Text(), nullable=True),
    )

    # --- Projects ---
    op.create_table(
        "projects",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("Project_ID", sa.String(), unique=True, nullable=False),
        sa.Column("Name", sa.String(), nullable=False),
        sa.Column("Client_ID", sa.String(), nullable=True),
        sa.Column("Description", sa.Text(), nullable=True),
        sa.Column("Priority", sa.String(), nullable=True),
        sa.Column("Deadline", sa.DateTime(), nullable=True),
        sa.Column("Status", sa.String(), nullable=True),
        sa.Column("Linked_Inventory", sa.String(), nullable=True),
    )

    # --- Tasks ---
    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("Task_ID", sa.String(), unique=True, nullable=False),
        sa.Column("Task_Name", sa.String(), nullable=True),
        sa.Column("Project_ID", sa.String(), nullable=True),
        sa.Column("Type", sa.String(), nullable=True),
        sa.Column("Assigned_To", sa.String(), nullable=True),
        sa.Column("Priority", sa.String(), nullable=True),
        sa.Column("Deadline", sa.DateTime(), nullable=True),
        sa.Column("Status", sa.String(), nullable=True),
        sa.Column("Dependencies", sa.String(), nullable=True),
        sa.Column("Description", sa.Text(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("tasks")
    op.drop_table("projects")
    op.drop_table("users")
    op.drop_table("teams")
    op.drop_table("clients")
