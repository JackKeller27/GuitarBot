# Chords library and sharp-to-flat conversions

sharp_to_flat = {
    'G#': 'Ab',
    'A#': 'Bb',
    'C#': 'Db',
    'D#': 'Eb',
    'F#': 'Gb'
}

# TODO: fill in missing chords
chord_dict = {
    # A
    'A': ['X', 0, 2, 2, 2, 0],
    'Am': ['X', 0, 2, 2, 1, 0],
    'AM6': [5, 4, 4, 'X', 5, 5],
    'AM7': None,
    'AM9': None,
    'Am6': [5, 3, 2, 2, 0, 0],
    'Am7': ['X', 3, 1, 3, 1, 3],
    'Am9': ['X', 3, 0, 3, 4, 3],
    'Am11': [8, 6, 5, 5, 6, 6],
    'Asus': ['X', 0, 2, 2, 3, 3],
    'Asus2': ['X', 0, 'X', 'X', 0, 0],
    'Asus4': ['X', 0, 2, 2, 3, 3],
    'A7': ['X', 0, 2, 0, 2, 0],
    'A9': None,
    'A13': None,
    'Adim7': None,
    'Adim': ['X', 3, 1, 'X', 1, 2],
    'Ao': ['X', 3, 1, 3, 1, 2],
    'A+': None,
    'A5': ['X', 0, 'X', 'X', 'X', 0],

    # B
    'B': ['X', 2, 4, 4, 4, 2],
    'Bm': [7, 9, 9, 7, 7, 7],
    'BM6': ['X', 2, 1, 1, 0, 2],
    'BM7': [7, 9, 8, 8, 7, 7],
    'BM9': None,
    'Bm6': None,
    'Bm7': ['X', 2, 0, 2, 0, 2],
    'Bm9': None,
    'Bm11': None,
    'Bsus': [7, 7, 9, 9, 7, 7],
    'Bsus2': ['X', 2, 'X', 'X', 2, 2],
    'Bsus4': [7, 7, 9, 9, 7, 7],
    'B7': ['X', 2, 1, 2, 0, 2],
    'B9': None,
    'B13': None,
    'Bdim7': None,
    'Bdim': None,
    'Bo': ['X', 2, 0, 2, 0, 1],
    'B+': None,
    'B5': ['X', 2, 'X', 'X', 0, 2],

    # C
    'C': ['X', 3, 2, 0, 1, 0],
    'Cm': [8, 6, 5, 0, 8, 8],
    'CM6': ['X', 3, 2, 2, 1, 3],
    'CM7': ['X', 3, 2, 4, 0, 3],
    'CM9': ['X', 3, 0, 3, 5, 3],
    'Cm6': ['X', 3, 1, 2, 3, 3],
    'Cm7': ['X', 3, 1, 3, 1, 3],
    'Cm9': ['X', 3, 0, 3, 4, 3],
    "Cm11": [8, 5, 5, 8, 6, 6],
    'Csus': [8, 8, 5, 5, 6, 8],
    'Csus2': [8, 5, 5, 0, 8, 8],
    'Csus4': [8, 8, 5, 5, 6, 8],
    'C7': [3, 2, 0, 0, 0, 0],
    'C9': None,
    'C13': None,
    'Cdim7': None,
    'Cdim': ['X', 3, 1, 'X', 1, 2],
    'Co': ['X', 3, 1, 3, 1, 2],
    'C+': None,
    'C5': ['X', 3, 'X', 0, 1, 3],

    # D
    'D': ['X', 5, 7, 7, 7, 5],
    'Dm': ['X', 'X', 0, 2, 3, 1],
    'DM6': ['X', 5, 4, 4, 3, 5],
    'DM7': ['X', 'X', 0, 2, 2, 2],
    'DM9': ['X', 2, 1, 'X', 2, 2],
    'Dm6': ['X', 5, 3, 4, 5, 5],
    'Dm7': ['X', 'X', 0, 2, 1, 1],
    'Dm9': ['X', 5, 7, 5, 6, 0],
    "Dm11": [10, 0, 10, 10, 8, 0],
    'Dsus': ['X', 5, 5, 0, 3, 5],
    'Dsus2': ['X', 'X', 0, 2, 'X', 0],
    'Dsus4': ['X', 5, 5, 0, 3, 5],
    'D7': ['X', 'X', 0, 2, 1, 2],
    'D9': None,
    'D13': None,
    'Ddim7': None,
    'Ddim': ['X', 'X', 0, 1, 3, 1],
    'Do': ['X', 'X', 0, 1, 1, 1],
    'D+': None,
    'D5': ['X', 'X', 0, 2, 'X', 'X'],

    # E
    'E': [0, 2, 2, 1, 0, 0],
    'Em': [0, 2, 2, 0, 0, 0],
    'EM6': [0, 2, 2, 4, 2, 4],
    'EM7': None,
    'EM9': None,
    'Em6': [0, 2, 4, 0, 2, 2],
    'Em7': [0, 2, 0, 0, 3, 0],
    'Em9': [0, 2, 0, 0, 0, 2],
    "Em11": [10, 0, 10, 10, 8, 10],
    'Esus': [0, 2, 2, 2, 0, 0],
    'Esus2': ['X', 'X', 0, 2, 'X', 0],
    'Esus4': [0, 2, 2, 2, 0, 0],
    'E7': [0, 'X', 0, 1, 0, 0],
    'E9': None,
    'E13': None,
    'Edim7': None,
    'Edim': [0, 7, 8, 0, 8, 0],
    'Eo': [0, 1, 0, 0, 3, 3],
    'E+': None,
    'E5': [0, 'X', 'X', 'X', 0, 0],

    # F
    'F': [1, 3, 3, 2, 1, 1],
    'Fm': ['X', 'X', 3, 1, 1, 4],
    'FM6': [1, 0, 0, 2, 1, 1],
    'FM7': [1, 0, 3, 2, 1, 0],
    'FM9': [1, 0, 1, 0, 1, 3],
    'Fm6': [1, 3, 0, 1, 1, 3],
    'Fm7': [1, 3, 1, 1, 4, 1],
    'Fm9': [1, 3, 1, 1, 1, 3],
    'Fm11': None,
    'Fsus': [1, 1, 3, 3, 1, 1],
    'Fsus2': [1, 'X', 'X', 0, 1, 1],
    'Fsus4': [1, 1, 3, 3, 1, 1],
    'F7': [1, 3, 1, 2, 1, 1],
    'F9': None,
    'F13': None,
    'Fdim7': None,
    'Fdim': ['X', 'X', 3, 4, 6, 4],
    'Fo': [1, 2, 3, 1, 4, 1],
    'F+': None,
    'F5': [1, 'X', 'X', 'X', 1, 1],

    # G
    'G': [3, 2, 0, 0, 0, 3],
    'Gm': [3, 1, 0, 0, 3, 3],
    'GM6': [3, 2, 0, 0, 3, 0],
    'GM7': [3, 1, 0, 0, 0, 2],
    'GM9': [3, 0, 0, 2, 0, 1],
    'Gm6': [3, 1, 0, 2, 3, 0],
    'Gm7': [3, 1, 0, 0, 3, 1],
    'Gm9': [3, 0, 0, 3, 3, 1],
    'Gm11': None,
    'Gsus': [3, 5, 3, 0, 0, 3],
    'Gsus2': [1, 'X', 'X', 0, 1, 1],
    'Gsus4': [3, 5, 3, 0, 0, 3],
    'G7': [3, 2, 0, 0, 0, 1],
    'G9': None,
    'G13': None,
    'Gdim7': None,
    'Gdim': [3, 1, 'X', 0, 2, 3],
    'Go': [3, 1, 3, 3, 2, 1],
    'G+': None,
    'G5': None,

    # Ab
    'Ab': [4, 6, 6, 5, 4, 4],
    'Abm': [4, 6, 6, 4, 4, 4],
    'AbM6': [4, 6, 6, 5, 6, 4],
    'AbM7': None,
    'AbM9': None,
    'Abm6': None,
    'Abm7': ['X', 'X', 6, 8, 7, 7],
    'Abm9': [4, 6, 4, 4, 0, 6],
    'Abm11': None,
    'Absus': [4, 4, 6, 6, 4, 4],
    'Absus2': [4, 1, 1, 3, 4, 4],
    'Absus4': [4, 4, 6, 6, 4, 4],
    'Ab7': [4, 6, 5, 5, 4, 4],
    'Ab9': None,
    'Ab13': None,
    'Abdim7': None,
    'Abdim': [4, 2, 0, 4, 0, 4],
    'Abo': [4, 2, 0, 4, 0, 2],
    'Ab+': None,
    'Ab5': [4, 6, 6, 'X', 4, 4],

    # Bb
    'Bb': ['X', 1, 0, 3, 3, 1],
    'Bbm': ['X', 1, 3, 3, 2, 1],
    'BbM6': ['X', 1, 0, 0, 'X', 1],
    'BbM7': [6, 0, 3, 3, 3, 5],
    'BbM9': None,
    'Bbm6': None,
    'Bbm7': [6, 8, 8, 6, 9, 9],
    'Bbm9': None,
    'Bbm11': None,
    'Bbsus': [6, 6, 3, 3, 4, 6],
    'Bbsus2': [6, 3, 3, 3, 6, 6],
    'Bbsus4': [6, 6, 3, 3, 4, 6],
    'Bb7': [6, 8, 6, 7, 6, 6],
    'Bb9': None,
    'Bb13': None,
    'Bbdim7': None,
    'Bbdim': [6, 4, 'X', 6, 5, 0],
    'Bbo': ['X', 1, 2, 1, 2, 0],
    'Bb+': None,
    'Bb5': ['X', 1, 3, 3, 'X', 1],

    #Db
    'Db': ['X', 4, 6, 6, 6, 4],
    'Dbm': [9, 7, 'X', 9, 9, 0],
    'DbM6': ['X', 4, 3, 3, 2, 4],
    'DbM7': ['X', 4, 6, 5, 6, 4],
    'DbM9': [9, 6, 6, 8, 6, 7],
    'Dbm6': ['X', 4, 2, 3, 4, 4],
    'Dbm7': ['X', 4, 2, 4, 0, 4],
    'Dbm9': ['X', 4, 6, 4, 4, 0],
    "Dbm11": [9, 9, 6, 8, 0, 0],
    'Dbsus': ['X', 4, 4, 1, 2, 2],
    'Dbsus2': [9, 6, 6, 8, 9, 9],
    'Dbsus4': ['X', 4, 4, 1, 2, 2],
    'Db7': ['X', 4, 3, 1, 0, 1],
    'Db9': None,
    'Db13': None,
    'Dbdim7': None,
    'Dbdim': ['X', 4, 2, 0, 2, 0],
    'Dbo': ['X', 4, 2, 0, 0, 3],
    'Db+': None,
    'Db5': ['X', 4, 6, 6, 'X', 4],

    #Eb
    'Eb': ['X', 6, 5, 0, 4, 6],
    'Ebm': ['X', 6, 8, 8, 7, 6],
    'EbM6': ['X', 6, 5, 5, 4, 6],
    'EbM7': ['X', 6, 0, 0, 4, 6],
    'EbM9': ['X', 6, 5, 0, 6, 6],
    'Ebm6': ['X', 6, 4, 5, 6, 6],
    'Ebm7': ['X', 6, 8, 6, 7, 6],
    'Ebm9': None,
    'Ebm11': None,
    'Ebsus': ['X', 6, 6, 'X', 4, 6],
    'Ebsus2': ['X', 6, 8, 8, 6, 6],
    'Ebsus4': ['X', 6, 6, 'X', 4, 6],
    'Eb7': ['X', 6, 8, 6, 8, 6],
    'Eb9': None,
    'Eb13': None,
    'Ebdim7': None,
    'Ebdim': ['X', 'X', 1, 2, 4, 2],
    'Ebo': ['X', 6, 4, 6, 4, 5],
    'Eb+': None,
    'Eb5': ['X', 6, 8, 8, 'X', 6],

    #Gb
    'Gb': [2, 4, 4, 3, 2, 2],
    'Gbm': ['X', 'X', 4, 2, 2, 2],
    'GbM6': ['X', 'X', 4, 6, 4, 6],
    'GbM7': [2, 4, 3, 3, 2, 2],
    'GbM9': [2, 1, 2, 1, 2, 0],
    'Gbm6': [2, 0, 1, 1, 2, 2],
    'Gbm7': [2, 0, 4, 2, 2, 0],
    'Gbm9': [2, 0, 2, 1, 2, 0],
    'Gbm11': None,
    'Gbsus': [2, 4, 4, 4, 2, 2],
    'Gbsus2': [2, 'X', 'X', 1, 2, 2],
    'Gbsus4': [2, 4, 4, 4, 2, 2],
    'Gb7': ['X', 'X', 4, 3, 2, 1],
    'Gb9': None,
    'Gb13': None,
    'Gbdim7': None,
    'Gbdim': [2, 0, 'X', 2, 1, 2],
    'Gbo': [2, 0, 2, 2, 1, 0],
    'Gb+': None,
    'Gb5': [2, 4, 4, 'X', 2, 2]
}