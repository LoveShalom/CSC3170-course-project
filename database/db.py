"""
Time: 2024/11/1
This file is used for the initialization of database and table creation. Besides, it
also used to insert test data. Totally two clients, three employees, two restaurants
with two foods each.
"""

import sqlite3

# Connect to the database
conn = sqlite3.connect('csc3170.db')

# Create 7 tables
# conn.execute('DROP TABLE users;')
conn.execute('DROP TABLE restaurants;')
# conn.execute('DROP TABLE food;')
# conn.execute('DROP TABLE employees;')
# conn.execute('DROP TABLE orders;')
# conn.execute('DROP TABLE order_info;')
# conn.execute('DROP TABLE work_study;')


# users table
conn.execute(
    'CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT, account NONE NOT NULL, password NONE '
    'NOT NULL, phone TEXT NOT NULL, add_time TEXT NOT NULL, modify_time TEXT NOT NULL);'
)
conn.commit()

# restaurants table
conn.execute(
    'CREATE TABLE restaurants(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, password NONE NOT NULL,'
    'store_manager TEXT NOT NULL,num_of_employees INT NOT NULL, level INT, num_foods INT NOT NULL,'
    'add_time TEXT NOT NULL, modify_time TEXT NOT NULL);'
)
conn.commit()

# food table
conn.execute(
    'CREATE TABLE food(id INTEGER PRIMARY KEY AUTOINCREMENT, id_shop INTEGER NOT NULL, name TEXT NOT NULL,'
    'material TEXT NOT NULL, tasty TEXT, price INT NOT NULL, cost INT, '
    'add_time TEXT NOT NULL, modify_time TEXT NOT NULL,FOREIGN KEY(id_shop) REFERENCES restaurants(id));'

 )
conn.commit()

# employees table
conn.execute(
    'CREATE TABLE employees(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,'
    'age INT, sex TEXT, type TEXT NOT NULL,'
    'salary INT NOT NULL, status TEXT NOT NULL, add_time TEXT NOT NULL, modify_time TEXT NOT NULL);'
)
conn.commit()

# order table
conn.execute(
    'CREATE TABLE orders(id INTEGER PRIMARY KEY AUTOINCREMENT, id_shop INTEGER NOT NULL, id_client INTEGER NOT NULL,'
    'total_price INT NOT NULL, status TEXT NOT NULL, pay_status TEXT NOT NULL, '
    'add_time TEXT NOT NULL, modify_time TEXT NOT NULL,FOREIGN KEY(id_shop) REFERENCES restaurants(id),FOREIGN KEY('
    'id_client) REFERENCES users(id));'
)
conn.commit()

# order information table
conn.execute(
    'CREATE TABLE order_info(id INTEGER PRIMARY KEY AUTOINCREMENT, id_order INTEGER NOT NULL, id_food INTEGER NOT NULL,'
    'price INT NOT NULL, status TEXT NOT NULL, amount INT NOT NULL,FOREIGN KEY(id_order) REFERENCES orders(id),'
    'FOREIGN KEY(id_food) REFERENCES food(id));'
)
conn.commit()

# work study table
conn.execute(
    'CREATE TABLE work_study(student_id INTEGER PRIMARY KEY AUTOINCREMENT, id_work INTEGER NOT NULL,name TEXT NOT '
    'NULL, college TEXT NOT NULL,'
    'major TEXT NOT NULL, faculty TEXT NOT NULL, year TEXT NOT NULL, current_job TEXT NOT NULL, salary INT NOT NULL,'
    'add_time TEXT NOT NULL, modify_time TEXT NOT NULL, FOREIGN KEY(id_work) REFERENCES employees(id));'
)
conn.commit()


# insert test data
# client
conn.execute(
    'INSERT INTO users(id, account, password, phone, add_time, modify_time)'
    'VALUES(000, "123", "123456", "13317449999", "2024-11-02 12:20:15.123", "2024-11-02 12:20:15.123");'
)
conn.commit()

conn.execute(
    'INSERT INTO users(id, account, password, phone, add_time, modify_time)'
    'VALUES(001, "kelly", "552233", "18817449999", "2024-11-02 13:20:14.123", "2024-11-02 12:20:15.123");'
)
conn.commit()

conn.close()







