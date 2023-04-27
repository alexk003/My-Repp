
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


def to_bd(conn, user_id, found_profile_id):
    with conn.cursor() as cur:
        # if find_client(conn, email=email):  # Ищем клиента с таким имейлом
        #     return "Клиент с таким имейлом уже есть"  # Сообщаем пользователю, что клиент с таким имейлом уже есть
        cur.execute(
            """
            INSERT INTO viewed_profiles(user_id, found_profile_id)
            VALUES (%s, %s);
            """,
            (user_id, found_profile_id,)
        )
        conn.commit()
    #     if phone:  # Проверяем передали ли телефон при добавлении контакта
    #         client_id_ = cur.fetchone()  # получаем из запроса идентификационный номер и сохраняем в переменную
    #         adding_phone = add_phone(conn, client_id=client_id_, phone=phone)  # Вызываем функцию добавления номера телефона и рузультат сохраняем в переменную
    #         if adding_phone == 'Телефон добавлен':  # Проверяем вернулось ли сообщение, которое равно тому, что сообщает о существовании номера
    #             conn.rollback()  # Отменяем создание клиента
    #             return "Невозможно добавить, такой номер телефона уже существует"  # Сообщаем что добавить невозможно
    #     conn.commit()  # Делаем коммит у соединения
    # return "Профиль добавлен"  # Сообщаем что клиент добавлен


def from_db(conn, user_id):
    with conn.cursor() as cur:
        cur.execute("""SELECT found_profile_id FROM viewed_profiles WHERE user_id = %s;
                """,
                (user_id,)  # Передаем id клиента
            )
        id_list = cur.fetchall()
    return id_list

# дальше просто по циклу for id in id_list(conn), но это без класса (по принципу 5 задания из БД)


# def add_phone(conn, client_id, phone):
#     with conn.cursor() as cur:
#         if find_client(conn, phone=phone):
#             return "Такой номер телефона уже существует"  # Соообщаем что такой номер есть
#         cur.execute(
#             """
#             SELECT * FROM clients WHERE client_id = %s;
#             """,
#             (client_id,)  # Передаем id клиента
#         )
#         if not cur.fetchone():  # Проверяем вернулась ли пустая коллекция
#             return "Такого клиета нет"  # Соообщаем что такого клиента нет
#         cur.execute(
#             """
#             INSERT INTO phone_numbers (phone_number, client_id_ref) VALUES (%s, %s);
#             """,
#             (phone, client_id,)
#         )
#         conn.commit()  # Подтверждаем изменения
#     return "Телефон добавлен"  # Возвращаем сообщение об успехе
#
#
# def change_client(conn, client_id, first_name=None, last_name=None, email=None):
#     with conn.cursor() as cur:
#         if first_name:
#             cur.execute("""
#             UPDATE clients SET first_name=%s WHERE client_id = %s;
#                 """, (first_name, client_id,))
#         if last_name:
#             cur.execute("""
#             UPDATE clients SET last_name=%s WHERE client_id = %s;
#                 """, (last_name, client_id,))
#         if email:
#             cur.execute("""
#             UPDATE clients SET email=%s WHERE client_id = %s;
#                 """, (email, client_id,))
#         conn.commit()
#
#
# def delete_phone(conn, client_id):
#     with conn.cursor() as cur:
#         cur.execute("""
#             DELETE FROM phone_numbers WHERE client_id_ref=%s;
#                 """, (client_id, ))
#         conn.commit()
#
#
# def delete_client(conn, client_id):
#     with conn.cursor() as cur:
#         cur.execute("""
#             DELETE FROM clients WHERE client_id=%s;
#                 """, (client_id, ))
#         conn.commit()
#
#
# def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
#     with conn.cursor() as cur:
#         if first_name is None:
#             first_name = '%'
#
#         if last_name is None:
#             last_name = '%'
#
#         if email is None:
#             email = '%'
#
#         client = [first_name, last_name, email]
#         new_str = ''
#
#         if phone:
#             new_str = ' AND phone_number = %s::text'  # Присваиваем переменной, которую определили через
#             # строку выше, новое значение с условием поиска телефона. Вместо первых точек указываем столбец с номерами
#             # из таблицы номеров.
#
#             client.append(phone)
#
#         request = f"""
#                 SELECT
#                     clients.email,
#                     clients.first_name,
#                     clients.last_name,
#                     CASE
#                         WHEN ARRAY_AGG(phone_number) = '{{Null}}' THEN ARRAY[]::TEXT[]
#                         ELSE ARRAY_AGG(phone_number)
#                     END phones
#                 FROM clients
#                 LEFT JOIN phone_numbers ON clients.client_id = phone_numbers.client_id_ref
#                 WHERE first_name LIKE %s AND last_name LIKE %s AND email LIKE %s{new_str}
#                 GROUP BY email, first_name, last_name
#                 """
#         cur.execute(
#
#             request,  # Передаем переменную с запросом
#
#             client  # Передаем список или кортеж с значениями
#         )
#         conn.commit()
#         return cur.fetchall()
#
#
# def print_data(conn):
#     with conn.cursor() as cur:
#         cur.execute("""SELECT * FROM clients;""")
#         print(cur.fetchall())
#         cur.execute("""SELECT * FROM phone_numbers;""")
#         print(cur.fetchall())
#
#
# with psycopg2.connect(database="client_db", user="postgres", password="*6352a17",) as conn:
#
#     clear_table(conn)
#
#     create_db(conn)
#
#     add_client(conn, "Alex", "Kom", "AlexKom@mail.ru", 12345623)
#
#     add_client(conn, "Alex2", "Kom2", "AlexKom2@mail.ru", 1234562)
#
#     add_client(conn, "Alex3", "Kom3", "AlexKom3@mail.ru", 123456233)
#
#     add_phone(conn, 1, 123456)
#
#     change_client(conn, 2, last_name="Ivanov", email="Ivan@ya.ru")
#
#     delete_phone(conn, 2)
#
#     delete_client(conn, 2)
#
#     print_data(conn)