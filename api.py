from flask import Flask, request, current_app, send_file, jsonify

import tensorflow as tf
import numpy as np

from tensorflow.keras import layers, regularizers

model = tf.keras.models.Sequential()

graph = tf.get_default_graph()

val = 0.005

model.add(layers.InputLayer(input_shape=(32, 32, 3)))
#model.add(layers.RandomCrop(25, 25))
#model.add(layers.RandomZoom((0, 0.4)))
model.add(layers.Conv2D(activation='relu', kernel_size=3, filters=16, strides=1, padding='same', use_bias=True, kernel_regularizer=regularizers.l2(val)))
model.add(layers.BatchNormalization())
model.add(layers.Conv2D(activation='relu', kernel_size=3, filters=16, strides=1, padding='same', use_bias=True, kernel_regularizer=regularizers.l2(val)))
model.add(layers.BatchNormalization())
model.add(layers.Conv2D(activation='relu', kernel_size=3, filters=16, strides=1, padding='same', use_bias=True, kernel_regularizer=regularizers.l2(val)))
model.add(layers.MaxPool2D(pool_size=2, strides=2, padding='same'))
model.add(layers.BatchNormalization())
model.add(layers.Conv2D(activation='relu', kernel_size=3, filters=16, strides=1, padding='same', use_bias=True, kernel_regularizer=regularizers.l2(val)))
model.add(layers.BatchNormalization())
model.add(layers.Conv2D(activation='relu', kernel_size=3, filters=16, strides=1, padding='same', use_bias=True, kernel_regularizer=regularizers.l2(val)))
model.add(layers.BatchNormalization())
model.add(layers.Conv2D(activation='relu', kernel_size=3, filters=16, strides=1, padding='same', use_bias=True, kernel_regularizer=regularizers.l2(val)))
model.add(layers.MaxPool2D(pool_size=2, strides=2, padding='same'))
model.add(layers.BatchNormalization())
model.add(layers.Conv2D(activation='relu', kernel_size=3, filters=16, strides=1, padding='same', use_bias=True, kernel_regularizer=regularizers.l2(val)))
model.add(layers.BatchNormalization())
model.add(layers.Conv2D(activation='relu', kernel_size=3, filters=16, strides=1, padding='same', use_bias=True, kernel_regularizer=regularizers.l2(val)))
model.add(layers.BatchNormalization())
model.add(layers.Conv2D(activation='relu', kernel_size=3, filters=16, strides=1, padding='same', use_bias=True, kernel_regularizer=regularizers.l2(val)))
model.add(layers.MaxPool2D(pool_size=2, strides=2, padding='same'))
model.add(layers.Flatten())
model.add(layers.BatchNormalization())
#model.add(layers.Dropout(0.05))
model.add(layers.Dense(units=200, input_dim=256, activation='relu', use_bias=True, kernel_regularizer=regularizers.l2(val)))
model.add(layers.BatchNormalization())
model.add(layers.Dropout(0.5))
model.add(layers.Dense(units=100, input_dim=200, activation='relu', use_bias=True, kernel_regularizer=regularizers.l2(val)))
model.add(layers.BatchNormalization())
model.add(layers.Dropout(0.5))
model.add(layers.Dense(units=8, input_dim=100, activation='softmax', use_bias=True, kernel_regularizer=regularizers.l2(val)))

model.load_weights('models/final_noanimal_lowdimhighreg.h5')

app = Flask(__name__)

@app.route('/api/ml', methods=['GET', 'POST'])
def runml():
    data = request.json['data']
    input_data = np.zeros((1, 32, 32, 3), dtype=np.uint8)
    for j in range(32):
        for k in range(32):
            for l in range(3):
                input_data[0][j][k][l] = data[j][k][l]
    with graph.as_default():
        result = jsonify({"result": [str(x) for x in list(model.predict(input_data)[0])]})
    return result

@app.route('/')
def index():
    return current_app.send_static_file('index.html')

@app.route('/process')
def process():
    return current_app.send_static_file('process.html')

@app.route('/try')
def tryit():
    return current_app.send_static_file('try.html')

@app.route('/api/file/<filename>')
def getfile(filename):
    return send_file('static/' + filename)

app.run()