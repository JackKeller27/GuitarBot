from UI.components.ChordSuggester import get_diatonic_chords

# take in a flat list of note names
NOTES = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']

# Gets corresponding index in ROOT_NOTES list ----- LARGELY COPIED FROM ChordSuggester.py
def get_note_idx(note):
    note_idx = -1
    for i in range(0, len(NOTES)):
        if NOTES[i] == note:
            note_idx = i
            break

    return note_idx


def note_as_root(key_chords, melody_note):
    return melody_note

def note_as_third(key_chords, melody_note):
    return NOTES[get_note_idx(melody_note) - ]

# def note_as_fifth(key_chords, melody_note):
#     return NOTES[]

def generate_harmony(key_chords, melody_notes):
    chord_progession = []

    for i in range(0, len(melody_notes), 4): # bar by bar
        chord_progession.append(note_as_third(key_chords, melody_notes[i]))

    return chord_progession

def demo():
    key = input('Pick a key: ')
    key = (key.split(' ')[0], key.split(' ')[1])

    key_chords = get_diatonic_chords(key)

    melody_notes = input("Insert space separated melody notes: ")
    melody_notes = melody_notes.upper()
    melody_notes = melody_notes.split(' ')

    print(generate_harmony(melody_notes))

demo()