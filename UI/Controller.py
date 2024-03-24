from Model import Model
from View import View, ChordNotationsPopup

class Controller:
    def __init__(self, view: View, model: Model):
        self.view = view
        self.model = model

        self.song_controls_frame = view.song_controls_frame
        self.song_frame = view.song_frame
        self.song_builder_frame = view.song_builder_frame
        self.new_section_btn = view.new_section_btn

        self._create_event_bindings()

    def start(self):
        self.view.start_mainloop()

    def _create_event_bindings(self):
        ### SONG CONTROLS
        # Song title entry
        self.song_controls_frame.song_title.trace_add(('write'), self._update_song_title_handler)

        # BPM spinbox
        self.song_controls_frame.bpm_spinbox.bind('<KeyRelease>', lambda e: self._update_bpm_handler(e, 'KeyRelease'))
        self.song_controls_frame.bpm_spinbox.bind('<<Increment>>', lambda e: self._update_bpm_handler(e, 'Increment'))
        self.song_controls_frame.bpm_spinbox.bind('<<Decrement>>', lambda e: self._update_bpm_handler(e, 'Decrement'))

        # Time signature options
        self.song_controls_frame.time_signature.trace_add('write', self._update_time_sig_handler)

        # Chord mode options
        self.song_controls_frame.chord_mode.trace_add('write', self._update_chord_mode_handler)

        # Chord notations btn
        self.song_controls_frame.chord_notation_btn.config(command=self._show_chord_notations_popup)

        # Save btn
        self.song_controls_frame.save_btn.config(command=self._save_song_handler)

        # Load btn
        self.song_controls_frame.load_btn.config(command=self._load_song_handler)

        # Send btn
        self.song_controls_frame.send_btn.config(command=self._send_song_handler)

        ### SECTIONS/SECTION LABELS
        for section in self.song_frame.sections:
            section_frame, section_labels = section
            section_labels.eraser_btn.configure(command=lambda: self._clear_section_handler(section_frame)) # use configure for CTk btn

    # Event handlers below
    ### SONG CONTROLS
    def _update_song_title_handler(self, event, *args):
        self.model.song_title = self.song_controls_frame.song_title.get()

    def _update_bpm_handler(self, event, type):
        # This event handler will run before increment/decrement buttons update the actual Entry, so we need to manually increment/decrement to account for that
        if type == 'Increment':
            self.model.bpm = int(self.song_controls_frame.bpm_spinbox.get()) + 1
        elif type == 'Decrement':
            self.model.bpm = int(self.song_controls_frame.bpm_spinbox.get()) - 1
        elif type == 'KeyRelease':
            self.model.bpm = int(self.song_controls_frame.bpm_spinbox.get())

    def _update_time_sig_handler(self, event, *args):
        self.model.time_signature = self.song_controls_frame.time_signature.get()

    def _update_chord_mode_handler(self, event, *args):
        self.model.chord_mode = self.song_controls_frame.chord_mode.get()

    def _show_chord_notations_popup(self):
        popup = ChordNotationsPopup(self.view)

        # when "Close" button is clicked, popup will be destroyed
        popup.close_btn.config(command=popup.destroy)

    # Save btn
    def _save_song_handler(self):
        pass

    # Load btn
    def _load_song_handler(self):
        pass

    # Send btn
    def _send_song_handler(self):
        pass

    ### SECTIONS/SECTION LABELS
    def _clear_section_handler(self, section_frame):
        # TODO: this is only interacting with view right now. Should update model as well
        print('clear ', section_frame.name)
        section_frame.clearTable()