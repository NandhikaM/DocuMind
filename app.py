import os
from datetime import datetime

from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///documind.db"

db = SQLAlchemy(app)


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String, nullable=False)
    filepath = db.Column(db.String, nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)


@app.route("/")
def index():
    documents = os.listdir(app.config["UPLOAD_FOLDER"])
    return render_template("home.html", documents=documents)


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        # request.files is a dict-like object of uploaded files (FileStorage per form field name)
        file = request.files["file"]
        if file.filename:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)
            document = Document(filename=file.filename, filepath=filepath)
            db.session.add(document)
            db.session.commit()
        return redirect("/")
    return render_template("upload.html")


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()
