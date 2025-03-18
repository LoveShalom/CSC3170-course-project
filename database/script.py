"""
2024/11/8
Author: Deng Yifan
 It's for check of database, and the file doesn't affect the running of program.
"""
import sqlite3


# Connect to the database
conn = sqlite3.connect('csc3170.db')

conn.execute('DROP TABLE food;')

# order information table
conn.execute(
    'CREATE TABLE food(id INTEGER PRIMARY KEY AUTOINCREMENT, id_shop INTEGER NOT NULL, name TEXT NOT NULL,'
    'material TEXT NOT NULL, tasty TEXT, price INT NOT NULL, cost INT, '
    'add_time TEXT NOT NULL, modify_time TEXT NOT NULL,FOREIGN KEY(id_shop) REFERENCES restaurants(id));'

 )
conn.commit()

conn.close()