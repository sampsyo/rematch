from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
posts = Table('posts', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=120)),
    Column('description', String(length=10000)),
    Column('professor_id', String(length=64)),
    Column('tags', String(length=10000)),
    Column('is_active', Boolean, nullable=False, default=ColumnDefault(True)),
    Column('date_created', DateTime, default=ColumnDefault(<sqlalchemy.sql.functions.current_timestamp at 0x104f6f410; current_timestamp>)),
    Column('date_modified', DateTime, onupdate=ColumnDefault(<sqlalchemy.sql.functions.current_timestamp at 0x104f6f710; current_timestamp>), default=ColumnDefault(<sqlalchemy.sql.functions.current_timestamp at 0x104f6f610; current_timestamp>)),
    Column('stale_date', DateTime),
    Column('contact_email', String(length=10000)),
    Column('project_link', String(length=10000)),
    Column('qualifications', String(length=10000)),
    Column('current_students', String(length=10000)),
    Column('desired_skills', String(length=10000)),
    Column('capacity', Integer),
    Column('current_number', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['posts'].columns['contact_email'].create()
    post_meta.tables['posts'].columns['project_link'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['posts'].columns['contact_email'].drop()
    post_meta.tables['posts'].columns['project_link'].drop()
