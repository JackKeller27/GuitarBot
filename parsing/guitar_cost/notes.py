def notePossibilities(desired_note):
    note_map = {
        "E": [0, -1, -1, -1, -1, -1], "F": [1, -1, -1, -1, -1, -1], "Gb": [2, -1, -1, -1, -1, -1],
        "G": [3, -1, -1, -1, -1, -1], "Ab": [4, -1, -1, -1, -1, -1], "A": [5, 0, -1, -1, -1, -1],
        "Bb": [6, 1, -1, -1, -1, -1], "B": [7, 2, -1, -1, -1, -1], "C": [8, 3, -1, -1, -1, -1],
        "Db": [9, 4, -1, -1, -1, -1], "D": [10, 5, 0, -1, -1, -1], "Eb": [-1, 6, 1, -1, -1, -1],
        "E2": [-1, 7, 2, -1, -1, -1], "F2": [-1, 8, 3, -1, -1, -1], "Gb2": [-1, 9, 4, -1, -1, -1],
        "G2": [-1, 10, 5, 0, -1, -1], "Ab2": [-1, -1, 6, 1, -1, -1], "A2": [-1, -1, 7, 2, -1, -1],
        "Bb2": [-1, -1, 8, 3, -1, -1], "B2": [-1, -1, 9, 4, 0, -1], "C2": [-1, -1, 10, 5, 1, -1],
        "Db2": [-1, -1, -1, 6, 2, -1], "D2": [-1, -1, -1, 7, 3, -1], "Eb2": [-1, -1, -1, 8, 4, -1],
        "E3": [-1, -1, -1, 9, 5, 0], "F3": [-1, -1, -1, 10, 6, 1], "Gb3": [-1, -1, -1, -1, 7, 2],
        "G3": [-1, -1, -1, -1, 8, 3], "Ab3": [-1, -1, -1, -1, 9, 4], "A3": [-1, -1, -1, -1, 10, 5],
        "Bb3": [-1, -1, -1, -1, -1, 6], "B3": [-1, -1, -1, -1, -1, 7], "C3": [-1, -1, -1, -1, -1, 8],
        "Db3": [-1, -1, -1, -1, -1, 9], "D3": [-1, -1, -1, -1, -1, 10]
    }

    return note_map.get(desired_note, [-1, -1, -1, -1, -1, -1])

