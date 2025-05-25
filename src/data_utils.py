
import numpy as np
import tensorflow as tf
from music21 import note, converter

def load_melody_midi(file_path):
    score = converter.parse(file_path)
    melody = []
    for el in score.flatten().notes:
        if isinstance(el, note.Note):
            melody.append((el.pitch.midi, el.quarterLength))
    return melody

def prepare_sequences(melody, seq_length=32):
    notes = [m for (m, d) in melody]
    unique_notes = sorted(set(notes))
    note_to_int = {note: number for number, note in enumerate(unique_notes)}
    int_to_note = {number: note for note, number in note_to_int.items()}

    network_input = []
    network_output = []

    if len(notes) <= seq_length:
        raise ValueError(f"Melodi çok kısa! Nota sayısı: {len(notes)}, gerekli minimum: {seq_length + 1}")

    for i in range(0, len(notes) - seq_length):
        seq_in = notes[i:i + seq_length]
        seq_out = notes[i + seq_length]
        network_input.append([note_to_int[n] for n in seq_in])
        network_output.append(note_to_int[seq_out])

    n_patterns = len(network_input)
    X = np.reshape(network_input, (n_patterns, seq_length, 1)) / float(len(unique_notes))
    y = tf.keras.utils.to_categorical(network_output, num_classes=len(unique_notes))


    return X, y, note_to_int, int_to_note

