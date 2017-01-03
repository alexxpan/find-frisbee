from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
event = Table('event', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('type', String(length=20)),
    Column('date', String(length=20)),
    Column('location', String(length=50)),
    Column('time', String(length=20)),
    Column('am_or_pm', String(length=20)),
    Column('description', String(length=140)),
    Column('host_id', Integer),
    Column('edited_type', Boolean, default=ColumnDefault(False)),
    Column('edited_date', Boolean, default=ColumnDefault(False)),
    Column('edited_location', Boolean, default=ColumnDefault(False)),
    Column('edited_time', Boolean, default=ColumnDefault(False)),
    Column('edited_am_or_pm', Boolean, default=ColumnDefault(False)),
    Column('edited_description', Boolean, default=ColumnDefault(False)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['event'].columns['am_or_pm'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['event'].columns['am_or_pm'].drop()
