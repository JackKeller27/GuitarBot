import numpy as np
import itertools
from pluck_mapgen import get_string_state
from dict_maps import tuning

def genNotemap(note, tuning):
    """
    - Define ranges for each string.
    - Loop through the strings where the note can be played
    - Returns fret numbers in an array of length 6. Each item corresponding to each string. first item is string 1 (low E)

    """
    # For each string
    highest_pitch = tuning + 9

    frets = np.zeros(6)
    strings = np.zeros(6)

    for i in np.arange(6):
        low = tuning[i]
        high = highest_pitch[i]
        if note >= low and note <= high:
            pos = note-low
            frets[i] = pos
            strings[i] = i+1
        else:
            continue
    return frets, strings

def fretToNote(f, s, tuning):
    """
    Convert a fret position and a string position to midi note
    inputs 
    f: type (float). Fret number of the note
    s: type (float). String number of the note
    return: midi note value corresponding to given fret position and sttring position
    """
    note = tuning[int(s-1)] + f
    return note

def mapgen():
    fretmap = []
    stringmap = []

    for i, note in enumerate(np.arange(40, 74)):
        frets, strings = genNotemap(note, tuning)
        fretmap.append(frets)
        stringmap.append(strings)

    return fretmap, stringmap

def indexPositions(note, fretmap, stringmap):
    """
    Function to index positions from the existing fretboard map
    """
    # print (f'note: {note}, type: {type(note)}')
    index = int(note-40) # 40 = the lowest note possible on the guitarbot according to standard tuning
    # print (f'index: {index}')
    note_fretmap = fretmap[index]
    note_stringmap = stringmap[index]
    return note_fretmap, note_stringmap

def genStringPossibilities(notes, fretmap, stringmap):
    """
    Function to generate all possible locations where the given set of notes can be played.
    Returns: All possible combinations
    """
    strings_possibilities = []
    frets_possibilities = []
    for note in notes:
        fretmap_note, stringmap_note = indexPositions(note, fretmap, stringmap)
        print (f'note: {note}, fretmap_note: {fretmap_note}', f'stringmap_note: {stringmap_note}')
        tmp = np.nonzero(stringmap_note)[0]
        strings_possibilities.append(list(tmp+1))
        frets_possibilities.append(list(fretmap_note[tmp]))
    return strings_possibilities, frets_possibilities


def shortlistCombinations(string_possibilities, fret_possibilities):
    """
    shortlist all possible combinations for the note set, limiting to maximum one note per string
    """
    string_combination = []
    fret_combination = []
    i = 0

    for p in itertools.product(*string_possibilities):
        # Check if duplicates exist in p
        if len(p) == len(set(p)):
            string_combination.append(list(p))

            # For each note
            notes_states = []

            for i, f in enumerate(p):
                note_frets = fret_possibilities[i]
                # find f in string_possibilities[i]
                index_frets = int(np.where(string_possibilities[i] == f)[0])
                notes_states.append(note_frets[index_frets])
            fret_combination.append(notes_states)

    return string_combination, fret_combination

def limit_pitches(array):
    """
    limit pitches to the playable number of pitches.
    Limits to add:
    - Total number of pitches should be less than or equal to 6. 
    """
    if len(array) > 6:
        # Remove the lowest note
        array = array[-6:]
    return array

def absLoss(current_frets, target):
    """
    Returns left hand loss, only based on fret positions
    """
    cost = 0
    if len(current_frets) == 1:
        current_frets = current_frets[0]
    for i in np.arange(6):
        curr = current_frets[i]
        if target[i] == 0:
            c = 0
        else:
            c = np.abs(target[i]-curr)
        cost += c
    return cost

