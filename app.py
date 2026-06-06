import os

from flask import Flask, redirect, render_template, request

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        # request.files is a dict-like object of uploaded files (FileStorage per form field name)
        file = request.files["file"]
        if file.filename:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)
        return redirect("/")
    return render_template("upload.html")


if __name__ == "__main__":
    app.run()
