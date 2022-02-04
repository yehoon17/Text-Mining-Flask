# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, flash
from . import db
from website.models import Analysis, Document
from website.utils import *
from collections import Counter


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


@views.route("tf/<id>")
def tf(id):
    termfrequency = TermFrequency.query.filter_by(document_id=id).all()
    return render_template("tf.html", tf=termfrequency)


@views.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files['file']
        if file.filename == "":
            flash('No selected file')
        if file:
            if allowed_file(file.filename):
                analysis_id = add_analysis(file)
                for line in file:
                    document_id = add_document(line, analysis_id)
                    tf = Counter(preprocess(Document.query.filter_by(
                        id=document_id).first().doc_content))
                    add_tf(tf, document_id)
                flash('File uploaded')
            else:
                flash('not allowed extension')

    return render_template("upload.html")
