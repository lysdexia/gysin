# -*- coding: utf-8 -*-
import uuid
from flask import Flask, render_template, abort, request, session, redirect, url_for
from flaskext.auth import AuthUser, permission_required, logout
from flaskext.auth.models.sa import get_user_class
from flask_mail import Message
from gysin.Models import Poesy, Email

def countlimit(count, offset, limit):
    more = None
    less = None

    if count - (offset + limit) > 0:
        more = {
                "offset": offset + limit,
                "limit": limit,
                }

    if offset - limit >= 0:
        less = {
                "offset": offset - limit,
                "limit": limit,
                }

    return more, less

def routes(app, db, mail):
    User = get_user_class(db.Model)

    @app.route("/admin/create", methods=["GET", "POST",])
    def admin_create():
        try:
            db.create_all()
        except Exception as error:
            print(error)

        if request.method == 'POST':

            key = request.form['key']
            if not key == app.config["ADMIN_SECRET_KEY"]:
                return 'Bogus key.'

            username = request.form['username']
            if User.query.filter(User.username==username).first():
                return 'User already exists.'

            email = request.form['email']
            if Email.query.filter(Email.email==email).first():
                return 'Email already exists.'

            role = request.form["role"]

            if not role in ["admin", "user"]:
                return "Role not found."

            password = request.form['password']
            user = User(username=username, password=password, role=role)
            email = Email(username=username, email=email)
            db.session.add(user)
            db.session.add(email)
            db.session.commit()
            return redirect(url_for('index'))
        return render_template("admin/new-user.html")

    @app.route("/")
    def index():
        poems = Poesy.query.order_by(Poesy.id.desc())[0:5]
        return render_template("index.html", poems=poems)

    @app.route("/titles")
    def enumerate_titles():
        return redirect(url_for("titles", offset=0, limit=5))

    @app.route("/titles/<int:offset>/<int:limit>")
    def titles(offset, limit):
        poems = Poesy.query.order_by(Poesy.id.desc())[offset:offset + limit]
        count = Poesy.query.count()
        more, less = countlimit(count, offset, limit)
        return render_template(
                "titles.html",
                poems=poems,
                more=more,
                less=less,
                )
   
    @app.route("/authors")
    def enumerate_authors():
        return redirect(url_for("authors", offset=0, limit=5))

    @app.route("/authors/<int:offset>/<int:limit>")
    def authors(offset, limit): 
        authors = Email.query.with_entities(Email.username)\
                .order_by(Email.username)[offset: offset + limit]
        authors = [author[0] for author in authors]
        count = Email.query.count()
        more, less = countlimit(count, offset, limit)
        return render_template(
                "authors.html",
                authors=authors,
                more=more,
                less=less,
                ) 

    @app.route("/by-author/<string:author>")
    def enumerate_by_author(author):
        return redirect(url_for("by_author", author=author, offset=0, limit=5))

    @app.route("/by-author/<string:author>/<int:offset>/<int:limit>")
    def by_author(author, offset, limit): 
        poems = Poesy.query.filter(Poesy.author==author)\
                .order_by(Poesy.id.desc())[offset: offset + limit]
        count = Poesy.query.filter(Poesy.author==author).count()
        more, less = countlimit(count, offset, limit)
        path = "/".join(request.path.split("/")[0:3])
        return render_template(
                "by-author.html",
                poems=poems,
                author=author,
                more=more,
                less=less,
                )

    @app.route("/edit")
    def edit():
        return render_template("edit.html");

    @app.route("/what-is-this")
    def what():
        return render_template("what-is-this.html");

    @app.route("/read/<string:id>")
    def read(id):
        poem = Poesy.query.filter(Poesy.id==id).first()
        poem.body = "\n".join(poem.body.split("  "))
        return render_template("read.html", poem=poem);

    @app.route("/publish", methods=["POST",])
    def publish():
        title = request.form["title"]
        body = request.form["body"]

        if not all([title, body]):
            return render_template("error.html");

        session["title"] = title
        session["body"] = body
        session["next"] = "save"

        return redirect(url_for('save'))

    @app.route("/signup", methods=["POST"])
    def signup():
        print(app.config["MAIL_USERNAME"])
        email = request.form["email"]
        if not email:
            return "no email"

        message = Message(
                "Sign up for Gysin",
                sender="doug.shawhan@gmail.com",
                recipients = [email],
                )

        message.html = """
        <p>how nice of you to <a href=https://gysin.com/signup/%s>sign up.</a>
        """%str(uuid.uuid4())
        mail.send(message)
        return render_template("auth/signup-thanks.html", email=email)

    @app.route("/login", methods=["GET", "POST",])
    def login():
        if request.method == "POST":
            username = request.form["username"]
            session["username"] = username

            try:
                user = User.query.filter(User.username==username).one()
            except Exception as error:
                return render_template(
                        "auth/login.html",
                        error = "Incorrect user name or password.",
                        username=username)

            if user is not None:
                if not user.authenticate(request.form["password"]):
                    return render_template(
                        "login.html",
                        error = "Incorrect user name or password.",
                        username=username)

                # hey! We are logged in!
                session["logged_in"] = True

                # redirect us to our "next" page in session 
                next_page = session.get("next")
                if next_page:
                    # don't keep "next" page around
                    session["next"] = None
                    return redirect(url_for(next_page))
                return redirect(url_for("index"))

        return render_template("auth/login.html")

    @app.route("/logout")
    def logmeout():
        logout()
        session["username"] = False
        session["logged_in"] = False
        session["next"] = None
        return render_template("auth/logout.html")

    @permission_required(resource="create", action="poem")
    def save():
        username = session["username"]
        title = session["title"]
        body = session["body"]

        poem = Poesy(
                author=username,
                title=title,
                body=body,
                )
        db.session.add(poem)
        db.session.commit()
        
        body = "\n".join(body.split("  "))
        return render_template("save.html", body=body, title=title, id=poem.id);
    app.add_url_rule("/save", "save", save)
