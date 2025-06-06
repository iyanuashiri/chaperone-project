"""add new fields to the Association game

Revision ID: a5180d0fc9d5
Revises: 
Create Date: 2025-05-17 04:31:09.379304

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel             # NEW



# revision identifiers, used by Alembic.
revision: str = 'a5180d0fc9d5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('vocabulary',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('word', sa.String(length=50), nullable=False),
    sa.Column('meaning', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('association',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('PENDING', 'CORRECT', 'INCORRECT', name='associationstatus'), nullable=False),
    sa.Column('number_of_times_played', sa.Integer(), nullable=False),
    sa.Column('number_of_times_correct', sa.Integer(), nullable=False),
    sa.Column('number_of_times_incorrect', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('vocabulary_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['vocabulary_id'], ['vocabulary.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('option',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('option', sa.String(length=255), nullable=False),
    sa.Column('meaning', sa.String(length=255), nullable=False),
    sa.Column('is_correct', sa.Boolean(), nullable=False),
    sa.Column('association_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['association_id'], ['association.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('option')
    op.drop_table('association')
    op.drop_table('vocabulary')
    op.drop_table('user')
    # ### end Alembic commands ###
