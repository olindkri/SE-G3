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

cur.execute("INSERT INTO posts (byUser, title, content, country, city, language, price) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (1, 'Olivers guide', 'Hi, is this working?.', 'Norway', 'Halden', 'Norsk', 320)
            )

cur.execute("INSERT INTO posts (byUser, title, content, country, city, language, price) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (2, 'Nontagans guide', 'Hi, do you want a tour?.', 'Thailand', 'Bangkok', 'Thai', 425)
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
            ('Hello Oliver!', 1, 2)
            )

cur.execute("INSERT INTO message (content, inChat, byUser) VALUES (?, ?, ?)",
            ('Yo, Nontagan!', 4, 4)
            )

cur.execute("INSERT INTO message (content, inChat, byUser) VALUES (?, ?, ?)",
            ('Hello Sakariya!', 3, 1)
            )

cur.execute("INSERT INTO message (content, inChat, byUser) VALUES (?, ?, ?)",
            ('Hello Erik!', 2, 1)
            )

cur.execute("INSERT INTO message (content, inChat, byUser) VALUES (?, ?, ?)",
            ('How are you?', 1, 1)
            )

cur.execute("INSERT INTO message (content, inChat, byUser) VALUES (?, ?, ?)",
            ('Hello Sakariya!', 4, 2)
            )

cur.execute("INSERT INTO guide_user (user, guide, from_date, to_date) VALUES (?, ?, ?, ?)",
            (1, 2, "2023-10-15", "2023-10-20")
            )

cur.execute("INSERT INTO guide_user (user, guide, from_date, to_date) VALUES (?, ?, ?, ?)",
            (2, 1, "2023-11-04", "2023-11-14")
            )

connection.commit()
connection.close()
