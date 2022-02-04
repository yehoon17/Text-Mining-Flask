# -*- coding: utf-8 -*-

from email import message
from flask_restful import Api, Resource, abort, fields, marshal_with, reqparse
from website.models import DocumentFrequency, Document
import urllib.parse
from math import log
from . import db
from website.utils import preprocess, normalize
from collections import Counter

docfreq_fields = {
    "id": fields.Integer,
    "term": fields.String,
    "frequency": fields.Integer,
    "idf": fields.Float,
}

df_get_args = reqparse.RequestParser()
df_get_args.add_argument("term", type=str, required=True)

df_p_args = reqparse.RequestParser()
df_p_args.add_argument("term", type=str, required=True)
df_p_args.add_argument("frequency", type=int, required=True)
df_p_args.add_argument("idf", type=float)


class DocFreq(Resource):
    @marshal_with(docfreq_fields)
    def get(self):
        '''cmd에서 명령어 실행
        한글 문자열은 URL 인코딩
        예시)curl -X GET -H "Content-Type: application/json"^
             -d "{\"term\": \"%EC%9B%90%EB%82%B4%EB%8C%80%ED%91%9C\"}"^
             http://127.0.0.1:5000/api/df

        json 파일로 보내는 경우
        예시)curl -X GET -H "Content-Type: application/json"^
             -d @term.json http://127.0.0.1:5000/api/df

        '''
        term = urllib.parse.unquote(df_get_args.parse_args()["term"])
        if result := DocumentFrequency.query.filter_by(term=term).first():
            return result
        else:
            return abort(404, message=f"{term} does not exist in database")

    @marshal_with(docfreq_fields)
    def put(self):
        args = df_p_args.parse_args()
        term = urllib.parse.unquote(args["term"])
        if result := DocumentFrequency.query.filter_by(term=term).first():
            abort(409, message=f"{term} already exists in database")
        else:
            frequency = args["frequency"]
            idf = args["idf"]
            if not idf:
                n_doc = Document.query.count()
                idf = log(n_doc / (1 + frequency))
            df = DocumentFrequency(term=term, frequency=frequency, idf=idf)
            db.session.add(df)
            db.session.commit()
            return df, 201

    @marshal_with(docfreq_fields)
    def patch(self):
        args = df_p_args.parse_args()
        term = urllib.parse.unquote(args["term"])
        if result := DocumentFrequency.query.filter_by(term=term).first():
            result.frequency = args["frequency"]
            if idf := args["idf"]:
                result.idf = idf

            db.session.commit()
            return result
        else:
            abort(404, message=f"{term} doesn't exist, cannot update")


class DocFreq2(Resource):
    '''powershell에서 명령어 실행
    예시) curl http://127.0.0.1:5000/api/df/원내대표

    '''
    @marshal_with(docfreq_fields)
    def get(self, term: str):
        if result := DocumentFrequency.query.filter_by(term=term).first():
            return result
        else:
            return abort(404, message=f"{term} does not exist in database")

    @marshal_with(docfreq_fields)
    def delete(self, term: str):
        if result := DocumentFrequency.query.filter_by(term=term):
            result.delete()
            db.session.commit()
            return '', 204
        else:
            abort(404, message=f"{term} doesn't exist, cannot delete")


tfidf_args = reqparse.RequestParser()
tfidf_args.add_argument("text", type=str, required=True)

class TFIDF(Resource):
    def get(self):
        text = urllib.parse.unquote(tfidf_args.parse_args()["text"])
        text = preprocess(text)
        tf = Counter(text)
        tfidf = []
        for term in tf:
            if df := DocumentFrequency.query.filter_by(term=term).first():
                idf = df.idf
            else:
                idf =  log((Document.query.count() + 1) / 2)
            tfidf.append([term, idf * tf[term]])
        tfidf = normalize(tfidf, 100)
        tfidf.sort(key=lambda x: x[1], reverse=True)
        return tfidf


def api(app):
    api_ = Api(app)

    api_.add_resource(DocFreq, "/api/df")
    api_.add_resource(DocFreq2, "/api/df/<string:term>")
    api_.add_resource(TFIDF, "/tfidf")
