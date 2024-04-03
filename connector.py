import psycopg2
from psycopg2 import sql, extras

class Connector:
    def __init__(self):
        self.mydb = None
        self.start_session()


    def user_login(self, username_or_email, pwd):
        try:
            mycursor = self.mydb.cursor()
            mycursor.execute("SELECT username, email, pwd FROM users WHERE username = %s OR email = %s AND pwd = %s", (username_or_email, username_or_email, pwd))

            result = mycursor.fetchone()

            if result is None:
                print(f"[LOGIN-ERROR] User '{username_or_email}' does not exists.")                
                return False
            else:
                print(f"[LOGIN-SUCCESS] User '{username_or_email}' successfully logged in.")
                return True

        except Exception as e:
            print(f"[LOGIN-ERROR] Unexpected exception ocurred when trying to login: {e}")
            return False

    def user_register(self, username, email, pwd):
            try:
                mycursor = self.mydb.cursor()
                mycursor.execute("INSERT INTO users (username, email, pwd) VALUES (%s, %s, %s)", (username, email, pwd))
                self.mydb.commit()

                result = mycursor.fetchone()

                if result is None:
                    print(f"[REG-ERROR] User '{email}' already exists.")                
                    return False
                else:
                    print(f"[REG-SUCCESS] User '{email}' successfully registered.")
                    return True

            except Exception as e:
                print(f"[REG-ERROR] Unexpected exception ocurred on registration of user '{email}': {e}")
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
