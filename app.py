import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'

user_id = 1


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


def get_user(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM user WHERE id = ?',
                        (user_id,)).fetchone()
    conn.close()
    if user is None:
        abort(404)
    return user


@app.route('/user/', methods=('GET', 'POST'))
def user():
    if request.method == 'POST':
        global user_id
        if request.form.get('user1') == '1':
            user_id = 1
            return redirect(url_for('index'))
        elif request.form.get('user2') == '2':
            user_id = 2
            return redirect(url_for('index'))

    return render_template('user.html')


@app.route('/')
def index():
    global user_id
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts, user WHERE NOT byUser = ? AND user.id = byUser ORDER BY posts.id DESC', (user_id,)).fetchall()
    conn.close()
    return render_template('index.html', posts=posts)


@app.route('/chat/')
def chat():
    global user_id
    conn = get_db_connection()
    chat = conn.execute(
        'SELECT * FROM chat, user WHERE CASE WHEN ? = user1 THEN user.id = user2 WHEN ? = user2 THEN user.id = user1 END',
        (user_id, user_id,)).fetchall()
    conn.close()
    return render_template('chat.html', chat=chat)


@app.route('/my-guides/')
def guides():
    global user_id
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts, user WHERE byUser = ? AND user.id = posts.byUser ORDER BY posts.id DESC', (user_id,)).fetchall()
    conn.close()
    return render_template('my-guides.html', posts=posts)


@app.route('/profile/', methods=('GET', 'POST'))
def profile():
    global user_id
    if request.form.get('redirect') == '1':
        return redirect(url_for('guides'))
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return render_template('profile.html', user=user)


@app.route('/create/', methods=('GET', 'POST'))
def create():
    global user_id
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (byUser, title, content) VALUES (?, ?, ?)',
                         (user_id, title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('guides'))
    return render_template('create.html')


@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('edit.html', post=post)


@app.route('/<int:id>/view/', methods=('GET', 'POST'))
def view(id):
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts, user WHERE posts.id = ? AND posts.byUser = user.id', (id,)).fetchone()
    conn.close()
    return render_template('view-guide.html', posts=posts)


@app.route('/<int:id>/message/', methods=('GET', 'POST'))
def message(id):
    global user_id
    conn = get_db_connection()
    message = conn.execute('SELECT * FROM message, chat, user WHERE chat.id = ? AND message.inChat = chat.id AND user.id = message.byUser ORDER BY message.id DESC', (id,)).fetchall()
    if request.method == 'POST':
        message = request.form['message']

        if not message:
            flash('You need to write something.')
        else:
            conn.execute('INSERT INTO message (content, inChat, byUser) VALUES (?, ?, ?)',
                         (message, id, user_id))
            conn.commit()
            conn.close()
            return redirect(url_for('message', id=id))

    return render_template('message.html', message=message)


@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))
