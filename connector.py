import psycopg2
from psycopg2 import sql, extras

class Connector:
    def __init__(self):
        self.mydb = None
        self.start_session()


    def user_login(self, username_or_email, pwd):
        try:
            mycursor = self.mydb.cursor()
            mycursor.execute("SELECT * FROM (SELECT * FROM users WHERE username = %s OR email = %s) WHERE pwd = %s", (username_or_email, username_or_email, pwd))

            result = mycursor.fetchone()

            if result is None:
                print(f"[ERROR] User or password '{username_or_email}' are not correct.")
                return False
            else:
                print(f"[SUCCESS] User '{username_or_email}' successfully logged in.")
                return True

        except Exception as e:
            print(f"[EXCEPTION] Unexpected exception ocurred when trying to login: {e}")
            return False

    def user_register(self, username, email, pwd):
            try:
                mycursor = self.mydb.cursor()
                mycursor.execute("INSERT INTO users (username, email, pwd) VALUES (%s, %s, %s)", (username, email, pwd))
                self.mydb.commit()

                result = mycursor.fetchone()

                if result is None:
                    print(f"[ERROR] User '{email}' already exists.")                
                    return False
                else:
                    print(f"[SUCCESS] User '{email}' successfully registered.")
                    return True

            except Exception as e:
                print(f"[EXCEPTION] Unexpected exception ocurred on registration of user '{email}': {e}")
                return False

    def get_registered_users(self):
        try:
            mycursor = self.mydb.cursor()
            mycursor.execute("SELECT username, email, pwd FROM users")

            result = mycursor.fetchall()

            if result is None:
                print(f"[ERROR] There are no users registered.")                
                return False
            else:
                print(f"[SUCCESS] Successfully selected registered users.")
                return result

        except Exception as e:
            print(f"[EXCEPTION] Unexpected exception ocurred: {e}")
            return False


    def insert_book(self, id, name, description, author, publication_date, page_qty, book_cover_uri):
        try:
            mycursor = self.mydb.cursor()
            mycursor.execute("INSERT INTO books (id, name, description, author, publication_date, page_qty, book_cover_uri) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                                (id, name, description, author, publication_date, page_qty, book_cover_uri))
            self.mydb.commit()

            print(f"[SUCCESS] Book successfully created.")
            return True

        except Exception as e:
            print(f"[EXCEPTION] Unexpected exception ocurred: {e}")
            return False

    def insert_user_book(self, book_id, username, creation_date, update_date):
        try:
            mycursor = self.mydb.cursor()
            mycursor.execute("INSERT INTO user_books (book_id, username, creation_date, update_date) VALUES (%s, %s, %s, %s)",
                                (book_id, username, creation_date, update_date))
            self.mydb.commit()

            return True

        except Exception as e:
            print(f"[EXCEPTION] Unexpected exception ocurred: {e}")
            return False

    def start_session(self):
        try:
            self.mydb = psycopg2.connect(
                host="192.168.1.87",
                user="postgres",
                password="bookself",
                dbname="bookself"
            )
        except Exception as e:
            print(f"[CONN-ERROR] Unexpected exception ocurred when trying to connect to database: {e}")


    def end_session(self):
        self.mydb.close()
