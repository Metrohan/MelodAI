
import tensorflow as tf
from music21 import note
import numpy as np

class LSTMComposer:
    def __init__(self, note_to_int, int_to_note):
        self.note_to_int = note_to_int
        self.int_to_note = int_to_note
        self.model = self.create_lstm_model()

    def create_lstm_model(self):
        model = tf.keras.Sequential()
        model.add(tf.keras.layers.LSTM(128, input_shape=(32, 1), return_sequences=True))
        model.add(tf.keras.layers.Dropout(0.3))
        model.add(tf.keras.layers.LSTM(128))
        model.add(tf.keras.layers.Dense(64, activation='relu'))
        model.add(tf.keras.layers.Dense(len(self.note_to_int), activation='softmax'))
        model.compile(loss='categorical_crossentropy', optimizer='adam')
        return model
    
    def sample_with_temperature(self, preds, temperature=1.0):
        preds = np.asarray(preds).astype('float64')
        preds = np.log(preds + 1e-9) / temperature
        exp_preds = np.exp(preds)
        preds = exp_preds / np.sum(exp_preds)
        probas = np.random.multinomial(1, preds, 1)
        return np.argmax(probas)

    def generate_melody(self, seed, length=64, temperature=1.0):
        pattern = seed[:]
        output_notes = []
        for _ in range(length):
            input_seq = np.reshape(pattern, (1, len(pattern), 1)) / float(len(self.note_to_int))
            prediction = self.model.predict(input_seq, verbose=0)[0]
            index = self.sample_with_temperature(prediction, temperature)
            result_note = self.int_to_note[index]
            output_notes.append(note.Note(midi=result_note))
            pattern.append(index)
            pattern = pattern[1:]
        return output_notes

