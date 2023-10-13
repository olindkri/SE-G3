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
            (1, 'Olivers Post', 'Content for my post')
            )

cur.execute("INSERT INTO posts (byUser, title, content) VALUES (?, ?, ?)",
            (2, 'Nontas Post', 'Content for my post')
            )

cur.execute("INSERT INTO chat (user1, user2) VALUES (?, ?)",
            (1, 2)
            )

cur.execute("INSERT INTO message (content, inChat, byUser) VALUES (?, ?, ?)",
            ('Hello Nontagan!', 1, 1)
            )

connection.commit()
connection.close()
