from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
migration_tmp = Table('migration_tmp', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('type', VARCHAR(length=20)),
    Column('date', VARCHAR(length=20)),
    Column('location', VARCHAR(length=50)),
    Column('time', VARCHAR(length=20)),
    Column('description', VARCHAR(length=140)),
    Column('host_id', INTEGER),
    Column('is_editing', BOOLEAN),
    Column('edited_date', BOOLEAN),
    Column('edited_description', BOOLEAN),
    Column('edited_location', BOOLEAN),
    Column('edited_time', BOOLEAN),
    Column('edited_type', BOOLEAN),
)

event = Table('event', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('type', String(length=20)),
    Column('date', String(length=20)),
    Column('location', String(length=50)),
    Column('time', String(length=20)),
    Column('description', String(length=140)),
    Column('host_id', Integer),
    Column('edited_type', Boolean, default=ColumnDefault(False)),
    Column('edited_date', Boolean, default=ColumnDefault(False)),
    Column('edited_location', Boolean, default=ColumnDefault(False)),
    Column('edited_time', Boolean, default=ColumnDefault(False)),
    Column('edited_description', Boolean, default=ColumnDefault(False)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['migration_tmp'].drop()
    post_meta.tables['event'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['migration_tmp'].create()
    post_meta.tables['event'].drop()
