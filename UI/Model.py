from constants.bot_specs import DEFAULT_BPM, MIN_BPM, MAX_BPM
from constants.time_signatures import DEFAULT_TIME_SIG
from constants.chord_modes import DEFAULT_CHORD_MODE
from parse import parseleft_M, parseright_M
from models.Section import Section

# model stores all of the UI's data
# model also handles the business logic for the UI -> calls UIParse.py methods
class Model:
    def __init__(self):
        self.song_title = 'Song Title'

        # TODO: add logic to limit bpm to MIN_BPM, MAX_BPM range and update view accordingly
        self.bpm = DEFAULT_BPM

        self.time_signature = DEFAULT_TIME_SIG
        self.chord_mode = DEFAULT_CHORD_MODE

        self.sections = {} # Key-value pairs of form {id, Section}

    # Called by Controller, adds a new section to the Model
    def add_section(self, id, name):
        new_section = Section(id, name) # left_arm, right_arm will be initialized to empty lists
        self.sections[id] = new_section

    # Called by Controller, updates the data for a particular section (indexed by id)
    # Data includes name and left_arm, right_arm lists
    def update_section_data(self, id, name, left_arm, right_arm):
        section = self.sections[id]
        section.name = name
        section.left_arm = left_arm
        section.right_arm = right_arm

    # Called by Controller, clears all left_arm and right_arm data for a particular section (indexed by id)
    def clear_section_data(self, id):
        self.sections[id].clear()

    # Called by Controller, removes a particular section (indexed by id)
    def remove_section(self, id):
        self.sections.pop(id)

    def send_arm_lists(self, section_ids):
        # call parse.py, pass in left_arm, right_arm lists of each Section in self.sections
        # appends arm lists to song based on the order of the sections in the Song Builder
        # TODO: modify parse.py to accept new chord notations

        for id in section_ids:
            section = self.sections[id]
            print('section: ', id)
            print(section.left_arm, section.right_arm)
            
            measure_time = int(self.time_signature[0]) * (60/self.bpm) # calculate the total time for each measure in seconds
            parseleft_M(section.left_arm, measure_time) 
            parseright_M(section.right_arm, measure_time)