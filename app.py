from flask import *
from models import *
import json
import hashlib


def login_required(func):
    def wrapper(*args, **kwargs):
        user = request.args.get("user")
        password = request.args.get("password")
        if Authentication.query.filter_by(user=user, password=password).first():
            return func(*args, **kwargs)
        else:
            abort(401)
    return wrapper

@app.route("/", methods=["GET"])
def home():
    data = {"result": True, "status": 202, "message": "Backend API for Website https://profile.tahsinayman.repl.co"}
    return jsonify(data), 202

@app.route("/comments/", methods=["GET"])
def comments():
    return jsonify([json.loads(i.__str__()) for i in Comment.query.all()]), 202

@app.route("/comments/add/", methods=["POST"])
def add_comment():
    try:
        data = request.get_json(force=True)
        com = Comment(id=data.get("id"), name=data.get("name"), comment=data.get("comment"))
        db.session.add(com)
        db.session.commit()
        return jsonify({"result": True, "status": 202, "message": "Successfully Added Comment"}), 202
    except Exception:
        abort(406, "Couldn't Add Comment")

@app.route("/certificates/", methods=["GET"])
def certificates():
    return jsonify([json.loads(i.__str__()) for i in Certificates.query.all()]), 202

@login_required
@app.route("/certificates/add/", methods=["POST"])
def add_certificates():
    try:
        data = request.get_json(force=True)
        certificate = Certificates(title=data.get("title"), company=data.get("company"), birth=data.get("birth"), expiration=data.get("expiration"), credentialId=data.get("credentialId"), link=data.get("link"))
        db.session.add(certificate)
        db.session.commit()
        return jsonify({"result": True, "status": 202, "message": "Successfully Added Certificate"}), 202
    except Exception:
        abort(406, "Couldn't Add Certificates")

@app.route("/projects/", methods=["GET"])
def projects():
    return jsonify([json.loads(i.__str__()) for i in Projects.query.all()]), 202

@login_required
@app.route("/projects/add/", methods=["POST"])
def add_project():
    try:
        data = request.get_json(force=True)
        project = Projects(id=data.get("id"), title=data.get("title"), company=data.get("company"), description=data.get("description"), url=data.get("url"))
        db.session.add(project)
        db.session.commit()
        return jsonify({"result": True, "status": 202, "message": "Successfully Added Projects"}), 202
    except Exception:
        abort(406, "Couldn't Add Projects")
@app.errorhandler(406)
def error_406(error):
    return jsonify({"result": False, "status": 406, "message": f"{error}"}), 406

@app.errorhandler(405)
def error_405(error):
    return jsonify({"result": False, "status": 405, "message": f"{request.method} method is not Allowed"}), 405


@app.errorhandler(404)
def error_404(error):
    return jsonify({"result": False, "status": 404, "message": "URL is Not Valid"}), 404

@app.errorhandler(401)
def error_401(error):
    return jsonify({"result": False, "status": 401, "message": "Unauthorized"}), 401


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)