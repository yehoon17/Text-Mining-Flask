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


@views.route("/df")
def df():
    df = DocumentFrequency.query.all()
    n_doc = Document.query.count()
    return render_template("df.html", df=df, n_doc=n_doc)


@views.route("/documents/<id>")
def view_document(id):
    documents = Document.query.filter_by(analysis_id=id).all()
    return render_template("articles.html", documents=documents)


@views.route("/detail/<id>")
def detail(id):
    document = Document.query.filter_by(analysis_id=id).first()
    return render_template("detail.html", document=document)


@views.route("/detail/tf/<id>")
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
                df_counter = Counter()
                analysis_id = add_analysis(file)
                for line in file:
                    document_id = add_document(line, analysis_id)
                    tf = Counter(preprocess(Document.query.filter_by(
                        id=document_id).first().doc_content))
                    add_tf(tf, document_id)
                    df_counter.update(set(tf))
                update_df(df_counter)
                db.session.commit()
                flash('File uploaded')
            else:
                flash('not allowed extension')

    return render_template("upload.html")
