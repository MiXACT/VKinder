import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
import psycopg2


def db_engine(db_init):
    DB = f"postgresql://postgres:{db_init['password']}@localhost:5432/{db_init['db']}"
    engine = sq.create_engine(DB)
    connection = engine.connect()
    return connection

def del_db(tab, db_init):
    connection = db_engine(db_init)
    connection.execute(f"TRUNCATE {tab} CASCADE;")
    return

def candidates_tab(data_to_fill, last_id, db_init):
    connection = db_engine(db_init)
    for i, v in enumerate(data_to_fill):
        try:
            connection.execute(
                f"INSERT INTO candidates VALUES({last_id + i},"
                f"'{v['last_name']} {v['first_name']}',"
                f"'https://vk.com/id{v['id']}');"
            )
        except KeyError:
            continue
    return last_id + i

def photo_tab(vk_id, pics, owner_num, last_id, db_init):
    connection = db_engine(db_init)
    for i, v in enumerate(pics):
        connection.execute(
            f"INSERT INTO photos VALUES({last_id + i},"
            f"'https://vk.com/photo{vk_id}_{v['id']}',"
            f"{owner_num});"
        )
    return last_id + i