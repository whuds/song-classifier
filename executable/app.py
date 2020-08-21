import os
from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
import librosa as lb
from librosa.feature import mfcc
import tensorflow as tf
import numpy as np
import json

ALLOWED_EXTENSIONS = {'mp3', 'wav'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.')[-1].lower() in ALLOWED_EXTENSIONS


# Flask app config
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "audio"
app.config['JS'] = "static/js"
app.config['CSS'] = "static/css"
app.config['FAVICON'] = "static"

model_directory = "model.h5"
sample_rate = 22050

# Tuning Variables
genres = ['blues','classical','country','disco','hiphop','jazz','metal','pop','reggae','rock']
train_split = 0.8 # Percentage of data that will be used to train
segment_width = 0.2 # Length of each audio segment in seconds
num_frequencies = 128 # Number of frequency bins
max_frequency = 4000 # Frequencies above this value will not be included
num_epochs = 10 # Number of epochs to train with
training_data_used = 1.0 # Percentage of the training data that is used
test_data_used = 1.0 # Percentage of the test data that is used


model = tf.keras.models.load_model("model.h5")

# Routing for homepage, static files, and the uploader
@app.route('/', methods=["GET"])
def homepage():
    return render_template('index.html')

@app.route('/js/<path:path>', methods=["GET"])
def get_send_js(path):
    return send_from_directory(app.config['JS'], path)

@app.route('/css/<path:path>', methods=["GET"])
def get_send_css(path):
    return send_from_directory(app.config['CSS'], path)

@app.route('/favicon.ico', methods=["GET"])
def get_favicon():
    return send_from_directory(app.config['FAVICON'], "favicon.ico")


# Endpoint for uploading files
# Accepts files if it has an allowed extension
# Else raises an error
@app.route('/uploader', methods=["POST"])
def upload():
    f = request.files['file']
    filename = secure_filename(f.filename)
    if allowed_file(filename):
        print("Uploaded ", f)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # x , sr = lb.load(f)
        frames, sr = lb.load("audio/" + filename)
        prediction, confidence = predict_genre(frames, model)
        print(prediction, confidence)

        values_sorted = []
        g = genres.copy()
        c = confidence.copy().tolist()
        for _ in range(len(genres)):
            i = np.argmax(c)
            values_sorted.append({'confidence': c[i]*100, 'genre': g[i]})
            del c[i]
            del g[i]

        os.remove("audio/" + filename)
        results = {'data': values_sorted}
        return results
    else:
        raise ValueError(filename.rsplit('.', 1)[1].lower() + " is not an allowed file type.")


def predict_genre(frames, model):
    # Segment Data
    print("Segmenting data...")
    sample_size = int(sample_rate * segment_width)
    segments = []
    c = 0
    while True:
        start = c * sample_size
        end = start + sample_size
        if end >= len(frames) * training_data_used:
            break
        segments.append(frames[start:end])
        c += 1
    segments = np.array(segments)

    # Get mfcc of segments
    print("Taking MFCC of segments...")
    mfcc_arr = []
    for s in segments:
        mfcc_arr.append(mfcc(y=s, sr=sample_rate, n_mfcc=num_frequencies, fmax=max_frequency))
    mfcc_arr = np.array(mfcc_arr)

    # Predict each segment
    print("Making segment predictions...")
    counts = np.zeros(len(genres))
    predictions = np.argmax(model.predict(mfcc_arr), axis=1)
    for p in predictions:
        counts[p] += 1
    predictions = np.array(predictions)
    counts = np.array(counts)

    # Predict the overall genre
    genre_prediction = np.argmax(counts)
    confidence = counts / len(predictions)

    return genre_prediction, confidence

if __name__ == '__main__':
    app.run()
