from flask import Flask, flash, render_template, request, jsonify, redirect, session, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import Column, Integer, String
from cloud_storage import upload, download
from werkzeug.datastructures import ImmutableMultiDict
from speech_rating_app import rate
import psycopg2

ALLOWED_EXTENSIONS = {'wav'}
setup = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:5432@localhost/xise'
setup.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
setup.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(setup)


class Employee(db.Model):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    speech_file = Column(String(200))

    def __init__(self, speech_file):
        self.speech_file = speech_file


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@ setup.route('/speech/audio/rating/<id>', methods=['GET'])
def audio_rating(id):
    id = request.view_args['id']

    employee = db.session.query(Employee).filter_by(id=id).first()
    # file = download(employee.speech_file)

    rating = rate(employee.speech_file)
    os.remove(employee.speech_file)
    return jsonify({"rating": rating}), 200


@ setup.route('/speech/audio/upload', methods=['POST'])
def audio_upload():
    if 'file' not in request.files:
        return jsonify('No file present'), 400
    f = request.files['file']

    if f.filename == '':
        return jsonify('No selected file'), 400

    if allowed_file(f.filename):
        # filename = upload(file)
        # open("files/"+f.filename, 'w').write(f)
        f.save(f.filename)
        employee = Employee(f.filename)
        db.session.add(employee)
        db.session.commit()
        inserted_id = employee.id
        print(employee.speech_file)

        return jsonify({"id": inserted_id}), 201
    else:
        return jsonify("No wav file found"), 400


if __name__ == "__main__":
    setup.run(debug=True)
