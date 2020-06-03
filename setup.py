from flask import Flask, flash, render_template, request, jsonify, redirect, session, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
import os
import json
from sqlalchemy import Column, Integer, String, Float
from noise_reduction import *
from werkzeug.datastructures import ImmutableMultiDict
from speech_rating_app import *
import psycopg2

ALLOWED_EXTENSIONS = {'wav'}
setup = Flask(__name__)

setup.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:5432@localhost/xise'
setup.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# setup.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(setup)


class Employee(db.Model):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    speech_file = Column(String(200))
    fluencyRating = Column(Float)
    spellingRating = Column(Float)
    fillerRating = Column(Float)
    grammarRating = Column(Float)
    totalRating = Column(Float)

    def __init__(self, speech_file, fluencyRating, spellingRating, fillerRating, grammarRating, totalRating):
        self.speech_file = speech_file
        self.fluencyRating = fluencyRating
        self.spellingRating = spellingRating
        self.fillerRating = fillerRating
        self.grammarRating = grammarRating
        self.totalRating = totalRating


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@ setup.route('/speech/audio/rating/<id>', methods=['GET'])
def audio_rating(id):
    id = request.view_args['id']

    employee = db.session.query(Employee).filter_by(id=id).first()
    if employee.totalRating == -1:
        speech_rater = rate(employee.speech_file)
        r_json = json.loads(speech_rater)
        os.remove(employee.speech_file)
        employee.fluencyRating = r_json["fluencyRating"]
        employee.spellingRating = r_json["spellingRating"]
        employee.fillerRating = r_json["fillerRating"]
        employee.grammarRating = r_json["grammarRating"]
        employee.totalRating = cr_json["totalRating"]
        db.session.commit()
        return speech_rater, 200
    return jsonify_object(employee), 200


def jsonify_object(employee):
    data_set = {
        "fluencyRating": employee.fluencyRating,
        "spellingRating": employee.spellingRating,
        "fillerRating": employee.fillerRating,
        "grammarRating": employee.grammarRating,
        "totalRating": employee.totalRating
    }
    return json.dumps(data_set)


@ setup.route('/speech/audio/upload', methods=['POST'])
def audio_upload():
    if 'file' not in request.files:
        return jsonify('No file present'), 400
    f = request.files['file']
    if allowed_file(f.filename):
        f.save(f.filename)
        employee = Employee(f.filename, -1, -1, -1, -1, -1)
        db.session.add(employee)
        db.session.commit()
        return jsonify({"id": employee.id}), 201
    else:
        return jsonify("No wav file found"), 400


if __name__ == "__main__":
    setup.run(debug=True)
