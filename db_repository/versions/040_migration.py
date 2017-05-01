from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
posts = Table('posts', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('title', VARCHAR(length=120)),
    Column('description', VARCHAR(length=10000)),
    Column('professor_id', VARCHAR(length=64)),
    Column('tags', VARCHAR(length=10000)),
    Column('is_active', BOOLEAN, nullable=False),
    Column('date_created', DATETIME),
    Column('date_modified', DATETIME),
    Column('stale_date', DATETIME),
    Column('qualifications', VARCHAR(length=10000)),
    Column('current_students', VARCHAR(length=10000)),
    Column('desired_skills', VARCHAR(length=10000)),
    Column('capacity', INTEGER),
    Column('current_number', INTEGER),
)

posts = Table('posts', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=120)),
    Column('description', String(length=10000)),
    Column('professor_id', String(length=64)),
    Column('tags', String(length=10000)),
    Column('is_active', Boolean, nullable=False, default=ColumnDefault(True)),
    Column('stale_date', DateTime),
    Column('contact_email', String(length=10000)),
    Column('project_link', String(length=10000)),
    Column('required_courses', String(length=10000)),
    Column('grad_requirements', String(length=10000)),
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
    pre_meta.tables['posts'].columns['date_created'].drop()
    pre_meta.tables['posts'].columns['date_modified'].drop()
    post_meta.tables['posts'].columns['contact_email'].create()
    post_meta.tables['posts'].columns['grad_requirements'].create()
    post_meta.tables['posts'].columns['project_link'].create()
    post_meta.tables['posts'].columns['required_courses'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['posts'].columns['date_created'].create()
    pre_meta.tables['posts'].columns['date_modified'].create()
    post_meta.tables['posts'].columns['contact_email'].drop()
    post_meta.tables['posts'].columns['grad_requirements'].drop()
    post_meta.tables['posts'].columns['project_link'].drop()
    post_meta.tables['posts'].columns['required_courses'].drop()
