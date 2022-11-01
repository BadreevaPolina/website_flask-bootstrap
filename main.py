import sys

from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap

from model import db, db_init, Post
from config import SQLITE_DATABASE_NAME

app = Flask(__name__)
bootstrap = Bootstrap(app)

# SQLAlchimy config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + SQLITE_DATABASE_NAME
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Init Database
db.app = app
db.init_app(app)


@app.route("/")
def index():
    posts = Post.query.order_by(Post.id.desc()).limit(4).all()
    return render_template('index.html', posts=posts)


@app.route("/add_post.html", methods=['GET', 'POST'])
def add_post():
    if request.method == "POST":
        name = request.form.get('name', type=str, default='')
        text = request.form.get('text', type=str, default='')
        if not name:
            return render_template('add_post.html')

        if not text:
            return render_template('add_post.html')

        p = Post(name=name, text=text)
        db.session.add(p)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_post.html')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "init":
            with app.app_context():
                db_init()
                exit(0)

    app.run(host='0.0.0.0', port=5000, debug=True)
