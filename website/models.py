# -*- coding: utf-8 -*-

from . import db


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    media = db.Column(db.String(20), nullable=False)
    original_article = db.Column(db.String(80), nullable=False)
    doc_title = db.Column(db.String(30), nullable=False)
    doc_content = db.Column(db.Text, nullable=False)
    doc_datetime = db.Column(db.DateTime, nullable=False)
    like_count = db.Column(db.Integer, nullable=False)
    doc_url = db.Column(db.String(80), nullable=False)
    source = db.Column(db.String(30), nullable=False)
    customer = db.Column(db.String(20), nullable=False)
    request_seq = db.Column(db.Integer, nullable=False)
    doc_id = db.Column(db.String(30), nullable=False)
    analysis_id = db.Column(db.Integer, db.ForeignKey('analysis.id'),
                            nullable=False)
    termfrequencies = db.relationship('TermFrequency')


class TermFrequency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(20), nullable=False)
    frequency = db.Column(db.Integer, nullable=False)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'),
                            nullable=False)


class DocumentFrequency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(20), nullable=False)
    frequency = db.Column(db.Integer, nullable=False)


class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(20), nullable=False)
    documents = db.relationship('Document')
