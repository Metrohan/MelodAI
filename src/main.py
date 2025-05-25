import os
import random
import sys
import subprocess
from music21 import stream, instrument, note
from data_utils import load_melody_midi, prepare_sequences
from model import LSTMComposer
from agent import FeedbackAgent
from smart_chords import add_smart_chords, generate_rhythm, apply_rhythm_to_notes

def generate_percussion_track(length=64):
    percussion = stream.Part()
    percussion.insert(0, instrument.Woodblock())
    for i in range(length):
        offset = i * 0.5
        if i % 4 == 0:
            kick = note.Note(35); kick.quarterLength = 0.5
            percussion.insert(offset, kick)
        if i % 4 == 2:
            snare = note.Note(38); snare.quarterLength = 0.5
            percussion.insert(offset, snare)
        hihat = note.Note(42); hihat.quarterLength = 0.25
        percussion.insert(offset, hihat)
    return percussion

def save_full_song(melody_notes, filename="melody_full.mid"):
    rhythm = generate_rhythm(len(melody_notes))
    melody_with_rhythm = apply_rhythm_to_notes(melody_notes, rhythm)
    melody_stream = stream.Part()
    melody_stream.insert(0, instrument.Piano())
    for n in melody_with_rhythm:
        melody_stream.append(n)

    chords_stream = add_smart_chords(melody_with_rhythm)
    percussion_stream = generate_percussion_track(len(melody_with_rhythm))

    score = stream.Score()
    score.insert(0, melody_stream)
    score.insert(0, chords_stream)
    score.insert(0, percussion_stream)

    score.write('midi', fp=filename)
    print(f"Beste kaydedildi: {filename}")
    open_midi_file(filename)

def open_midi_file(path):
    if sys.platform.startswith('win'):
        os.startfile(path)
    elif sys.platform.startswith('darwin'):
        subprocess.call(['open', path])
    else:
        subprocess.call(['xdg-open', path])

def get_random_midi_path(dataset_folder):
    files = [f for f in os.listdir(dataset_folder) if f.endswith(".mid")]
    return os.path.join(dataset_folder, random.choice(files))

def get_user_feedback():
    while True:
        try:
            feedback = int(input("Bu besteyi 1 (kötü) ile 5 (çok iyi) arasında puanla: "))
            if 1 <= feedback <= 5:
                return feedback
        except ValueError:
            continue

if __name__ == "__main__":
    dataset_path = "path/to/your/midi/dataset"  # Change this to your dataset path
    midi_path = get_random_midi_path(dataset_path)
    print(f"Kullanılan örnek: {midi_path}")

    melody = load_melody_midi(midi_path)
    print(f"Melody uzunluğu: {len(melody)}")
    print(f"Melody örnek: {melody[:10]}")

    X, y, note_to_int, int_to_note = prepare_sequences(melody)
    print("note_to_int uzunluğu:", len(note_to_int))

    composer = LSTMComposer(note_to_int, int_to_note)

    composer.model.fit(X, y, epochs=150, batch_size=128)

    agent = FeedbackAgent()
    seed = list(X[0].flatten())

    best_reward = -float('inf')
    final_melody = None

    for episode in range(5):
        melody = composer.generate_melody(seed)
        save_full_song(melody, filename=f"rl_generated_{episode}.mid")
        reward = get_user_feedback()
        state = agent.get_state(melody)
        agent.update_q_table(state, "same", reward)
        print(f"Episode {episode}: Feedback = {reward}")

        if reward > best_reward:
            best_reward = reward
            final_melody = melody

    if final_melody:
        save_full_song(final_melody, filename="final_composition.mid")
        print("Final beste oluşturuldu: final_composition.mid")
