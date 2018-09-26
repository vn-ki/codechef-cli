from asciimatics.widgets import (Frame, TextBox, Layout,
                                 ListBox, Widget, Button,
                                 Background, PopUpDialog)
from asciimatics.event import KeyboardEvent
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication, \
    InvalidFields

import sys
import logging
import threading
from codechef_cli import util

# Initial data for the form
form_data = {
    "TA": ["Hello world!", "How are you?"],
    "problem_code": 0
}

palette = {
    "invalid": (Screen.COLOUR_BLACK, Screen.A_NORMAL, Screen.COLOUR_RED),
    "label": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK),
    "title": (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK),
    "selected_focus_field": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLUE),
    "focus_edit_text": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK),
    "focus_button": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK),
    "selected_focus_control": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK),
    "disabled": (Screen.COLOUR_BLACK, Screen.A_BOLD, Screen.COLOUR_BLACK),
    "background": (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK),
    "shadow": (Screen.COLOUR_BLACK, None, Screen.COLOUR_BLACK),
    "borders": (Screen.COLOUR_BLACK, Screen.A_BOLD, Screen.COLOUR_BLACK),
    "scroll": (Screen.COLOUR_CYAN, Screen.A_NORMAL, Screen.COLOUR_BLACK),
    "button": (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK),
    "field": (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK),
    "selected_field": (Screen.COLOUR_YELLOW, Screen.A_BOLD, Screen.COLOUR_BLACK),
    "focus_field": (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK),
}

logging.basicConfig(filename="forms.log", level=logging.DEBUG)


class TextArea(TextBox):
    def reset(self):
        # Reset to original data and move to end of the text.
        self._line = 0
        self._column = 0

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code in [10, 13]:
                return event
            elif event.key_code == Screen.KEY_BACK:
                return event
            elif event.key_code == Screen.KEY_DELETE:
                return event
            elif event.key_code >= 32:
                return event
        return super().process_event(event)


class DemoFrame(Frame):
    def __init__(self, screen, contest):
        super(DemoFrame, self).__init__(screen,
                                        int(screen.height),
                                        int(screen.width),
                                        data=form_data,
                                        name="My Form")
        layout = Layout([4, 18, 1], fill_frame=True)
        self.problem_body = TextArea(Widget.FILL_FRAME,
                                     name="TA")
        self.problem_body.register_frame(self)
        self.problem_body.custom_colour = "title"
        self.contest = contest
        self.add_layout(layout)
        self._list_view = ListBox(
            10, name="problem_code",
            options=[
                (val, idx)
                for idx, val in enumerate(contest.problem_codes)
            ],
            on_change=self._list_change,
            on_select=self._list_change)
        layout.add_widget(self._list_view, 0)
        layout.add_widget(self.problem_body, 1)
        layout2 = Layout([1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Quit", self._quit), 2)
        layout2.add_widget(Button("Submit", self._submit), 1)
        self.fix()
        self.palette = palette
        self._list_change()
        # self.set_theme("monochrome")

    def _on_click(self):
        self._scene.add_effect(
            PopUpDialog(self._screen, "You selected the menu!", ["OK"]))

    def _list_change(self):
        self.save()
        index = self.data['problem_code']
        # TODO(vn-ki): refractor this

        def set_text(lines):
            self.problem_body.value = lines
            self.problem_body.focus()

        def set_text_body(prob):
            lines = util.html_to_terminal(prob.body).split('\n')
            lines = [prob.problem_name + ''] + lines
            set_text(lines)

        def write_prob_to_screen():
            prob = self.contest[index]
            if len(self.problem_body.value) > 1:
                return
            set_text_body(prob)
        if not self.contest.is_problem_fetched(index):
            t = threading.Thread(name='deamon', target=write_prob_to_screen)
            t.setDaemon(True)
            t.start()
            set_text(['Loading....'])
        else:
            write_prob_to_screen()
            prob = self.contest[index]
            set_text_body(prob)

    def _quit(self):
        raise StopApplication("User requested exit")

    def _submit(self):
        self.save()
        index = self.data['problem_code']
        pc = self.contest[index].problem_code
        cc = self.contest[index].contest_code

def contest_screen(screen, scene, contest):
    screen.play([Scene([
        Background(screen),
        DemoFrame(screen, contest)
    ], -1)], stop_on_resize=True, start_scene=scene)


def draw_contest_page(contest):
    def cache_prob(idx):
        contest[idx]
    prob = contest[0]
    lines = util.html_to_terminal(prob.body).split('\n')
    lines = [prob.problem_name + ''] + lines
    global form_data
    form_data['TA'] = lines
    last_scene = None
    while True:
        try:
            Screen.wrapper(contest_screen, catch_interrupt=False,
                           arguments=[last_scene, contest])
            sys.exit(0)
        except ResizeScreenError as e:
            last_scene = e.scene
