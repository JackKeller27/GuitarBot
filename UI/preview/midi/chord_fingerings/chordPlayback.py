import numpy as np
import pandas as pd
from fretboard_mapgen import fretToNote
from dict_maps import tuning, fret_distances
from generateChords import chordMidiToNotes
# import sqlite3

def getSingleChordArray(df, root, chordType, chordsDB, random=True):
    if random == True:
        # From df, get all rows with root and chordType
        print (f'root: {root}, chordType: {chordType}')
        df = getAllPossibilities(df, root, chordType)
        array = select_random_chord(df, chordsDB)
        
    fretnum, fretplay = transform_to_fretnum_fretplay(array)
    return fretnum, fretplay


def generate_chord_trajectory(roots, chordTypes, df, fret_distances):
    """
    Generate the whole left hand trajectory for any given chord progression
    
    Inputs
    roots: all roots in the sequence. Includes repetitions too. eg - [CM, Am] x 2 = [C, C, A, A]
    chordTypes: all chordTypes in the sequence. Includes repetitions too. eg - [CM, Am] x 2 = [Major, Major, minor, minor]
    df: dataframe containing all chords (vocabulary)

    Outpus
    ifretnums: length = len(chord_progression)
    iplaynums: length = len(chord_progression)

    """
    ifretnums = []
    ifretplays = []
    
    # Select the first chord at random
    current_fretnum, current_fretplay = getSingleChordArray(df, roots[0], chordTypes[0], random=True)
    prev_fretnum = current_fretnum
    ifretnums.append(current_fretnum)
    ifretplays.append(current_fretplay)

    for i in range(1, len(roots)):
        print (f'curr chord: {roots[i-1]}{chordTypes[i-1]}, i: {i-1}, current fretnum: {current_fretnum}')
        # Get all possible chords corresponding to the next chord
        df_shortlisted = getAllPossibilities(df, roots[i], chordTypes[i])

        # Convert all possible chords to fretnum arrays
        next_fretnum_all = convert_df_to_chord_array(df_shortlisted)

        # Get the most optimised chord based on distance based cost function
        next_fretnum = shortlist(prev_fretnum, current_fretnum, next_fretnum_all, fret_distances)

        ifretnum, ifretplay = transform_to_fretnum_fretplay(next_fretnum)
        ifretnums.append(ifretnum)
        ifretplays.append(ifretplay)
        prev_fretnum = current_fretnum
        current_fretnum = next_fretnum

    return ifretnums, ifretplays

def convert_df_to_chord_array(df):
    """
    Get all chords from the dataframe
    """
    all_chords = []
    for i in range(len(df)):
        all_chords.append(list(df.values[i][3:9]))
    return all_chords

def getAllPossibilities(df, root, chordType):
    """
    Get a dataframe containing all chords for given root and chordType
    """
    return df[(df['Root'] == root) & (df['ChordType'] == chordType)]

def transform_to_fretnum_fretplay(array):
    fretnum = []
    fretplay = []
    for i in array:
        if i == 'X':
            fretplay.append(3)
            fretnum.append(5)
        
        elif int(float(i)) == 0:
            fretplay.append(1)
            fretnum.append(5)

        else:
            fretplay.append(2)
            fretnum.append(int(float(i)))
    return fretnum, fretplay

def select_random_chord(df, chordsDB):
    index = np.random.randint(0, len(df))
    chord_row = list(df.values[index][3:9])
    catch = ['X', '0.0', '0']
    intersection = list(set(catch) & set(chord_row))
    if intersection:
        # print (f'chord_row: {chord_row}')
        if chordsDB == 'Bot':
            return select_random_chord(df)
        else:
            return chord_row
    else:
        return chord_row

def shortlist(curr_state, potential_states, fret_distances):
    """
    Shortlist function for computing costs corresponding to each potential state and returns an updated state for LH adjusted for 0/ X

    inputs
    curr_state: current sate. May or may not be similar to one in df. It includes LH adjustment if made to accomodate 0/ X.
    potential_states: All possible potential states

    outputs
    ifretnum: final shortlisted state: 0/ X adjusted
    iplaycommand: RH array
    """
    costs = []
    updated_states = []
    updated_playcommands = []
    for i in range(len(potential_states)):
        potential_state = potential_states[i]
        try:
            cost, updated_state, updated_plays = compute_cost(curr_state, potential_state, fret_distances)
        except Exception as e:
            cost = 1000
            updated_state = potential_state
            updated_plays = []
        costs.append(cost)
        updated_states.append(updated_state)
        updated_playcommands.append(updated_plays)

    minCostIndex = np.argmin(costs)
    ifretnum = updated_states[minCostIndex]
    iplaycommand = updated_playcommands[minCostIndex]
    return ifretnum, iplaycommand

def compute_cost(curr_state, potential_state, fret_distances):
    """
    Cost function agnostic of the number of strings
    
    inputs
    curr_state: Doesn't necessarily have to be one of the exact chord positions in the df. X can be replaced by any other fretnum, same for 0.
    potential_state: to compute cost wrt current

    outputs
    cost, updated_state
    """
    cost = 0
    if 'X' or '0.0' in potential_state:
        updated_play = []
        for i, curr in enumerate(curr_state):
            if potential_state[i] == '0' or '0.0':
                cost += 0
                potential_state[i] == curr
                updated_play.append(1)
            
            elif potential_state[i] == 'X':
                cost += 0
                potential_state[i] == curr
                updated_play.append(3)
            
            else:
                # cost += abs(int(float(curr)) - int(float(potential_state[i])))
                pot = float(fret_distances[str(potential_state[i])])
                c = float(fret_distances[str(curr)])
                cost += abs(c - pot)
                potential_state[i] == curr
                updated_play.append(2)
        updated_state = potential_state
            
    else:
        for i, curr in enumerate(curr_state):
            # cost += abs(int(float(curr)) - int(float(potential_state[i])))
            pot = float(fret_distances[str(potential_state[i])])
            c = float(fret_distances[str(curr)])
            cost += abs(c - pot)
        updated_state = potential_state
        updated_state, updated_play = transform_to_fretnum_fretplay(updated_state)
    return cost, updated_state, updated_play
