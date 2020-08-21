import tensorflow as tf

print("tensorflow version: " + str(tf.__version__))

from tensorflow.keras import layers
from tensorflow.keras import Model

tf.keras.backend.set_floatx('float64')

class MusicGenreModel_v0(tf.keras.Model):
    def __init__(self):
        super(MusicGenreModel_v0, self).__init__()

        self.lstm0 = layers.LSTM(128, activation="tanh", recurrent_activation="sigmoid", return_sequences=False)
        self.dense0 = layers.Dense(10, activation="softmax")

    def call(self, x):
        x = self.lstm0(x)
        x = self.dense0(x)
        return x

class MusicGenreModel_v1(tf.keras.Model):
    # def __init__(self):
    #     super(MusicGenreModel, self).__init__()

    #     self.linear0 = Dense(8, activation=None)

    # def call(self, x):
    #     x = self.linear0(x)
    #     return x

    def __init__(self):
        super(MusicGenreModel_v1, self).__init__()

        self.lstm0 = layers.LSTM(512, activation="tanh", recurrent_activation="sigmoid", return_sequences=False)
        self.dense0 = layers.Dense(64, activation="relu")
        self.dense1 = layers.Dense(10, activation="softmax")

    def call(self, x):
        x = self.lstm0(x)
        x = self.dense0(x)
        x = self.dense1(x)
        return x

class MusicGenreModel_v2(tf.keras.Model):
    def __init__(self):
        super(MusicGenreModel_v2, self).__init__()

        self.lstm0 = layers.LSTM(64, activation="tanh", recurrent_activation="sigmoid", return_sequences=False)
        self.dense0 = layers.Dense(32, activation="relu")
        self.dense1 = layers.Dense(32, activation="relu")
        self.dense2 = layers.Dense(10, activation="softmax")

    def call(self, x):
        x = self.lstm0(x)
        x = self.dense0(x)
        x = self.dense1(x)
        x = self.dense2(x)
        return x