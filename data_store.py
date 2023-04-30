
import psycopg2

conn = psycopg2.connect(database="postgres", user="postgres", password="*6352a17")


def clear_table(conn):
    with conn.cursor() as cur:
        cur.execute("""DELETE FROM viewed_profiles""")
        conn.commit()


def create_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS viewed_profiles(
                user_id INTEGER,
                found_profile_id INTEGER UNIQUE);
            """)
        conn.commit()


def to_db(conn, user_id, found_profile_id):
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO viewed_profiles(user_id, found_profile_id)
            VALUES (%s, %s);
            """,
            (user_id, found_profile_id,)
        )
        conn.commit()


def from_db(conn, user_id):
    with conn.cursor() as cur:
        cur.execute("""SELECT found_profile_id FROM viewed_profiles WHERE user_id = %s;
                """,
                (user_id,)  # Передаем id клиента
            )
        id_list = cur.fetchall()
    return id_list