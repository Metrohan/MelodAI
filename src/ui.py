import os
import threading
import random
import subprocess
from tkinter import Tk, Button, Label, filedialog, IntVar, messagebox

from main import (
    load_melody_midi,
    prepare_sequences,
    LSTMComposer,
    FeedbackAgent,
    save_full_song,
    get_random_midi_path
)

class MelodAIGUI(Tk):
    def __init__(self):
        super().__init__()
        self.title("MelodAI")
        self.geometry("500x500")

        self.dataset_path = None
        self.composer = None
        self.agent = FeedbackAgent()
        self.seed = None
        self.final_melody = None
        self.best_reward = -float('inf')

        self.setup_widgets()

    def setup_widgets(self):
        Label(self, text="MelodAI", font=("Arial", 18)).pack(pady=10)

        Button(self, text="📁 Browse dataset folder", command=self.select_folder).pack(pady=5)
        Button(self, text="🎶 Compose", command=self.threaded_generate).pack(pady=5)
        Button(self, text="▶ Listen", command=self.play_midi).pack(pady=5)
        Button(self, text="⭐ Rate (1-5)", command=self.get_feedback).pack(pady=5)
        Button(self, text="💾 Save", command=self.save_final).pack(pady=5)

    def select_folder(self):
        self.dataset_path = filedialog.askdirectory()
        if self.dataset_path:
            messagebox.showinfo("Folder selected", f"Dataset path:\n{self.dataset_path}")

    def threaded_generate(self):
        threading.Thread(target=self.generate).start()

    def generate(self):
        if not self.dataset_path:
            messagebox.showwarning("Error", "Please select a dataset folder first.")
            return

        midi_path = get_random_midi_path(self.dataset_path)
        melody = load_melody_midi(midi_path)
        X, y, note_to_int, int_to_note = prepare_sequences(melody)

        self.composer = LSTMComposer(note_to_int, int_to_note)
        self.seed = list(X[0].flatten() * len(note_to_int))[:32]

        melody = self.composer.generate_melody(self.seed)
        save_full_song(melody, filename="gui_generated.mid")
        self.current_melody = melody
        messagebox.showinfo("Created a composition", "New melody created: gui_generated.mid")

    def play_midi(self):
        path = "gui_generated.mid"
        if not os.path.exists(path):
            messagebox.showwarning("Warning", "No melody generated yet.")
            return

        if os.name == 'nt':
            os.startfile(path)
        elif sys.platform == 'darwin':
            subprocess.call(['open', path])
        else:
            subprocess.call(['xdg-open', path])

    def get_feedback(self):
        if not hasattr(self, 'current_melody'):
            messagebox.showwarning("Warning", "No melody generated yet.")
            return

        feedback = IntVar()
        def submit():
            val = feedback.get()
            if 1 <= val <= 5:
                self.agent.update_q_table(
                    self.agent.get_state(self.current_melody), "same", val
                )
                if val > self.best_reward:
                    self.best_reward = val
                    self.final_melody = self.current_melody
                fb.destroy()
            else:
                messagebox.showerror("Warning", "Rating must be between 1 and 5.")

        fb = Tk()
        fb.title("Rate the Composition")
        Label(fb, text="Rate this composition between 1-5:").pack()
        for i in range(1, 6):
            Button(fb, text=str(i), command=lambda v=i: feedback.set(v)).pack(side="left", padx=5)
        Button(fb, text="Send", command=submit).pack(pady=10)
        fb.mainloop()

    def save_final(self):
        if self.final_melody:
            save_full_song(self.final_melody, filename="final_composition.mid")
            messagebox.showinfo("Saved", "Final composition saved: final_composition.mid")
        else:
            messagebox.showinfo("Info", "There is no saved composition before.")

if __name__ == "__main__":
    app = MelodAIGUI()
    app.mainloop()
