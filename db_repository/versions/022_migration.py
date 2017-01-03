from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
event = Table('event', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('type', VARCHAR(length=20)),
    Column('date', VARCHAR(length=20)),
    Column('location', VARCHAR(length=50)),
    Column('time', VARCHAR(length=20)),
    Column('description', VARCHAR(length=140)),
    Column('host_id', INTEGER),
    Column('edited_type', BOOLEAN),
    Column('edited_date', BOOLEAN),
    Column('edited_location', BOOLEAN),
    Column('edited_time', BOOLEAN),
    Column('edited_am_or_pm', BOOLEAN),
    Column('edited_description', BOOLEAN),
    Column('am_or_pm', VARCHAR(length=20)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['event'].columns['am_or_pm'].drop()
    pre_meta.tables['event'].columns['edited_am_or_pm'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['event'].columns['am_or_pm'].create()
    pre_meta.tables['event'].columns['edited_am_or_pm'].create()
