# -*- coding: utf-8 -*-

from email import message
from flask_restful import Api, Resource, abort, fields, marshal_with
from website.models import DocumentFrequency


docfreq_fields = {
    "id": fields.Integer,
    "term": fields.String,
    "frequency": fields.Integer,
    "idf": fields.Float,
}


class DocFreq(Resource):
    @marshal_with(docfreq_fields)
    def get(self, term: str):
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


def api(app):
    api_ = Api(app)

    api_.add_resource(DocFreq, "/api/df/<string:term>")
