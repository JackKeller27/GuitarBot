import numpy as np
import parsing.guitar_cost.traj as traj
import pandas as pd

def find_lowest_cost_chord(current_fret_positions, filepath, chord_letter, chord_type):
    min_cost = float('inf')
    easiest_frets = None

    for chord_voicing in _get_chord_voicings_list(filepath, chord_letter, chord_type):
        cost = _calculate_cost(current_fret_positions, chord_voicing)
        if cost < min_cost:
            min_cost = cost
            easiest_frets = chord_voicing

    return easiest_frets

def _get_chord_voicings_list(filepath, chord_letter, chord_type):
    df_chords = pd.read_csv(filepath)
    chord_possibilities = []
    row = 0

    # Finds row where first voicing occurs
    while row < 334 and not (df_chords.iloc[row].iloc[0] == chord_letter and df_chords.iloc[row].iloc[1] == chord_type):
        row += 1

    # Add all voicings (assumes they're contiguous, allows for stopping early)
    while row < 334 and df_chords.iloc[row].iloc[0] == chord_letter and df_chords.iloc[row].iloc[1] == chord_type:
        chord_possibilities.append(_chord_from_row(df_chords, row))
        row += 1

    return chord_possibilities

def _chord_from_row(df_chords, row):
    chord = []
    for j in range(3, 9):
        try:
            chord.append(int(df_chords.iloc[row].iloc[j]))
        except:
            chord.append(-1)
    return chord

def _calculate_cost(arr1, arr2, N = 25):
    cost = 0
    fret_lengths = [37.85201719088437, 35.63981144712466, 33.639502533759924,
                        31.751462333006657, 29.96938968620543, 28.287337091556935,
                        26.69969085488873, 25.201152354471787, 23.786720357363606,
                        22.45167432825832, 21.191558675138026]
    for a, b in zip(arr1, arr2):
        if b == -1:
            y1 = fret_lengths[0]
            y2 = fret_lengths[0]
        else:
            y1 = fret_lengths[a]
            y2 = fret_lengths[b]

        x_values = np.linspace(0, 1, N)
        avg = (0 + N) / 2

        out = traj.interpWithBend(y1, y2, 25, 0.2)
        costs = abs(np.gradient(out))
        y_value = np.interp(avg, x_values, costs)

        cost += y_value * 59.9406059

    cost = cost/6
    return cost
