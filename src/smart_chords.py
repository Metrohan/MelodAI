from music21 import chord, stream, note, key, meter, duration
import random
import copy

def get_key_signature(notes):
    s = stream.Stream()
    for n in notes:
        if isinstance(n, note.Note):
            s.append(n)
    return s.analyze('key')

def get_diatonic_chords(key_signature, complexity='rich'):
    scale_degrees = [
        ('I', key_signature.tonic),
        ('ii', key_signature.getScale().pitchFromDegree(2)),
        ('iii', key_signature.getScale().pitchFromDegree(3)),
        ('IV', key_signature.getScale().pitchFromDegree(4)),
        ('V', key_signature.getScale().pitchFromDegree(5)),
        ('vi', key_signature.getScale().pitchFromDegree(6)),
        ('vii°', key_signature.getScale().pitchFromDegree(7)),
    ]

    diatonic_chords = []
    for degree_name, root in scale_degrees:
        if degree_name in ['ii', 'iii', 'vi']:
            base_chord = chord.Chord([root.transpose('m3'), root.transpose('P5')])
        elif degree_name == 'vii°':
            base_chord = chord.Chord([root.transpose('m3'), root.transpose('d5')])
        else:
            base_chord = chord.Chord([root.transpose('M3'), root.transpose('P5')])

        base_chord.root = root

        if complexity == 'rich':
            try:
                seventh = root.transpose('m7') if degree_name in ['ii', 'iii', 'vi'] else root.transpose('M7')
                base_chord.add(seventh)
            except:
                pass

        diatonic_chords.append((degree_name, base_chord))
    return diatonic_chords

def choose_functional_progression():
    return random.choice([
        ['I', 'IV', 'V', 'I'],
        ['I', 'vi', 'IV', 'V'],
        ['ii', 'V', 'I'],
        ['I', 'iii', 'vi', 'ii', 'V', 'I']
    ])

def add_smart_chords(melody_notes, complexity='rich'):
    key_sig = get_key_signature(melody_notes)
    chords = get_diatonic_chords(key_sig, complexity)
    progression = choose_functional_progression()
    chord_map = {name: ch for name, ch in chords}

    harmony = stream.Part()
    harmony.insert(0, key_sig)
    harmony.insert(0, meter.TimeSignature('4/4'))

    measure_length = 4
    total_beats = len(melody_notes) * 0.5
    num_measures = int(total_beats // measure_length) + 1

    for i in range(num_measures):
        degree = progression[i % len(progression)]
        c = copy.deepcopy(chord_map.get(degree, chord_map['I']))
        c.duration = duration.Duration(4.0)
        harmony.append(c)

    return harmony

def generate_rhythm(length):
    values = [0.25, 0.5, 1.0]
    rhythm = [random.choice(values) for _ in range(length)]
    return rhythm

def apply_rhythm_to_notes(melody_notes, rhythm):
    for i in range(min(len(melody_notes), len(rhythm))):
        melody_notes[i].quarterLength = rhythm[i]
    return melody_notes
