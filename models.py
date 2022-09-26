from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import json
from flask_cors import CORS
import hashlib

app = Flask("app")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///profile.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)
CORS(app)


class Authentication(db.Model):
    __tablename__ = "auth"
    user = db.Column(db.String(50), primary_key=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __str__(self):
        # return json.dumps(obj={"user": self.user, "password": hashlib.md5(self.password.encode()).hexdigest()},
        #                   indent=4)
        return json.dumps(obj={"user": self.user, "password": self.password},
                          indent=4)


class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    comment = db.Column(db.String(1000), nullable=False)

    def __str__(self):
        return json.dumps(obj={"id": self.id, "name": self.name, "comment": self.comment}, indent=4)


class Certificates(db.Model):
    __tablename__ = "certificates"
    title = db.Column(db.String(50), nullable=False)
    company = db.Column(db.String(50), nullable=False)
    birth = db.Column(db.String(50), nullable=False)
    expiration = db.Column(db.String(50), nullable=False)
    credentialId = db.Column(db.String(50), nullable=False, primary_key=True)
    link = db.Column(db.String(100), nullable=False)

    def __str__(self):
        return json.dumps(
            obj={"title": self.title, "company": self.company, "birth": self.birth, "expiration": self.expiration,
                 "credentialId": self.credentialId, "link": self.link}, indent=4)


class Projects(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    company = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(50))
    url = db.Column(db.String(50))

    def __str__(self):
        return json.dumps(
            {"id": self.id, "title": self.title, "company": self.company, "description": self.description,
             "url": self.url}, indent=4)


class Content(db.Model):
    __tablename__ = "content"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(50), nullable=False)
    thumbnail = db.Column(db.String(2000), nullable=False)
    link = db.Column(db.String(2000), nullable=False)

    def __str__(self):
        return json.dumps(
            obj={"id": self.id, "title": self.title, "description": self.description, "thumbnail": self.thumbnail,
                 "link": self.link}, indent=4)


class Gallery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.String(200))
    link = db.Column(db.String(2000), nullable=False)

    def __str__(self):
        return json.dumps(
            obj={"id": self.id, "caption": self.caption, "link": self.link}, indent=4)


if __name__ == '__main__':
    db.create_all()
