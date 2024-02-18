from chordPlayback import compute_cost, getAllPossibilities, convert_df_to_chord_array
import numpy as np


def flatten(li):
    flat_list = []
    for sublist in li:
        for item in sublist:
            flat_list.append(item)
    return flat_list

def get_fingerings(chord_progression, df):
    num_chords = len(chord_progression)
    fingerings = []
    num_fingerings = []
    
    for i in range(num_chords):
        root = chord_progression[i].split(' ')[0]
        chordType = chord_progression[i].split(' ')[1]
        df_shortlisted = getAllPossibilities(df, root, chordType)
        # Convert all possible chords to fretnum arrays
        next_fretnum_all = convert_df_to_chord_array(df_shortlisted)
        fingerings.append(next_fretnum_all)
        num_fingerings.append(len(next_fretnum_all))
    
    return fingerings, num_fingerings, num_chords


def convert_cost_to_prob(cost, cost_range, cost_max):
    cost_min = cost_max-cost_range
    prob = 1-cost/(cost_max-cost_min)
    return prob

def initialize_viterbi(num_fingerings, num_chords):
    viterbi = np.zeros((num_chords, max(num_fingerings)))
    # updated_states_all = np.zeros((num_chords, max(num_fingerings)))
    backpointer = np.zeros((num_chords, max(num_fingerings)), dtype=int)
    viterbi[0, :] = np.ones(max(num_fingerings))
    return viterbi, backpointer


def terminate_viterbi(viterbi):
    best_cost = np.min(viterbi[-1, :])
    best_fingering = np.argmax(viterbi[-1, :])
    best_trajectory = [best_fingering]
    return best_cost, best_fingering, best_trajectory

def get_best_trajectory(num_chords, backpointer, best_trajectory, best_fingering):
    for t in range(num_chords-1, 0, -1):
        best_fingering = backpointer[t, best_fingering] # Get the best fingering index for the previous chord
        best_trajectory.insert(0, best_fingering)   # Insert at the beginning of the list
    
    return best_trajectory, best_fingering

def post_process_viterbi(li_viterbi_tmp):
    numMeasures = len(li_viterbi_tmp)//4
    li_viterbi = []
    for m in range(numMeasures):
        li_vib = []
        for i in range(4):
            tmp = li_viterbi_tmp[m*4+i]
            li_vib.append(tmp)
        li_viterbi.append(li_vib)
    return li_viterbi

def get_final_trajectory(best_trajectory, updated_fingerings, updated_playcommands):
    final_trajectory = []
    final_rh = []
    for i, traj in enumerate(best_trajectory):
        try:
            fing = [updated_fingerings[i][traj]]
            if i != len(best_trajectory)-1:
                fing.append(updated_playcommands[i][traj])
            else:
                fing.append([2, 2, 2, 2, 2, 2])
            final_trajectory.append(fing)
        except:
            continue
    return final_trajectory

def initialize_updated_playcommands(num_chords, num_fingerings):
    updated_playcommands = []
    for i in range(num_chords):
        updated_playcommands.append([])
        for j in range(num_fingerings[i]):
            updated_playcommands[i].append([])
    return updated_playcommands

def viterbi_recursion(num_chords, num_fingerings, fingerings, fret_distances, range_cost, max_cost, viterbi, backpointer, updated_fingerings, updated_playcommands):
    for t in range(1, num_chords):
        # Back calculate costs one step at a time
        for j in range(num_fingerings[t]):
            costs = []
            # updated_states = []
            for i in range(num_fingerings[t-1]):
                potential_prev_state = fingerings[t-1][i] # curr_state is the ith fingering of the previous chord
                curr_state = fingerings[t][j]  # potential_state is the jth fingering of the current chord
                # TODO: Use updated_play
                cost, updated_state, updated_play = compute_cost(curr_state, potential_prev_state, fret_distances)
                cost = convert_cost_to_prob(cost, range_cost, max_cost)
                costs.append(cost)
                updated_fingerings[t-1][i] == updated_state
                updated_playcommands[t-1][i] = updated_play
            while len(costs) < max(num_fingerings):
                max_cost_prob = convert_cost_to_prob(max_cost, range_cost, max_cost)
                costs.append(max_cost_prob)
            
            prob_transitions = viterbi[t-1, :] * costs
            best_state = np.argmax(prob_transitions)
            viterbi[t, j] = prob_transitions[best_state]
            backpointer[t, j] = best_state
    
    return viterbi, backpointer, updated_fingerings, updated_playcommands

def viterbi_search(chord_progression, df, fret_distances):
    """
    Viterbi algorithm for finding the most likely trajectory of fingerings given a chord progression.
    """
    # Define cost boundaries for later computation
    max_cost = 6 * max(fret_distances.values())
    min_cost = 0
    range_cost = max_cost-min_cost
    
    chord_progression = flatten(chord_progression)
    
    fingerings, num_fingerings, num_chords = get_fingerings(chord_progression, df)
    updated_fingerings = fingerings
    # Initialize an empty list with the same shape as fingerings
    updated_playcommands = initialize_updated_playcommands(num_chords, num_fingerings)

    # Initialization
    viterbi, backpointer = initialize_viterbi(num_fingerings, num_chords)
    
    # Recursion
    viterbi, backpointer, updated_fingerings, updated_playcommands = viterbi_recursion(num_chords, num_fingerings, fingerings, fret_distances, range_cost, max_cost, viterbi, backpointer, updated_fingerings, updated_playcommands)
    
    # Termination
    best_cost, best_fingering, best_trajectory = terminate_viterbi(viterbi)

    # Selection
    best_trajectory, best_fingering = get_best_trajectory(num_chords, backpointer, best_trajectory, best_fingering) # Backtracking
    final_trajectory = get_final_trajectory(best_trajectory, updated_fingerings, updated_playcommands)
    final_trajectory = post_process_viterbi(final_trajectory)
    return final_trajectory