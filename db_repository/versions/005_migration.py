from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
post = Table('post', pre_meta,
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

professor = Table('professor', pre_meta,
    Column('net_id', VARCHAR(length=64), primary_key=True, nullable=False),
    Column('name', VARCHAR(length=64)),
    Column('email', VARCHAR(length=120)),
    Column('desc', VARCHAR(length=10000)),
    Column('interests', VARCHAR(length=10000)),
)

posts = Table('posts', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=120)),
    Column('desc', String(length=10000)),
    Column('qualifications', String(length=10000)),
    Column('professor_id', String(length=64)),
    Column('current_students', String(length=10000)),
    Column('desired_skills', String(length=10000)),
    Column('capacity', Integer),
    Column('current_number', Integer),
)

professors = Table('professors', post_meta,
    Column('net_id', String(length=64), primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('email', String(length=120)),
    Column('desc', String(length=10000)),
    Column('interests', String(length=10000)),
)

students = Table('students', post_meta,
    Column('net_id', String(length=64), primary_key=True, nullable=False),
    Column('email', String(length=64)),
    Column('name', String(length=64)),
    Column('major', String(length=64)),
    Column('year', Integer),
    Column('skills', String(length=10000)),
    Column('resume', String(length=10000)),
    Column('description', String(length=10000)),
    Column('interests', String(length=10000)),
    Column('favorited_projects', String(length=10000)),
    Column('availability', String(length=10000)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['post'].drop()
    pre_meta.tables['professor'].drop()
    post_meta.tables['posts'].create()
    post_meta.tables['professors'].create()
    post_meta.tables['students'].columns['email'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['post'].create()
    pre_meta.tables['professor'].create()
    post_meta.tables['posts'].drop()
    post_meta.tables['professors'].drop()
    post_meta.tables['students'].columns['email'].drop()
