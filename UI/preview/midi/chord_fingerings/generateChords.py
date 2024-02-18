import numpy as np
from fretboard_mapgen import mapgen, indexPositions
from dict_maps import *
import itertools

# Write a function to generate all major chords that can be played using all six strings. Do not ignore inversions

def noteToMidi(note, first=True):
    """
    Returns midi location(s) of a given note and its type.
    Inputs
    type = root/ all
    """
    if first is True:
        return root_midi_dict[note]

    else:
        return note_midi_dict[note]

def midiToNote(midi):
    while midi > 51:
        midi = midi-12
    pos = list(root_midi_dict.values()).index(midi)
    return list(root_midi_dict.keys())[pos]

def chordMidiToNotes(chord_MIDI):
    chord_notes = []
    for midi in chord_MIDI:
        chord_notes.append(midiToNote(midi))
    return chord_notes

def chordsMidiToNotes(chords_MIDI):
    chords_notes = []
    for chord_MIDI in chords_MIDI:
        chords_notes.append(chordMidiToNotes(chord_MIDI))
    return chords_notes

def genBaselineChord(root, chordType):
    intervals = chord_interval_dict[chordType]
    numNotes = len(intervals) + 1
    # Get MIDI of root
    root_MIDI_base = noteToMidi(root)
    chord_MIDI_base = [root_MIDI_base]    # Initializing the chord MIDI array with root MIDI
    chord_notes_base = [root]   # Initializing the chord note array with root note
    for interval in intervals:
        midi_interval = root_MIDI_base + interval
        chord_MIDI_base.append(midi_interval)
        chord_notes_base.append(midiToNote(midi_interval))

    return chord_MIDI_base, chord_notes_base

def getAllNotes(baseline_chord):
    """
    Generate all possible MIDI notes (across octaves) corresponding to the given chord
    
    Input
    baseline_chord: Notes (not midi) output of genBaselineChord
    
    Return
    all_notes
    """
    all_notes = []
    for note in baseline_chord:
        all_notes.append(noteToMidi(note, False))
    return all_notes


def getNotesArray(all_notes):
    """
    Flatten the all_notes array
    """
    return list(itertools.chain(*all_notes))

def getAllNoteSets(all_notes, numNotes):
    """
    Get all possible combinations from the flattened array, without restricting must have notes.
    """
    
    s = list(all_notes)
    maxNotes = 6    # Maximum number of notes that can be played on a guitar
    return list(itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(numNotes, maxNotes + 1)))

def dataStructureHandle(all_combs):
    """
    Handle the data structure of the all_notes array
    """
    converted = []
    for c in all_combs:
        c = list(c)
        converted.append(c)
    return converted

def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))

def checkRelevance(lst):
    for l in lst:
        if len(l) == 0:
            return False

def filterRelevantCombinations(all_combinations, all_notes, numNotes):
    """
    Filter combinations containing all the notes in the baseline chord
    """
    all_combinations = dataStructureHandle(all_combinations)
    relevant_combinations = []
    for i, comb in enumerate(all_combinations):
        comb.sort()
        intersect  = []
        for j in np.arange(numNotes):
            common = intersection(comb, all_notes[j])
            intersect.append(common)
        rel = checkRelevance(intersect)
        # print (f'intersection: {intersect}, relevance: {rel}')
        if rel != False:
            relevant_combinations.append(comb)
    return relevant_combinations


def genChordPossibilities(comb, fmap, smap):
    """
    Generate all possible note positions for a given set of notes supposed to be played together.
    Note that this function will give isolated fret and string position possibilities for each note.
    """
    notes_fretpos, notes_stringpos = [], []
    for note in comb:
        note_fretpos, note_stringpos = indexPositions(note, fmap, smap)
        notes_fretpos.append(note_fretpos)
        notes_stringpos.append(note_stringpos)
    return notes_fretpos, notes_stringpos

def shortlistPossibilities(notes_fretpos, notes_stringpos):
    """
    Shortlist the playable possible combinations of frets and strings for each combination.
    """
    
    shortlisted_fretpos = []
    shortlisted_stringpos = []
    
    for p in itertools.product(*notes_stringpos):
        p = list(p)
        if len(p) == len(set(p)) and 0 not in p:
            shortlisted_stringpos.append(p)
            notes_states = []
            for i, f in enumerate(p):
                note_frets = notes_fretpos[i]
                index_frets = int(np.where(notes_stringpos[i] == f)[0])
                notes_states.append(note_frets[index_frets])
            shortlisted_fretpos.append(notes_states)

    return shortlisted_fretpos, shortlisted_stringpos
            

def genConfigsPerComb(comb, fmap, smap):
    """
    Get all possible configs of a given set of notes
    """
    f_possibilities, s_possibilities = genChordPossibilities(comb, fmap, smap)
    f_shortlisted, s_shortlisted = shortlistPossibilities(f_possibilities, s_possibilities)
    return f_shortlisted, s_shortlisted
    

def genAllConfigs(relevant_combinations, fmap, smap):
    """
    Generate all possible configurations on the fretboard from given notes. Include everything such as inversions, etc.
    
    Input
    baseline_chord: Notes (not midi) output of genBaselineChord
    
    Return
    all_configs: all possible chord configurations
    """
    f_pos_all = []
    s_pos_all = []
    combs = []
    for comb in relevant_combinations:
        f_pos_comb, s_pos_comb = genConfigsPerComb(comb, fmap, smap)
        if len(f_pos_comb) > 0:
            f_pos_all.extend(f_pos_comb)
            s_pos_all.extend(s_pos_comb)
            combs.append(comb)

    return f_pos_all, s_pos_all, combs


def getCombinations(root, chordType, fmap, smap):
    _, chord_notes = genBaselineChord(root, chordType)
    all_notes = getAllNotes(chord_notes)
    numNotes = len(all_notes)
    all_notes_flattened = getNotesArray(all_notes)
    all_note_sets = getAllNoteSets(all_notes_flattened, numNotes)
    print (f'all note sets: {len(all_note_sets)}')
    rel_combs = filterRelevantCombinations(all_note_sets, all_notes, numNotes)
    print (f'Combinations with all chord notes: {len(rel_combs)}')
    fpos_all, spos_all, final_combs = genAllConfigs(rel_combs, fmap, smap)
    print (f'num: {len(fpos_all)}, unique midiNums: {len(final_combs)}')
    return fpos_all, spos_all, final_combs


# if __name__ == '__main__':
#     fmap, smap = mapgen()
#     getCombinations('A', 'Minor', fmap, smap)