from flask import Flask, flash, render_template, request, jsonify, redirect, session, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
import speech_recognition as sr
import os
import asyncio
from sqlalchemy.dialects.sqlite import BLOB
from sqlalchemy import Column, Integer, String
from cloud_storage import upload, download
from werkzeug.datastructures import ImmutableMultiDict
from speech_rating_app import rate
import psycopg2

ALLOWED_EXTENSIONS = {'wav'}
app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:5432@localhost/xise'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Employee(db.Model):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    speech_file = Column(String(200))

    def __init__(self, speech_file):
        self.speech_file = speech_file


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@ app.route('/speech/audio/rating/<id>', methods=['GET'])
def audio_rating(id):
    id = request.view_args['id']

    employee = db.session.query(Employee).filter_by(id=id).first()
    file = download(employee.speech_file)

    rating = asyncio.rate(rate(employee.speech_file))
    os.remove(employee.speech_file)
    return jsonify({"rating": rating}), 200


@ app.route('/speech/audio/upload', methods=['POST'])
def audio_upload():
    if 'file' not in request.files:
        return jsonify('No file present'), 400
    file = request.files['file']

    if file.filename == '':
        return jsonify('No selected file'), 400

    if allowed_file(file.filename):
        filename = upload(file)
        employee = Employee(filename)
        db.session.add(employee)
        db.session.commit()
        inserted_id = employee.id
        # obj = wave.open('files/hindi_included.wav', 'r')

        return jsonify({"id": inserted_id}), 201
    else:
        return jsonify("No wav file found"), 400


# if __name__ == "__main__":
#     app.secret_key = 'super secret key'
#     # app.config['SESSION_TYPE'] = 'filesystem'
#     app.run(debug=True)
