import os
import flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

app = flask.Flask(__name__)
app.secret_key = os.urandom(16)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class TVShow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tv_show_name = db.Column(db.String(128))

db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    tvshows = TVShow.query.all()
    num_shows = len(tvshows)
    return flask.render_template(
        "index.html",
        num_shows = num_shows,
        tvshows = tvshows
    )

@app.route("/show_added", methods=["GET", "POST"])
def show_added():
    if flask.request.method == "POST":
        data = flask.request.form
        new_show = TVShow(
            tv_show_name = data["savetvshow"]
        )
        if (TVShow.query.filter_by(tv_show_name=new_show.tv_show_name).first()) is None:
            db.session.add(new_show)
            db.session.commit()
        else:
            return flask.redirect("/")

    tvshows = TVShow.query.all()
    num_shows = len(tvshows)
    return flask.render_template(
        "index.html",
        num_shows = num_shows,
        tvshows = tvshows
    )

@app.route("/show_deleted", methods=["GET", "POST"])
def show_deleted():
    if flask.request.method == "POST":
        data = flask.request.form
        old_show = TVShow.query.filter_by(tv_show_name=data["deletetvshow"]).first()
        if old_show is not None:
            db.session.delete(old_show)
            db.session.commit()
        else:
            return flask.redirect("/")

    tvshows = TVShow.query.all()
    num_shows = len(tvshows)
    return flask.render_template(
        "index.html",
        num_shows = num_shows,
        tvshows = tvshows
    )

app.run(debug=True)