import numpy as np
# Tuning of the robot
tuning = np.array([40, 45, 50, 55, 59, 64])
# minStrings = 6

note_midi_dict = {
        "E": [40, 52, 64],
        "F": [41, 53, 65],
        "F#": [42, 54, 66],
        "Gb": [42, 54, 66],
        "G": [43, 55, 67],
        "G#": [44, 56, 68],
        "Ab": [44, 56, 68],
        "A": [45, 57, 69],
        "A#": [46, 58, 70],
        "Bb": [46, 58, 70],
        "B": [47, 59, 71],
        "C": [48, 60, 72],
        "C#": [49, 61, 73],
        "Db": [49, 61, 73],
        "D": [50, 62],
        "D#": [51, 63],
        "Eb": [51, 63]
    }

root_midi_dict = {
        "E": note_midi_dict["E"][0],
        "F": note_midi_dict["F"][0],
        "F#": note_midi_dict["F#"][0],
        "Gb": note_midi_dict["Gb"][0],
        "G": note_midi_dict["G"][0],
        "G#": note_midi_dict["G#"][0],
        "Ab": note_midi_dict["Ab"][0],
        "A": note_midi_dict["A"][0],
        "A#": note_midi_dict["A#"][0],
        "Bb": note_midi_dict["Bb"][0],
        "B": note_midi_dict["B"][0],
        "C": note_midi_dict["C"][0],
        "C#": note_midi_dict["C#"][0],
        "Db": note_midi_dict["Db"][0],
        "D": note_midi_dict["D"][0],
        "D#": note_midi_dict["D#"][0],
        "Eb": note_midi_dict["Eb"][0]    
}

chord_interval_dict = {
        "M": [4, 7], # Major
        "m": [3, 7], # Minor
        "7": [4, 7, 10], # Dominant 7th
        "M7": [4, 7, 11], # Major 7th
        "m7": [3, 7, 10], # Minor 7th
        "add9": [4, 7, 14], # Add 9th
        "sus2": [2, 7], # Sus 2
        "sus4": [5, 7], # Sus 4
        "aug": [4, 8], # Augmented
        "dim": [3, 6], # Diminished
        "dim7": [3, 6, 9], # Diminished 7th
        "M6": [4, 7, 9], # Major 6th
        "m6": [3, 7, 9], # Minor 6th
        "M9": [4, 7, 11, 14], # Major 9th
        "m9": [3, 7, 10, 14], # Minor 9th
        "M11": [4, 7, 11, 14, 17], # Major 11th
        "m11": [3, 7, 10, 14, 17], # Minor 11th
        "M13": [4, 7, 11, 14, 17, 21], # Major 13th
        "m13": [3, 7, 10, 14, 17, 21], # Minor 13th
}

# fret_distances = {
#         "1": 30,
#         "2": 28,
#         "3": 28,
#         "4": 28,
#         "5": 27,
#         "6": 26,
#         "7": 25,
#         "8": 23.5,
#         "9": 22,
#         "10": 20
# }

fret_distances = {
        "0": 0,
        "1": 20,
        "2": 53,
        "3": 86,
        "4": 120,
        "5": 150,
        "6": 170,
        "7": 198,
        "8": 224,
        "9": 248,
        "10": 260,
        "0.0": 0,
        "1.0": 20,
        "2.0": 53,
        "3.0": 86,
        "4.0": 120,
        "5.0": 150,
        "6.0": 170,
        "7.0": 198,
        "8.0": 224,
        "9.0": 248,
        "10.0": 260
}