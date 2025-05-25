# 🎼 MelodAI

MelodAI is an intelligent melody generation system that learns your musical taste through feedback and creates original compositions. It combines LSTM-based neural networks with reinforcement learning (RL) and music theory to generate rhythmically and harmonically pleasing melodies.

## 🚀 Features

- 🎶 Melody generation using an LSTM model
- 🔁 Adaptive learning with user feedback (1–5 rating)
- 🎹 Smart chord and rhythm generation based on music theory
- 🧠 Lightweight Reinforcement Learning agent (Q-learning)
- 🖥️ Simple and intuitive GUI (built with Tkinter)
- 💾 MIDI export support for listening or further editing

## 📂 Folder Structure

```
MelodAI/
├── data/                # (Optional) User's own MIDI dataset (ignored by Git)
├── models/              # Trained models (saved weights)
├── src/                 # Source code
│   ├── main.py              # Melody generation and training loop
│   ├── gui.py               # Tkinter GUI app
│   ├── agent.py             # FeedbackAgent (Q-learning)
│   ├── model.py             # LSTMComposer (Keras-based)
│   ├── data_utils.py        # MIDI loading and preprocessing
│   ├── smart_chords.py      # Chord and rhythm generation
│   └── utils.py             # Miscellaneous helpers
├── requirements.txt     # Python dependencies
├── README.md            # This file
├── .gitignore           # Files to be ignored by Git
└── LICENSE              # Project license
```

## 🛠️ Installation

Make sure you have **Python 3.7+** installed. Then, install the dependencies:

```bash
pip install -r requirements.txt
```

## 🎛️ How to Use

1. Launch the GUI (under development):

```bash
python src/gui.py
```

2. Select a folder containing your own `.mid` (MIDI) files.
3. Click “Generate Melody” to let the AI compose a new melody.
4. Use “Play” to listen, and rate the melody from 1 to 5 using the GUI.
5. The agent learns your preference over time and updates its strategy.
6. Click “Save Best” to export the best composition as a `.mid` file.

We recommend you to run this AI model with Python files cause of not-complete GUI.

## 🧠 AI Architecture

- **LSTMComposer**: A deep learning model trained on sequences of notes to predict the next note in a melody.
- **FeedbackAgent**: A simple reinforcement learning agent that updates its Q-values based on your feedback scores.
- **Smart Chords**: Adds appropriate chords based on scale degrees and inferred harmony (basic C major is default).
- **Rhythmic Patterns**: Melodies are enhanced with predefined or randomized rhythms.

## ✅ Requirements

- `tensorflow`
- `numpy`
- `music21`
- `tk`

You can install them via:

```bash
pip install tensorflow numpy music21 tk
```

## 📈 Feedback-Driven Learning

Each time you rate a melody:
- The agent maps the melody to a simplified state.
- Rewards are stored in a Q-table.
- Over time, melodies that receive higher ratings are favored.

This process personalizes the generator to your preferences.

## 🎹 MIDI Files

You can use any folder of `.mid` files as training data. Ensure the files are monophonic or compatible with melody extraction.


## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please fork the repository and open a pull request with your improvements, whether it’s:
- Improved training routines
- Better harmony inference
- Advanced RL algorithms
- More UI features

---

Created by [Metehan Günen](https://github.com/Metrohan) & [Musa Emre Delen](https://github.com/Polsyia)