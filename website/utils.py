# -*- coding: utf-8 -*-

import json
from datetime import datetime
from . import db
from website.models import Analysis, Document, TermFrequency
from werkzeug.utils import secure_filename
import re
from collections import Counter


class NotValidPreprocessOptionError(Exception):
    def __init__(self):
        super().__init__("NotValidPreprocessOptionError")


ALLOWED_EXTENSIONS = {"json"}


def allowed_file(filename):
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def add_analysis(file) -> int:
    filename = secure_filename(file.filename)
    new_analysis = Analysis(filename=filename)
    db.session.add(new_analysis)
    db.session.commit()
    return new_analysis.id


def add_document(line: str, analysis_id: int) -> int:
    new_document = to_doc(line, analysis_id)
    db.session.add(new_document)
    db.session.commit()
    return new_document.id


def to_doc(line: str, analysis_id: int) -> Document:
    '''json 형식의 string을 Document 클래스로 변환

    '''
    data = json.loads(line)
    data["doc_datetime"] = datetime.strptime(
        data["doc_datetime"], "%Y-%m-%dT%H:%M:%S")
    new_document = Document(analysis_id=analysis_id, **data)
    return new_document


def preprocess(text: str, preprocess_option=2) -> list:
    '''Preprocess text by option.
    1: Remove special character
    2: Remove all except Korean

    Inputs a string and outputs list of tokens.

    '''
    if preprocess_option == 1:
        text = re.sub("[^A-Za-z0-9ㄱ-ㅎ가-힣\s]+", " ", text)
    elif preprocess_option == 2:
        text = re.sub("[^ㄱ-ㅎ가-힣\s]+", " ", text)
    else:
        raise NotValidPreprocessOptionError

    # Split sentences by space
    preprocessed_text = text.strip().split()

    return preprocessed_text


def add_tf(tf: Counter, document_id: int):
    for term in tf:
        new_tf = TermFrequency(
            term=term, frequency=tf[term], document_id=document_id)
        db.session.add(new_tf)
        db.session.commit()