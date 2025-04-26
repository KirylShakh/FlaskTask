"""Insert example users

Revision ID: d82d8b3f208f
Revises: 8b1758b8def8
Create Date: 2025-04-24 19:54:24.340326

"""
from alembic import op
from sqlalchemy import Table, MetaData


# revision identifiers, used by Alembic.
revision = 'd82d8b3f208f'
down_revision = '8b1758b8def8'
branch_labels = None
depends_on = None


def upgrade():
    meta = MetaData()
    users = Table('user', meta, autoload_with=op.get_bind())

    op.bulk_insert(users, [{"name": "Johnny"}, {"name": "Kate"}])


def downgrade():
    pass
