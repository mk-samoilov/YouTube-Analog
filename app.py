from flask import Flask
from flask import render_template, request, redirect, session

from config import *
from databaser import Database


app = Flask(__name__)
app.secret_key = SECRET_KEY

@app.route("/")
def p_index():
    db = Database()
    try:
        user = db.get_acc_by_uuid(_uuid=session["uuid"])
    except KeyError:
        user = None

    db = Database()
    videos = db.get_videos()

    return render_template("index.html", videos=videos, user=user)

@app.route("/video/<vid>")
def p_video(vid):
    db = Database()
    try:
        user = db.get_acc_by_uuid(_uuid=session["uuid"])
    except KeyError:
        user = None

    db = Database()
    video = db.get_video(vid)

    if video is None:
        return redirect("/")

    return render_template("video_page.html", video=video, user=user)


@app.route(rule="/profile")
def p_profile():
    db = Database()
    try:
        user = db.get_acc_by_uuid(_uuid=session["uuid"])
    except KeyError:
        user = None

    return render_template("profile.html", user=user)


# @app.route(rule="/upload_video", methods=["GET", "POST"])
# def p_upload_video():
#     db = Database()
#     try:
#         user = db.get_acc_by_uuid(_uuid=session["uuid"])
#     except KeyError:
#         user = None
#
#     if user:
#         if request.method == "POST":
#             name = request.form["name"]
#             desc = request.form["name"]
#
#             if file_video and file_preview:
#                 pass
#
#             author_name = user[1]
#
#             db = Database()
#             db.add_video(name=name, desc=desc, author_name=author_name)
#
#         else:
#             return render_template("upload_video.html", user=user, message=None)
#
#     else:
#         return redirect("/login")


@app.route(rule="/login", methods=["GET", "POST"])
def p_login():
    db = Database()
    try:
        user = db.get_acc_by_uuid(_uuid=session["uuid"])
    except KeyError:
        user = None

    if not user:
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            db = Database()
            _user = db.get_acc_by_username(username)

            if _user and password == _user[2]:
                session["uuid"] = _user[4]

                return redirect("/")

            return render_template("login.html", user=user, message="Uncorrected password or account not found!")

        else:
            return render_template("login.html", user=user, message=None)

    else:
        return redirect("/")


@app.route("/logout")
def logout():
    session["uuid"] = None
    return redirect("/")

@app.route(rule="/register", methods=["GET", "POST"])
def p_reg():
    db = Database()
    try:
        user = db.get_acc_by_uuid(_uuid=session["uuid"])
    except KeyError:
        user = None

    if not user:
        if request.method == "POST":
            username = str(request.form["username"])
            email = str(request.form["email"])
            password = str(request.form["password"])
            confirm_password = str(request.form["confirm_password"])

            print(username)

            if password == confirm_password:
                db = Database()
                db.create_acc(username, password, email)
                return redirect("/login")

            else:
                return render_template("reg.html", user=user, message="The password is equal to the verification password!")

        else:
            return render_template("reg.html", user=user, message=None)

    else:
        return redirect("/")


@app.route(rule="/video/<vid>/like", methods=["POST"])
def like_video(vid):
    vid = int(vid)

    db = Database()
    db.like_video(vid)

    return "accepted"

@app.route("/video/<vid>/dislike", methods=["POST"])
def dislike_video(vid):
    vid = int(vid)

    db = Database()
    db.dislike_video(vid)

    return "accepted"


if __name__ == "__main__":
    app.run(
        host=SERVER_HOST,
        port=SERVER_PORT,
        debug=DEBUG_MODE
    )