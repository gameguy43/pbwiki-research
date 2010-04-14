from sqlalchemy import create_engine
from sqlalchemy import MetaData, Column, Table
from sqlalchemy import Integer, Text

engine = create_engine('sqlite:///pbworks.sql')
metadata = MetaData(bind=engine)

wikis_table = Table('edu_wikis', metadata,
    Column('id', Integer, primary_key=True),
    Column('url', Text),

    Column('files_count', Integer),
    Column('files_checked_at', Integer),
    Column('files_list', Text),

    Column('page_char_size', Integer),
    Column('page_checked_at', Integer),
    Column('page_html', Text),
    Column('page_name', Text),
    Column('page_revision', Integer),
    Column('page_url', Text),

    Column('pages_count', Integer),
    Column('pages_list', Text),

    Column('time_pageedit', Integer),
    Column('time_file', Integer),
    Column('time_tag', Integer),
    Column('time_permission', Integer),
    Column('time_comment', Integer),
    Column('times_checked_at', Integer),

    Column('works', Integer)
    )

metadata.create_all()


def table_from_wiki(id, url, pages)
    pass
