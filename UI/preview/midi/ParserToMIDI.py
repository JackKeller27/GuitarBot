from mido import Message
from UI.constants.ChordsDict import chords

MAJOR_THIRD, PERFECT_FOURTH = 4, 5
curr_chord_name = ""

# Given a position, seeks to the next strum
def get_next_chord_strum(left_arm, right_arm, tempo, measure_idx, subdiv_idx, curr_chord_name):
    next_chord_name = curr_chord_name # holds next chord if change made in meantime

    is_downstrum = right_arm[measure_idx][subdiv_idx].lower() == "d"
    subdiv_idx += 1
    curr_chord_subdiv_count = 1
    
    while measure_idx < len(right_arm):
        while subdiv_idx < len(right_arm[measure_idx]):
            if subdiv_idx < len(left_arm[measure_idx]) and left_arm[measure_idx][subdiv_idx] != "":
                next_chord_name = left_arm[measure_idx][subdiv_idx]
            if right_arm[measure_idx][subdiv_idx] != "":
                break # strum performed
            curr_chord_subdiv_count += 1
            subdiv_idx += 1
        subdiv_idx = 0
        measure_idx += 1

    MIDI_note_ons, MIDI_note_offs = chord_name_to_MIDI(curr_chord_name, curr_chord_subdiv_count, is_downstrum)
    MIDI_tuple = (MIDI_note_ons, MIDI_note_offs, tempo/120 * curr_chord_subdiv_count) # assumes eight notes the subdiv
    curr_chord_name = next_chord_name

    return measure_idx, subdiv_idx, MIDI_tuple

# Takes in arms and timing info information, uses them to create MIDI message for whole song
# left_arm: same ideas as one in UIGen.py
# right_arm: created in UIGen.py
def arms_to_MIDI(left_arm, right_arm, tempo):
    global curr_chord_name
    MIDI_song = [] # list of tuples of form (note_ons, note_offs, duration in seconds for chord)

    measure_idx, subdiv_idx = 0, 0

    # Assumes a chord will be specified in the first slot...
    curr_chord_name = left_arm[0][0]
    
    while measure_idx < len(left_arm):
        measure_idx, subdiv_idx, MIDI_tuple = get_next_chord_strum(left_arm, right_arm, tempo, measure_idx, subdiv_idx, curr_chord_name)
        MIDI_song.append(MIDI_tuple)

    return MIDI_song

# Takes in tab and timing information, mapping inputs to MIDI.
###        chord: name of chord
### subdivisions: number of eigth notes chord rings
### is_downstrum: true if downstrum, false if upstrum
# TODO: remove extraneous subdivisions param from calling code 
def chord_name_to_MIDI(chord_name, subdivisions, is_downstrum):
    MIDI_note_ons, MIDI_note_offs = [], []
    open_note = 40 # E2 in standard tuning
    chord_tab = chords[chord_name] # list of ints in tab notation where 6th string, low bass, comes first

    string_idx = 7
    # TODO: velocity, or loudness, should vary by note to correspond with upstrum/downstrum?
    # should emphasize 1 and 3 beats in 4/4?
    for fret_number_of_note in chord_tab:
        string_idx -= 1
        if fret_number_of_note == 'X':
            continue
        MIDI_note_ons.append(Message("note_on", note=open_note+fret_number_of_note, velocity=80, channel=0).bytes())
        MIDI_note_offs.append(Message("note_off", note=open_note+fret_number_of_note, channel=0).bytes()) # removed duration, doesn't work w/ VST?
        if string_idx != 3:
            open_note += PERFECT_FOURTH
        else:
            open_note += MAJOR_THIRD
        
    if not is_downstrum:
        for i in range(3, 6):
            MIDI_note_ons[i].velocity = 70 # decrease bass note volume
        
        MIDI_note_ons.reverse() # reverse order of notes to mimic upstrum (high e comes first)
        MIDI_note_offs.reverse()
    
    else:
        for i in range(0, 3):
            MIDI_note_ons[i].velocity = 90 # up bass note volume

    return MIDI_note_ons, MIDI_note_offs


# Each interval "constant" holds the appropriate offset
# MINOR_FIRST, FIRST, MINOR_SECOND, MINOR_THIRD, MAJOR_THIRD = 1, 2, 3, 4, 5
# PERFECT_FOURTH, PERFECT_FIFTH, MINOR_SIXTH, MAJOR_SIXTH = 6, 7, 8, 9
# MINOR_SEVENTH, MAJOR_SEVENTH, OCTAVE = 10, 11, 12
# Function that returns an E major shape MIDI voicing of the given chord formatted in a MIDO message.
### chord: chord name, 
### eightNotes: number of eigth notes chord rings
### tempo: BPM it is played in
### NOTE: Assumes chord is not an inversion, logic can be adjusted later to check for / char
# def barre_chord(chord, eightNotes, tempo):
#     rootNoteNum = ord(chord[0]) - 29 # uppercase ASCII -> MIDI bass note
#     offsetIfMinor = -1 if (len(chord) > 1 and chord[1] == 'm') else 0
#     duration = eightNotes * 30/tempo
#     if (rootNoteNum < 40): # ensures no dips below standard tuning E2 limit
#         rootNoteNum += OCTAVE
#     # TODO: adjust velocity to scale with duration?
#     return [Message("note_on", note=rootNoteNum, velocity=80, channel=0),
#             Message("note_on", note=rootNoteNum+PERFECT_FIFTH, velocity=80, channel=0),
#             Message("note_on", note=rootNoteNum+OCTAVE, velocity=80, channel=0),
#             Message("note_on", note=rootNoteNum+OCTAVE+MAJOR_THIRD+offsetIfMinor, velocity=80, channel=0),
#             Message("note_on", note=rootNoteNum+OCTAVE+PERFECT_FIFTH, velocity=80, channel=0),
#             Message("note_on", note=rootNoteNum+2*OCTAVE, velocity=80, channel=0),
#                 Message("note_off", note=rootNoteNum, time=duration, channel=0),
#                 Message("note_off", note=rootNoteNum+PERFECT_FIFTH, time=duration, channel=0),
#                 Message("note_off", note=rootNoteNum+OCTAVE, time=duration, channel=0),
#                 Message("note_off", note=rootNoteNum+OCTAVE+MAJOR_THIRD+offsetIfMinor, time=duration, channel=0),
#                 Message("note_off", note=rootNoteNum+OCTAVE+PERFECT_FIFTH, time=duration, channel=0),
#                 Message("note_off", note=rootNoteNum+2*OCTAVE, time=duration, channel=0)]
