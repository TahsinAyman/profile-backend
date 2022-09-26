import os

from flask import *
from models import *
import json
import hashlib
from models import *
import random

ALLOWED_EXTENSIONS = {"jpg", "png", "gif", "jpeg", "webp"}
app.secret_key = "0bcc0dd770173491c51453c1eb2b8486" + str(random.randint(1, 10000))
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
app.config["UPLOAD_FOLDER"] = "static/images"


def login_required(func):
    def wrapper(*args, **kwargs):
        user = request.args.get("user")
        password = request.args.get("password")
        if Authentication.query.filter_by(user=user, password=password).first():
            return func(*args, **kwargs)
        else:
            abort(401)

    return wrapper


@app.route("/admin/auth/", methods=["POST"])
def admin_authorization():
    try:
        data = request.get_json(force=True)
        password = data.get("password")
        auth = Authentication.query.filter_by(user=data.get("user"),
                                              password=hashlib.md5(password.encode()).hexdigest()).first()
        if auth:
            token = hashlib.md5(str(auth.user + auth.password).encode()).hexdigest()
            return jsonify({"result": True, "message": "Successfully Logged In", "token": token})
        else:
            raise Exception
    except Exception:
        return jsonify({"result": False, "message": "Wrong Credential Provided"})


@app.route("/check/auth/", methods=["POST"])
def check_auth():
    try:
        token = request.get_json(force=True).get("token")
        auth = [hashlib.md5(str(y.get("user") + y.get("password")).encode()).hexdigest() for y in
                (json.loads(i.__str__()) for i in Authentication.query.all())]
        if token in auth:
            return jsonify({"result": True, "message": "Correct Token Data"})
        else:
            raise Exception
    except Exception:
        return jsonify({"result": False, "message": "Wrong Token Data"})


@app.route("/", methods=["GET"])
def home():
    data = {"result": True, "status": 202, "message": "Backend API for Website https://touhida.rowshan.net/"}
    return jsonify(data), 202


def get_comments():
    pages = []
    comments_data = [json.loads(i.__str__()) for i in Comment.query.all()]
    for i in range(0, len(comments_data), 3):
        pages.append(comments_data[i: i + 3])

    new_pages = {}
    for i in range(1, len(pages) + 1):
        new_pages[i] = pages[i - 1]

    return new_pages


@app.route("/profile/card/", methods=["GET"])
def get_profile_card_text():
    with open("data/profileText.json") as file:
        data = json.load(file)
    return jsonify(data)


@app.route("/content/", methods=["GET"])
def get_content():
    try:
        return jsonify([json.loads(i) for i in Content.query.all()])
    except Exception:
        return jsonify([])


@app.route("/comments/", methods=["GET"])
def comments():
    try:
        page = request.args.get("page")
        comments_data = get_comments()
        comments_result = None

        if not page:
            return jsonify(
                {"result": True, "data": [json.loads(i.__str__()) for i in Comment.query.all()], "pages": len(
                    comments_data)})

        for i in comments_data:
            if int(i) == int(page):
                comments_result = comments_data[i]

        return jsonify({"result": True, "message": f"Page No {page}", "data": comments_result, "pages": len(
            comments_data)})
    except Exception:
        return jsonify({"result": False, "data": []})


@app.route("/profile/card/image/", methods=["POST"])
def upload_file():
    if "image" not in request.files:
        return jsonify({"result": False, 'message': "File Was Not provided"})
    else:
        files = request.files.getlist('image')
        errors = {}
        success = False

        for file in files:
            if file:
                filename = file.filename
                if filename.split(".")[-1] not in ALLOWED_EXTENSIONS:
                    return jsonify({"result": False, "message": "Wrong File Extensions"})
                filename = "cover.jpg"
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                success = True
            else:
                errors[file.filename] = "File Type is Not Allowed"

        if success and errors:
            errors["message"] = "File successfully Uploaded"
            errors["result"] = True
            return jsonify(errors)
        if success:
            errors["message"] = "File successfully Uploaded"
            errors["result"] = True
            return jsonify(errors)
        else:
            errors["result"] = False
            return jsonify(errors)


@app.route("/profile/card/edit/", methods=["PUT"])
def edit_profile_card():
    try:
        data = request.get_json(force=True)
        if data.get("name"):
            with open("data/profileText.json") as file:
                profile_data = json.load(file)
            profile_data["name"] = data.get("name")
            with open("data/profileText.json", "w") as file:
                json.dump(fp=file, indent=4, obj=profile_data)
        if data.get("designation"):
            with open("data/profileText.json") as file:
                profile_data = json.load(file)
            profile_data["designation"] = data.get("designation")
            with open("data/profileText.json", "w") as file:
                json.dump(fp=file, indent=4, obj=profile_data)
        if data.get("company"):
            with open("data/profileText.json") as file:
                profile_data = json.load(file)
            profile_data["company"] = data.get("company")
            with open("data/profileText.json", "w") as file:
                json.dump(fp=file, indent=4, obj=profile_data)
        return jsonify({"result": True, "message": "Successfully Updated"})
    except Exception as e:
        return jsonify({"result": False, "message": f"Couldn't Update"})


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
        certificate = Certificates(title=data.get("title"), company=data.get("company"), birth=data.get("birth"),
                                   expiration=data.get("expiration"), credentialId=data.get("credentialId"),
                                   link=data.get("link"))
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
        project = Projects(id=data.get("id"), title=data.get("title"), company=data.get("company"),
                           description=data.get("description"), url=data.get("url"))
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
    return jsonify({"result": False, "status": 405, "message": f"{request.method} method is not Allowed"}), 202


@app.errorhandler(404)
def error_404(error):
    return jsonify({"result": False, "status": 404, "message": "URL is Not Valid"}), 202


@app.errorhandler(401)
def error_401(error):
    return jsonify({"result": False, "status": 401, "message": "Unauthorized"}), 202


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