def prioritizeStrum(potential_strings, potential_frets):
    """
    Input potential states and strings
    Prioritise the mappings that can be played on subsequent strings
    return only those mappings
    """
    strings = []
    frets = []
    for i, state in enumerate(potential_strings):
        # Compute non zero indices. find avg of diff array. If avg is -1, then append
        nz = np.nonzero(state)[0]
        diff = np.diff(nz)
        if len(set(diff)) == 1 and diff[0] == 1:
        # if np.mean(diff) == 1:
            strings.append(state)
            frets.append(potential_frets[i])
    
    if not strings:
        return potential_strings, potential_frets

    else:
        return strings, frets
            
def fretboard_costfn(current_frets, potential_frets):
    costs = np.array([])
    for i, potfret in enumerate(potential_frets):
        cost = absLoss(current_frets, potfret)
        costs = np.append(costs, cost)

    return costs

def selectFretboardState(current_strings, current_frets, potential_strings, potential_frets):
    """
    Define cost
    """
    potential_strings, potential_frets = prioritizeStrum(potential_strings, potential_frets)
    costs = fretboard_costfn(current_frets, potential_frets)
    index = np.argmin(costs)
    fretboard_state = potential_frets[index]
    string_state = potential_strings[index]
    return string_state, fretboard_state

def transformTo6(strings_comb, frets_comb):
    """
    Change the dimension of an item of strings/ frets list from numNotes to 6 (guitar representation) for cost calculation 
    in subsequent steps.
    """
    strings_res = []
    frets_res = []
    
    for i, comb in enumerate(strings_comb):
        strings_tmp = np.zeros(6)
        frets_tmp = np.zeros(6)
        indices = np.array(comb)-1
        strings_tmp[indices] = comb
        frets_tmp[indices] = frets_comb[i]
        strings_res.append(strings_tmp)
        frets_res.append(frets_tmp)
    return strings_res, frets_res


def updateFBstate(current_frets, string_state, fretboard_state_tmp):
    if len(current_frets) == 1:
        current_frets = current_frets[0]
    
    if len(string_state) == 1:
        string_state = string_state[0]
    
    change_indices = np.nonzero(string_state)[0]
    
    fretboard_state = np.array(current_frets)
    
    fretboard_state[change_indices] = fretboard_state_tmp[change_indices]

    return fretboard_state


def genPolyFBMap(notes, fretmap, stringmap, current_strings, current_frets):
    """
    Generate polyphonic fretboard state map for a given timestamp
    """
    str_poss, frets_poss = genStringPossibilities(notes, fretmap, stringmap)
    strings_comb, frets_comb = shortlistCombinations(str_poss, frets_poss)
    # Transform strings_comb, frets_comb into 6 dimensional arrays.
    strings_res, frets_res = transformTo6(strings_comb, frets_comb)

    # If multiple possibilities
    if len(strings_comb) > 1:
        string_state, fretboard_state_tmp = selectFretboardState(current_strings, current_frets, strings_res, frets_res)
    
    else:
        string_state = strings_res
        fretboard_state_tmp = frets_res[0]
    
    fretboard_state = updateFBstate(current_frets, string_state, fretboard_state_tmp)

    return string_state, fretboard_state

def gen_poly_states(pitches, vels, fretmap, stringmap, bot_picking_map):
    """
    Input: rolled up pitches array
    """
    # Define initial positions for cost calculation
    current_frets = [5, 5, 5, 5, 5, 5]
    current_strings = [1, 2, 3, 4, 5, 6]
    
    # Just set position and don't strum
    
    fretboard_states = []
    string_states = []
    
    for i, notes in enumerate(pitches):
        string_state, fretboard_state = genPolyFBMap(notes, fretmap, stringmap, current_strings, current_frets)
        string_state = get_string_state(string_state, bot_picking_map, fretboard_state)
        
        # Make pluck style (left hand states and right hand plucks) 0 if velocity = 0.
        if vels[i] == 0:
            string_state = np.ones(6)
        fretboard_states.append(fretboard_state)
        string_states.append(string_state)
        current_strings = string_state
        current_frets = fretboard_state
    
    return fretboard_states, string_states