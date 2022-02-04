# -*- coding: utf-8 -*-

from email import message
from flask_restful import Api, Resource, abort, fields, marshal_with, reqparse
from website.models import DocumentFrequency
import urllib.parse

docfreq_fields = {
    "id": fields.Integer,
    "term": fields.String,
    "frequency": fields.Integer,
    "idf": fields.Float,
}

df_get_args = reqparse.RequestParser()
df_get_args.add_argument("term", type=str, required=True)


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
    def put(self, term: str, frequency: int):
        pass

    @marshal_with(docfreq_fields)
    def patch(self, term: str, frequency: int):
        pass

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


def api(app):
    api_ = Api(app)

    api_.add_resource(DocFreq, "/api/df")
    api_.add_resource(DocFreq2, "/api/df/<string:term>")
