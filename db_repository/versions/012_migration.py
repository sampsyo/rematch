from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
posts = Table('posts', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('title', VARCHAR(length=120)),
    Column('desc', VARCHAR(length=10000)),
    Column('qualifications', VARCHAR(length=10000)),
    Column('professor_id', VARCHAR(length=64)),
    Column('current_students', VARCHAR(length=10000)),
    Column('desired_skills', VARCHAR(length=10000)),
    Column('capacity', INTEGER),
    Column('current_number', INTEGER),
)

posts = Table('posts', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=120)),
    Column('description', String(length=10000)),
    Column('qualifications', String(length=10000)),
    Column('professor_id', String(length=64)),
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
    pre_meta.tables['posts'].columns['desc'].drop()
    post_meta.tables['posts'].columns['description'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['posts'].columns['desc'].create()
    post_meta.tables['posts'].columns['description'].drop()
