# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, flash
from werkzeug.utils import secure_filename
import json
from . import db
from website.models import Analysis, Document
from datetime import datetime


ALLOWED_EXTENSIONS = {"json"}


def allowed_file(filename):
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


views = Blueprint("views", __name__)


@views.route("/")
def home():
    return render_template("home.html")


@views.route("/documents")
def documents():
    analysis = Analysis.query.all()
    return render_template("documents.html", analysis=analysis)


@views.route("/documents/<id>")
def view_document(id):
    documents = Document.query.filter_by(analysis_id=id).all()
    return render_template("articles.html", documents=documents)


@views.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "":
            flash('No selected file')
        if file:
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                new_analysis = Analysis(filename=filename)
                db.session.add(new_analysis)
                db.session.commit()
                analysis_id = new_analysis.id
                for line in file:
                    db.session.add(to_doc(line, analysis_id))
                    db.session.commit()
                flash('File uploaded')
            else:
                flash('not allowed extension')

    return render_template("upload.html")


def to_doc(line, analysis_id):
    data = json.loads(line)
    data["doc_datetime"] = datetime.strptime(
        data["doc_datetime"], "%Y-%m-%dT%H:%M:%S")
    new_document = Document(analysis_id=analysis_id, **data)
    return new_document
