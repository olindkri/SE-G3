import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO user (firstname, lastname, age, country) VALUES (?, ?, ?, ?)",
            ('Oliver Lind', 'Kristiansen', 20, 'Norway')
            )

cur.execute("INSERT INTO user (firstname, lastname, age, country) VALUES (?, ?, ?, ?)",
            ('Nontagan', 'Phomin', 21, 'Norway')
            )

cur.execute("INSERT INTO user (firstname, lastname, age, country) VALUES (?, ?, ?, ?)",
            ('Erik', 'Evjen', 23, 'Norway')
            )

cur.execute("INSERT INTO user (firstname, lastname, age, country) VALUES (?, ?, ?, ?)",
            ('Sakariya', 'Mahamud', 24, 'Norway')
            )

cur.execute("INSERT INTO posts (byUser, title, content) VALUES (?, ?, ?)",
            (1, 'Olivers Post', 'Content for my post.')
            )

cur.execute("INSERT INTO posts (byUser, title, content) VALUES (?, ?, ?)",
            (2, 'Nontas Post', 'Content for my post.')
            )

cur.execute("INSERT INTO posts (byUser, title, content) VALUES (?, ?, ?)",
            (3, 'Eriks Post', 'Content for my post.')
            )

cur.execute("INSERT INTO posts (byUser, title, content) VALUES (?, ?, ?)",
            (4, 'Sakariyas Post', 'Content for my post.')
            )

cur.execute("INSERT INTO chat (user1, user2) VALUES (?, ?)",
            (1, 2)
            )

cur.execute("INSERT INTO chat (user1, user2) VALUES (?, ?)",
            (1, 3)
            )

cur.execute("INSERT INTO chat (user1, user2) VALUES (?, ?)",
            (1, 4)
            )

cur.execute("INSERT INTO chat (user1, user2) VALUES (?, ?)",
            (2, 4)
            )

cur.execute("INSERT INTO chat (user1, user2) VALUES (?, ?)",
            (3, 4)
            )

cur.execute("INSERT INTO message (content, inChat, byUser) VALUES (?, ?, ?)",
            ('Hello Nontagan!', 1, 1)
            )

cur.execute("INSERT INTO message (content, inChat, byUser) VALUES (?, ?, ?)",
            ('Hello Sakariya!', 4, 2)
            )

connection.commit()
connection.close()
