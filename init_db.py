import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO user (firstname, lastname, age, country) VALUES (?, ?, ?, ?)",
            ('Oliver Lind', 'Kristiansen', 20, 'Norway')
            )

cur.execute("INSERT INTO user (firstname, lastname, age, country) VALUES (?, ?, ?, ?)",
            ('Nontagan', 'Phomin', 20, 'Norway')
            )

cur.execute("INSERT INTO posts (byUser, title, content) VALUES (?, ?, ?)",
            (1, 'First Post', 'Content for the first post')
            )

cur.execute("INSERT INTO posts (byUser, title, content) VALUES (?, ?, ?)",
            (2, 'Second Post', 'Content for the second post')
            )

connection.commit()
connection.close()
