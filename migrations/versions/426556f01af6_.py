"""empty message

Revision ID: 426556f01af6
Revises: b3403fa9cdc8
Create Date: 2020-03-06 20:25:14.221750

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '426556f01af6'
down_revision = 'b3403fa9cdc8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('CAPEC',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('capecId', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('abstraction', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('alternateTerms', sa.String(), nullable=True),
    sa.Column('likelihoodOfAttack', sa.String(), nullable=True),
    sa.Column('typicalSeverity', sa.String(), nullable=True),
    sa.Column('relatedAttack', sa.String(), nullable=True),
    sa.Column('patterns', sa.String(), nullable=True),
    sa.Column('executionFlow', sa.String(), nullable=True),
    sa.Column('prerequisites', sa.String(), nullable=True),
    sa.Column('skillsRequired', sa.String(), nullable=True),
    sa.Column('resourcesRequired', sa.String(), nullable=True),
    sa.Column('indicators', sa.String(), nullable=True),
    sa.Column('consequences', sa.String(), nullable=True),
    sa.Column('mitigations', sa.String(), nullable=True),
    sa.Column('exampleInstances', sa.String(), nullable=True),
    sa.Column('relatedWeaknesses', sa.String(), nullable=True),
    sa.Column('taxonomyMappings', sa.String(), nullable=True),
    sa.Column('notes', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_CAPEC_capecId'), 'CAPEC', ['capecId'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_CAPEC_capecId'), table_name='CAPEC')
    op.drop_table('CAPEC')
    # ### end Alembic commands ###
