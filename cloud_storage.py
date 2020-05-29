import pyrebase
import time

config = {
    "apiKey": "AIzaSyB3_LJjwTrWL_5Qffaeo1gekMmqCW7_qGw",
    "authDomain": "speech-analyzer-5e833.firebaseapp.com",
    "databaseURL": "https://speech-analyzer-5e833.firebaseio.com",
    "projectId": "speech-analyzer-5e833",
    "storageBucket": "speech-analyzer-5e833.appspot.com",
    "messagingSenderId": "108483703406",
    "appId": "1:108483703406:web:e6f192c993aca4b6e5ac7f",
    "measurementId": "G-5DRYXJ2N6D"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()


def upload(file):

    milli_sec = int(round(time.time() * 1000))
    f = file.filename.split('.')
    filename = f[0] + '_' + str(milli_sec)+'.'+f[1]
    cloud_path = "files/"+filename
    storage.child(cloud_path).put(file)
    return filename


def download(filename):
    cloud_path = "files/"+filename
    return storage.child(cloud_path).download(filename)
