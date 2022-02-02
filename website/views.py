# -*- coding: utf-8 -*-

from flask import Blueprint, render_template


views = Blueprint("views", __name__)

@views.route("/")
def home():
    return render_template("home.html")

    
@views.route("/upload")
def upload():
    return render_template("upload.html")