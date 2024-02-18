import pandas as pd

from mido import Message
from UI.constants.ChordsDict import chords, sharp_to_flat
from UI.preview.midi.chord_fingerings.viterbi import flatten, get_fingerings, initialize_viterbi, terminate_viterbi

MAJOR_THIRD, PERFECT_FOURTH = 4, 5

all_chords = pd.read_csv('all_chords_9frets.csv')
human_chords = pd.read_csv('humanPlayable_9frets.csv')

# Given a position, seeks to the next strum
def get_next_chord_strum(left_arm, right_arm, bpm, subdiv_per_beat, measure_idx, subdiv_idx, curr_chord_name):
    next_chord_name = curr_chord_name # holds next chord if change made in meantime

    is_downstrum = right_arm[measure_idx][subdiv_idx].lower() == "d"
    subdiv_idx += 1 # points to next strum input
    curr_chord_subdiv_count = 1
    break_outer = False
    
    while measure_idx < len(right_arm):
        while subdiv_idx < len(right_arm[measure_idx]):
            chord_idx = int(subdiv_idx / subdiv_per_beat) # account for the fact that there's only 1 chord input per beat

            # update the next chord if it's a new chord
            if chord_idx < len(left_arm[measure_idx]) and left_arm[measure_idx][chord_idx] != "":
                next_chord_name = left_arm[measure_idx][chord_idx]

            # break if the next strum input is a new strum
            if right_arm[measure_idx][subdiv_idx] != "":
                break_outer = True # set flag to break out of outer loop
                break # next strum/chord will be converted to midi in the next iteration

            curr_chord_subdiv_count += 1
            subdiv_idx += 1

        if (break_outer):
            break
        subdiv_idx = 0
        measure_idx += 1

    MIDI_note_ons, MIDI_note_offs = chord_name_to_MIDI(curr_chord_name, is_downstrum)

    note_duration = (60 / (bpm * subdiv_per_beat)) * curr_chord_subdiv_count # subdiv_duration * subdiv_count
    MIDI_tuple = (MIDI_note_ons, MIDI_note_offs, note_duration)
    curr_chord_name = next_chord_name

    return measure_idx, subdiv_idx, MIDI_tuple, curr_chord_name

# Takes in arms and timing info information, uses them to create MIDI message for whole song
# left_arm: same ideas as one in UIGen.py
# right_arm: created in UIGen.py
def arms_to_MIDI(left_arm, right_arm, bpm, subdiv_per_beat):
    MIDI_song = [] # list of tuples of form (note_ons, note_offs, duration in seconds for chord)

    measure_idx, subdiv_idx = 0, 0
    curr_chord_name = ''

    # If the first beat contains a chord, begin from there
    if (left_arm[0][0] != ''):
        curr_chord_name = left_arm[0][0]
    else:
        # find first chord and set measure_idx, subdiv_idx accordingly
        break_outer = False

        while measure_idx < len(right_arm):
            while subdiv_idx < len(right_arm[measure_idx]):
                chord_idx = int(subdiv_idx / subdiv_per_beat) # account for the fact that there's only 1 chord input per beat
            
                # find first chord/strum input
                if left_arm[measure_idx][chord_idx] != '' and right_arm[measure_idx][subdiv_idx] != '':
                    curr_chord_name = left_arm[measure_idx][chord_idx]
                    break_outer = True
                    break
                else:
                    subdiv_idx += 1

            if break_outer:
                break
            subdiv_idx = 0
            measure_idx += 1
    
    while measure_idx < len(left_arm):
        measure_idx, subdiv_idx, MIDI_tuple, curr_chord_name = get_next_chord_strum(left_arm, right_arm, bpm, subdiv_per_beat, measure_idx, subdiv_idx, curr_chord_name)
        MIDI_song.append(MIDI_tuple)

    return MIDI_song

# Resolves a chord name to a chord voicing (in tab), and maps it to MIDI.
###   chord_name: name of chord, i.e., A (for A major)
### is_downstrum: true if downstrum, false if upstrum
def chord_name_to_MIDI(chord_name, is_downstrum):
    MIDI_note_ons, MIDI_note_offs = [], []
    open_note = 40 # E2 in standard tuning

    # map sharps to flats
    if len(chord_name) >= 2 and chord_name[1] == '#':
        chord_name = sharp_to_flat[chord_name[:2]] + ('' if len(chord_name) < 3 else chord_name[2:])

    chord_tab = chords[chord_name] # list of ints in tab notation where 6th string, low bass, comes first
    # chord_tab = chord_name_to_tab(chord_name) # naive integration, runtime optimization possible

    string_idx = 6
    # TODO: velocity, or loudness, should vary by note to correspond with upstrum/downstrum?
    # should emphasize 1 and 3 beats in 4/4?
    for fret_number_of_note in chord_tab:
        if fret_number_of_note == 'X' or fret_number_of_note == 'x': 
            continue

        note_volume = 80
        if string_idx >= 4:
            if is_downstrum:
                note_volume += 10
            else:
                note_volume -= 10

        MIDI_note_ons.append(Message("note_on", note=open_note+fret_number_of_note, velocity=note_volume, channel=0).bytes()) # default velocity is 64
        MIDI_note_offs.append(Message("note_off", note=open_note+fret_number_of_note, channel=0).bytes()) # removed duration, doesn't work w/ VST?
        if string_idx != 3: # tempered for standard tuning
            open_note += PERFECT_FOURTH
        else:
            open_note += MAJOR_THIRD
        string_idx -= 1

    if not is_downstrum: # upstrum
        MIDI_note_ons.reverse() # reverse order of notes to mimic upstrum (high e comes first)
        MIDI_note_offs.reverse()

    return MIDI_note_ons, MIDI_note_offs

# Unit that maps a chord name to tab using Saksham's viterbi
def chord_name_to_tab(chord_name):
    num_fingerings = -1
    num_chords = -1

    viterbi, back_pointer = initialize_viterbi(num_fingerings, num_chords)

    # chord_progression = flatten(left_arm)
    terminate_viterbi(viterbi)