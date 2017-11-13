
import sqlite3

connection = sqlite3.connect("data.db")
cursor = connection.cursor()

create_users_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"  ## id is auto increment here
cursor.execute(create_users_table)

create_items_table = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price real)"  
cursor.execute(create_items_table)

#cursor.execute("INSERT INTO items VALUES ('piano', 20.99)")

connection.commit()
connection.close()