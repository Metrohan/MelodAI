import random
import subprocess
import time
import numpy as np
from music21 import note, stream, scale

class MusicAgent:
    def __init__(self):
        self.c_major_scale = scale.MajorScale("C4")
        self.q_table = {}
        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = 0.1

    def generate_melody(self, length=16):
        melody = stream.Stream()
        for _ in range(length):
            n = note.Note(random.choice(self.c_major_scale.getPitches()))
            melody.append(n)
        return melody

    def add_note(self, melody):
        n = note.Note(random.choice(self.c_major_scale.getPitches()))
        melody.append(n)
    
    def change_pitch(self, melody):
        if melody.notes:
            n = random.choice(melody.notes)
            n.pitch = random.choice(self.c_major_scale.getPitches())
    
    def change_duration(self, melody):
        if melody.notes:
            n = random.choice(melody.notes)
            n.quarterLength = random.choice([0.25, 0.5, 1.0, 2.0])
    
    def remove_note(self, melody):
        if melody.notes:
            n = random.choice(melody.notes)
            melody.remove(n)
    
    def take_action(self, melody, action):
        actions = {
            0: self.add_note,
            1: self.change_pitch,
            2: self.change_duration,
            3: self.remove_note,
            4: lambda x: x
        }
        if action in actions:
            actions[action](melody)
        return melody
    
    def get_reward(self, melody):
        from music21 import interval  # Eksik import düzeltildi
        reward = 0

        prev_note=None
        for n in melody.notes:
            if prev_note:
                interval_size = abs(interval.Interval(prev_note, n).semitones)
                if interval_size > 7:
                    reward -= 1
                else:
                    reward += 1
            prev_note = n
        
        note_frequencies = {}
        for n in melody.notes:
            pitch_name = n.pitch.name
            if pitch_name in note_frequencies:
                note_frequencies[pitch_name] += 1
            else:
                note_frequencies[pitch_name] = 1
        
        for count in note_frequencies.values():
            if count > 1:
                reward += 0.5
        
        return reward
    
    def get_state(self, melody):
        return tuple(n.pitch.midi for n in melody.notes)

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(range(5))
        return np.argmax(self.q_table.get(state, np.zeros(5)))

    def update_q_table(self, state, action, reward, next_state):
        if state not in self.q_table:
            self.q_table[state] = np.zeros(5)
        if next_state not in self.q_table:
            self.q_table[next_state] = np.zeros(5)

        best_next_action = np.argmax(self.q_table[next_state])
        self.q_table[state][action] = (1 - self.alpha) * self.q_table[state][action] + \
                                      self.alpha * (reward + self.gamma * self.q_table[next_state][best_next_action])
    def train(self, episodes=100):
        """Ajanın Q-learning ile eğitilmesi."""
        for episode in range(episodes):
            melody = self.generate_melody()
            state = self.get_state(melody)
            
            for _ in range(10):  # 10 adım boyunca aksiyon al
                action = self.choose_action(state)
                self.take_action(melody, action)
                next_state = self.get_state(melody)
                reward = self.get_reward(melody)
                
                self.update_q_table(state, action, reward, next_state)
                state = next_state
            
            if episode % 10 == 0:
                print(f"Episode {episode}: Reward {reward}")         

agent = MusicAgent()
agent.train()

class MusicEnv:
    def __init__(self):
        self.melody = stream.Stream()
        self.c_major_scale = scale.MajorScale("C4")
        self.state = []
    
    def generate_melody(self, length=16):

        self.state = []
        self.melody = stream.Stream()

        for _ in range(length):
            pitch = self.c_major_scale.getPitches()[random.randint(0, 6)].name
            n = note.Note(pitch)
            self.melody.append(n)
            self.state.append(n)

    def show_melody(self):
        file_path = "temp_music.xml"
        self.melody.write('musicxml', fp=file_path)  # XML dosyası olarak kaydet
        process = subprocess.Popen(["C:/Program Files/MuseScore 4/bin/MuseScore4.exe", file_path])
        return process

    def get_reward(self):
        while True:
            feedback = input("Bu melodi hoşuna gitti mi? (y/n): ").strip().lower()
            if feedback in ['y', 'n']:
                return 1 if feedback == 'y' else -1
            print("Lütfen sadece 'y' veya 'n' girin.")

def is_valid_melody(melody):
    prev_note = None
    for n in melody:
        if prev_note:
            interval = abs(prev_note.pitch.midi - n.pitch.midi)
            if interval > 7:
                return False
        prev_note = n
    return True

env = MusicEnv()

for _ in range(5):
    env.generate_melody()
    
    musescore_process = env.show_melody()  # **Musescore'u aç, terminali kilitlemeden devam et**
    
    print("Melodi açıldı, Musescore'u kapatınca devam edecek...")
    
    musescore_process.wait()  # **Burada program, Musescore kapanana kadar bekler**
    
    # Kullanıcı geri bildirimi al
    reward = env.get_reward()
    
    print(f"Kullanıcıdan gelen ödül: {reward}")
    print("Melodi geçerli mi?", is_valid_melody(env.state))


