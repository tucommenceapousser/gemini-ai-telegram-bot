"""Add foreign key to ChatSession

Revision ID: ddd488dfb70c
Revises: af8fa7460019
Create Date: 2024-11-22 07:50:11.964940

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ddd488dfb70c'
down_revision = 'af8fa7460019'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chat_message', schema=None) as batch_op:
        batch_op.alter_column('chat_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.create_foreign_key(None, 'chat_session', ['chat_id'], ['id'])

    with op.batch_alter_table('chat_session', schema=None) as batch_op:
        batch_op.alter_column('chat_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.create_unique_constraint(None, ['chat_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chat_session', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('chat_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    with op.batch_alter_table('chat_message', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.alter_column('chat_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###