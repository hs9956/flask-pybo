"""empty message

Revision ID: 5845ef4592b7
Revises: 29c540570b9f
Create Date: 2021-09-16 01:46:37.169749

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5845ef4592b7'
down_revision = '29c540570b9f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('question_voter',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], name=op.f('fk_question_voter_question_id_question'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_question_voter_user_id_user'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'question_id', name=op.f('pk_question_voter'))
    )
    op.create_table('answer_voter',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('answer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['answer_id'], ['answer.id'], name=op.f('fk_answer_voter_answer_id_answer'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_answer_voter_user_id_user'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'answer_id', name=op.f('pk_answer_voter'))
    )
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable='False')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    op.drop_table('answer_voter')
    op.drop_table('question_voter')
    # ### end Alembic commands ###
